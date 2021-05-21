from .models import SignupForm
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "something went wrong")

    form = SignupForm()
    return render(request, 'authentication/signup.html', {'form': form})