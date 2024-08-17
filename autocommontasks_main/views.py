from django.shortcuts import render, redirect
from django.http import HttpResponse
# imports the function from the TASKS.PY of DATAENTRY folder
from dataentry.tasks import celery_test_task
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth


def home(request):
    return render(request, 'home.html')


# celery test
def celery_test(request):
    # execute time - consumin task here for celery execution
    celery_test_task.delay()  # calls the celery_test_task function and
    # execute this asynchronously or in the background or not at the same time
    # but we get the H3 message displayed right away.
    return HttpResponse('<h3>Function executed successfully.</h3>')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful.')
            return redirect('register')
        else:
            context = {
                'form': form,
            }
            # loads the web page again
            return render(request, 'register.html', context)

    else:
        form = RegistrationForm()
        context = {
            'form': form,
        }
    return render(request, 'register.html', context)


def login(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # gets the value from the Django Form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                # authenticated user is login
                auth.login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')

    else:
        form = AuthenticationForm()
        context = {
            'form': form,
        }

    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')
