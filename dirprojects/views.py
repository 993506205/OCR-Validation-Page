from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DirProjForm
from django.http import HttpResponseRedirect
from functions.save2db import create_ocrfiles
from datetime import datetime
from .models import DirProject
from django.urls import reverse


def prj_create(request):
    if request.method == "POST":
        form = DirProjForm(request.POST)
        files = [request.FILES.get('file[%d]' % i)
        for i in range(0, len(request.FILES))]
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
            dirp, created = DirProject.objects.get_or_create(
                name=name,
                description=description,
                creator_id=creator_id,
                date=date,
            )
            pk = dirp.pk
            
            #create project
            create_ocrfiles(files, username, pk)    
            messages.success(request, 'The project was created successfully!')
            return redirect(reverse('index'))
        return render(request, 'dirprojs/createnew.html', {'form': form})
    return render(request, 'dirprojs/createnew.html', {'form': DirProjForm()})