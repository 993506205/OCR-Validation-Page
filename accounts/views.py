from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from dirprojects.models import DirProject
from ocrfiles.models import Ocrfiles
from datetime import datetime
from django.shortcuts import render, get_object_or_404
import json
from functions import emptyDirClean


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if password match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is taken')
                return redirect('register')
            else:
                # Check email
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is being used')
                    return redirect('register')
                else:
                    # Create user
                    user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
                    # Login after register
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in')
                    # return redirect('index')
                    user.save()
                    messages.success(request, 'registeration successful')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Hello! {0}.'.format(username))
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Successful logout')  
        return redirect('index')


def dashboard(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            func_type = data['type']
            if func_type == "delete":
                dir_id = data['dir_id']
                dir_delete = get_object_or_404(DirProject, id=dir_id)
                dir_delete.delete()
                messages.success(request, 'Successful Delete!')

                # clean empty dirs
                emptyDirClean.deleteDirs()
            elif func_type == "edit":
                dir_id = data['dir_id']
                dir_name = data['dir_name']
                dir_des = data['dir_des']
                DirProject.objects.filter(id=dir_id).update(name=dir_name, description=dir_des)
    except Exception as e:
        messages.error(request, 'The Project could not be delete: Error {}'.format(e))  

    date_now = datetime.now()
    formatedDate =date_now.strftime('%d %b %Y')
    if DirProject.objects.filter(creator_id=request.user.id).exists():
        dir_projs = DirProject.objects.filter(creator_id=request.user.id)
        # ocr_files = Ocrfiles.objects.filter(dir_project=dir_projs)
        # ocr_object = (Q(ocrfiles=ocr_file) for ocr_file in ocr_files)

        content = {
            # 'ocr_files': ocr_files,
            # 'ocr_object': ocr_object,
            'dir_project': dir_projs,
            'now': formatedDate
        }
        return render(request, 'accounts/dashboard.html',content)
    else:
        return render(request, 'accounts/dashboard.html',{'now': formatedDate})
