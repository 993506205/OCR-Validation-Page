from django.shortcuts import render
from ocrfiles.choices import type_choices
from dirprojects.models import DirProject


def index(request):
    current_user = request.user
    
    dir_projs = DirProject.objects.filter(creator_id=current_user.id)
    context = {
        'dir_projs': dir_projs,
        'type_choices': type_choices
    }
    return render(request, 'pages/index.html', context)


def about(request):
    return render(request, 'pages/about.html')
