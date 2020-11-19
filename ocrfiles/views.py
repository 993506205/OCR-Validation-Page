import sys
import os
import operator
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from functions import emptyDirClean
from functions.save2db import create_ocrfiles, create_validation
from ocrfiles.choices import type_choices
from .models import Ocrfiles, OcrConvertedImage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.urls import reverse
from validations.models import Validation as validation_models
from dirprojects.models import DirProject
from django.contrib.auth.models import User
from functools import reduce
from django.contrib import messages

def index(request):
    # check if login
    if not request.user.is_authenticated:
        messages.info(request, 'Please login first!')
        return render(request, 'accounts/login.html')
    # check if has Directory Project
    if not DirProject.objects.filter(creator_id=request.user.id).exists():
        messages.info(request, 'Please create one Directory Project!')
        return redirect('index')
    
    dir_projs = DirProject.objects.filter(creator_id=request.user.id).latest('id')
    if 'project_select' in request.GET:
        id = request.GET['project_select']
        dir_projs = DirProject.objects.filter(id=id).first()
        
    # else:
    #     dir_projs = DirProject.objects.filter(creator_id=request.user.id).latest('id')

    dir_select_form = DirProject.objects.filter(creator_id=request.user.id).order_by('id')
    ocr_files = Ocrfiles.objects.filter(dir_project=dir_projs)
    ocr_object = (Q(ocrfiles=ocr_file) for ocr_file in ocr_files)
    converted_image = OcrConvertedImage.objects.filter(reduce(operator.or_, ocr_object)).order_by('page_number').distinct()
    # add paginator
    paginator = Paginator(ocr_files, 12)
    page = request.GET.get('page')
    paged_ocrfiles = paginator.get_page(page)
    
    if request.method == 'DELETE':
        data = json.loads(request.body)
        func_type = data['type']
        if func_type == "delete":
            #delete file
            deleteFile(request,data['file_id'])
    
    context = {
        'ocr_files': paged_ocrfiles,
        'converted_image': converted_image,
        'dir_select_form': dir_select_form,
        'dir_projs': dir_projs
    }
    return render(request, 'ocrfiles/ocrfiles.html', context=context)

def search(request):
    # check if login
    if not request.user.is_authenticated:
        messages.info(request, 'Please login first!')
        return render(request, 'accounts/login.html')
    # check if has Directory Project
    if not DirProject.objects.filter(creator_id=request.user.id).exists():
        messages.info(request, 'Please create one Directory Project!')
        return redirect('index')
    
    ocr_files = Ocrfiles.objects.all()
    converted_image = OcrConvertedImage.objects.all()
    current_user = request.user
    
    dir_projs = DirProject.objects.filter(creator_id=current_user.id)

    # directory project
    if 'dirProj' in request.GET:
        dirProj_id = request.GET['dirProj']
        if dirProj_id:
            ocr_files = ocr_files.filter(dir_project=dirProj_id)

    # file name
    if 'fileName' in request.GET:
        fileName = request.GET['fileName']
        if fileName:
            ocr_files = ocr_files.filter(file_name__icontains=fileName)

    # file type
    if 'fileType' in request.GET:
        fileType = request.GET['fileType']
        if fileType == 'pdf':
            ocr_files = ocr_files.filter(file_extension__iexact='pdf')
        elif fileType == 'img':
            ocr_files = ocr_files.filter(Q(file_extension__iexact='png') | Q(
                file_extension__iexact='jpg') | Q(file_extension__iexact='jpeg'))

    if request.method == 'DELETE':
        data = json.loads(request.body)
        func_type = data['type']
        if func_type == "delete":
            #delete file
            deleteFile(request,data['file_id'])
            
    
    # add paginator
    paginator = Paginator(ocr_files, 6)
    page = request.GET.get('page')
    paged_ocrfiles = paginator.get_page(page)
    context = {
        'type_choices': type_choices,
        'ocr_files': paged_ocrfiles,
        'converted_image': converted_image,
        'request_value': request.GET,
        'dir_projs': dir_projs,
    }
    return render(request, 'ocrfiles/search.html', context)

def validation(request, ocr_id, page_number):
    # check if login
    if not request.user.is_authenticated:
        messages.info(request, 'Please login first!')
        return render(request, 'accounts/login.html')
    # check if has Directory Project
    if not DirProject.objects.filter(creator_id=request.user.id).exists():
        messages.info(request, 'Please create one Directory Project!')
        return redirect('index')
    
    # update changed text
    if request.method == 'POST':
        data = json.loads(request.body)
        validation_models.objects.filter(id=data['validation_id']).update(get_text=data['changedValue'])

    ocr_files = get_object_or_404(Ocrfiles, pk=ocr_id)

    converted_image = OcrConvertedImage.objects.filter(
        ocrfiles=ocr_files, page_number=page_number)

    create_validation(ocr_files, page_number)
    
    validation_text = validation_models.objects.filter(ocrfiles=ocr_files, page_number=page_number)
    text_len = len(validation_text)
    context = {
        'ocr_id': ocr_id,
        'ocr_file': ocr_files,
        'converted_image': converted_image,
        'page_number': page_number,
        'validation_text': validation_text,
        'text_len':text_len,
    }
    return render(request, 'ocrfiles/validation.html', context=context)

def deleteFile(request, file_id):
    try:
        file_delete = get_object_or_404(Ocrfiles, id=file_id)
        #converted_file_delete = get_object_or_404(OcrConvertedImage, ocrfiles=file_delete)
        #converted_file_delete.delete()
        file_delete.delete()

        # clean empty dirs
        emptyDirClean.deleteDirs()
    except Exception as e:
        print("delete error: ")
        print(e)
        
def addNew(request, dirprj_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            files = [request.FILES.get('file[%d]' % i)
            for i in range(0, len(request.FILES))]
            try:
                #create project
                if request.user.is_authenticated:
                    username = request.user.username
                create_ocrfiles(files, username, dirprj_id)
                return JsonResponse({
                    'success': True,
                    'url': request.build_absolute_uri(reverse('ocrfiles')) + "?project_select="+str(dirprj_id),
                })
            except Exception as e:
                print("add new error: ")
                print(e)
    