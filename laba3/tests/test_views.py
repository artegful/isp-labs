import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from pytest_django.asserts import assertTemplateUsed, assertRedirects
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from note.models import Note, NoteForm
from authentication.models import SignupForm, SendResetEmailForm, SetPasswordForm


@pytest.fixture
def users():
    users = list()
    test_user1 = User.objects.create_user(
        username="testuser1", password="12345", email="artemklimo@gmail.com"
    )
    test_user1.save()
    users.append(test_user1)

    test_user2 = User.objects.create_user(username="testuser2", password="12345")
    test_user2.save()
    users.append(test_user2)

    return users


@pytest.fixture
def notes(users):
    test_note1 = Note.objects.create(user=users[0], title="test user1", content="")
    test_note2 = Note.objects.create(user=users[1], title="test user2", content="")


@pytest.mark.parametrize(
    "url",
    [
        r"/authentication/login",
        r"/authentication/signup",
        r"/add",
        r"/authentication/reset-password",
    ],
)
def test_response_status(client, url):
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "url, template",
    [
        (r"/authentication/signup", r"authentication/signup.html"),
        (r"/authentication/login", r"registration/login.html"),
        (r"/add", r"note/add_note.html"),
    ],
)
def test_right_templates(client, url, template):
    response = client.get(url)

    assertTemplateUsed(response, template)


def test_redirect_to_login(client):
    response = client.get(r"/")

    assertRedirects(response, r"/authentication/login")


@pytest.mark.django_db
def test_index(client, users):
    client.login(username="testuser1", password="12345")

    response = client.get(r"/")
    assertTemplateUsed(response, r"note/notes_list.html")


@pytest.mark.django_db
def test_delete_note(client, notes):
    user = User.objects.first()
    assert client.login(username=user.username, password="12345")

    note = Note.objects.filter(user=user).first()

    note_amount = Note.objects.count()
    response = client.get(fr"/{note.pk}/delete")

    assert note_amount - 1 == Note.objects.count()
    assert not Note.objects.filter(pk=note.pk)


@pytest.mark.django_db
def test_edit_note(client, notes):
    user = User.objects.first()
    assert client.login(username=user.username, password="12345")

    note = Note.objects.filter(user=user).first()

    note_amount = Note.objects.count()
    response = client.get(fr"/{note.pk}/edit")

    assert response.status_code == 200
    assert note_amount == Note.objects.count()
    assert Note.objects.filter(pk=note.pk)


@pytest.mark.django_db
def test_signup(client):
    data = {
        "username": "Vasya",
        "email": "vasya@gmail.com",
        "password1": "vasyapassword",
        "password2": "vasyapassword",
    }
    assert SignupForm(data=data).is_valid()

    client.post(r"/authentication/signup", data)
    assert User.objects.filter(username=data["username"])


@pytest.mark.django_db
def test_add_note(client, users):
    data = {"title": "test title", "content": "sample content"}
    assert NoteForm(data=data).is_valid()

    note_count = Note.objects.count()
    client.login(username=users[0].username, password="12345")
    client.post(r"/add", data)
    assert note_count + 1 == Note.objects.count()


@pytest.mark.django_db
def test_change_password(client, users):
    data = {
        "old_password": "12345",
        "new_password1": "hellohihihi",
        "new_password2": "hellohihihi",
    }
    user = users[0]
    assert PasswordChangeForm(user, data=data).is_valid()

    assert client.login(username=user.username, password="12345")
    response = client.post(r"/authentication/change-password", data)
    assert client.login(username=user.username, password=data["new_password2"])


@pytest.mark.django_db
def test_reset_password(client, users):
    data = dict(email="artemklimo@gmail.com")

    assert SendResetEmailForm(data=data).is_valid()

    assert client.post(r"/authentication/reset-password", data).status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "password",
    ["hellohihihi", "passwordpassword", "saymynamesaymyname"],
)
def test_complete_reset_password(client, users, password):
    uid = urlsafe_base64_encode(force_bytes(users[0].pk))
    token = PasswordResetTokenGenerator().make_token(users[0])
    link = reverse(
        "complete_password_reset",
        kwargs=dict(uidb64=uid, token=token),
    )

    assert client.get(link).status_code == 200

    data = dict(new_password1=password, new_password2=password)
    assert SetPasswordForm(data=data).is_valid()

    client.post(link, data).status_code == 200
    assert client.login(username=users[0].username, password=password)
