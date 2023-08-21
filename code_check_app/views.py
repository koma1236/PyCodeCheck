from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import SignupForm, UserFiles, UsersMail
from code_check_app.modules.files_uploader.uploader import Uploader
from code_check_app.modules.base import base_exec


def login_page(request):
    """Displays the login page and authenticates the user."""

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('files')
        else:
            error_message = "Incorrect username or password"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def signup(request):
    """Displays the signup page and registers a new user."""

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in after successful registration
            login(request, user)
            return redirect('login_page')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def files(request):
    """Displays the files page and handles file uploading and deletion."""

    if not request.user.is_authenticated:
        return redirect('login_page')
    if request.method == 'POST':
        if request.POST.get('action') == 'upload':
            Uploader(request).upload_user_files()
        elif request.POST.get('action') == 'delete':
            file_id = request.POST.get('file_id')
            base_exec.delete_file(file_id)
    context = {'files': UserFiles.objects.filter(uploaded_by_user_id=request.user.id)}
    return render(request, 'files.html', context=context)


def mail(request):
    """Displays the mail page and shows the user's mails."""

    if not request.user.is_authenticated:
        return redirect('login_page')
    context = {'mails': UsersMail.objects.order_by('-mail_send_date').filter(user_id=request.user.id)}
    return render(request, 'mail.html', context=context)
