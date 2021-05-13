import pytest
import serializer


def assert_restored_object(subject):
    for language in serializer.get_formats():
        serialized = serializer.dumps(subject, language)
        restored = serializer.loads(serialized, language)
        assert restored == subject


def test_none():
    subject = None
    assert_restored_object(subject)


def test_ellipsis():
    subject = Ellipsis
    assert_restored_object(subject)


def test_notimplemented():
    subject = NotImplemented
    assert_restored_object(subject)


def test_false():
    subject = False
    assert_restored_object(subject)


def test_true():
    subject = True
    assert_restored_object(subject)


def test_int():
    subject = -999
    assert_restored_object(subject)


def test_float():
    subject = 22 / 7
    assert_restored_object(subject)


def test_complex():
    subject = complex(-4214, 0.73278)
    assert_restored_object(subject)


def test_str():
    subject = "Lorem ipsum"
    assert_restored_object(subject)


def test_list():
    subject = [10, 30, 20]
    assert_restored_object(subject)


def test_tuple():
    subject = (10, 30, 20)
    assert_restored_object(subject)


def test_range():
    subject = range(10, 30, 20)
    assert_restored_object(subject)


def test_bytes():
    subject = bytes.fromhex("02 ad 73 ff")
    assert_restored_object(subject)


def test_bytearray():
    subject = bytearray.fromhex("7d 10 37 00")
    assert_restored_object(subject)


def test_set():
    subject = {10, 30, 20}
    assert_restored_object(subject)


def test_frozenset():
    subject = frozenset({10, 30, 20})
    assert_restored_object(subject)


def test_dict():
    subject = {10: 20, 30: 40}
    assert_restored_object(subject)
