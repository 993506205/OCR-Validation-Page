from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DirProjForm
from django.http import HttpResponseRedirect
from functions.save2db import create_ocrfiles
from datetime import datetime
from .models import DirProject
from django.urls import reverse
from django.contrib import messages
from ocrfiles.choices import type_choices
from django.http import JsonResponse



def prj_create(request):
    if request.method == "POST":
        form = DirProjForm(request.POST)
        files = [request.FILES.get('file[%d]' % i)
        for i in range(0, len(request.FILES))]
        try:
            if form.is_valid():
                username = None
                creator_id = -1
                if request.user.is_authenticated:
                    username = request.user.username
                    creator_id = request.user.id
                # create dir project
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                date = datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d").date()
                dirp = DirProject.objects.create(name=name, description=description, date=date, creator_id=creator_id)
                pk = dirp.pk
                #create project
                create_ocrfiles(files, username, pk)
                dir_projs = DirProject.objects.filter(pk=pk)
                context = {
                    'dir_projs': dir_projs,
                    'type_choices': type_choices
                }
                messages.success(request, 'The project was created successfully!')
                return JsonResponse({
                    'success': True,
                    'url': request.build_absolute_uri(reverse('index')),
                })
        except:
            messages.error(request, 'Fail to create project')
            return render(request, 'dirprojs/createnew.html', {'form': form})
    return render(request, 'dirprojs/createnew.html', {'form': DirProjForm()})