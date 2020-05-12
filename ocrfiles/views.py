import sys
import os
import operator
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from functions.save2db import create_ocrfiles, create_validation
from ocrfiles.choices import type_choices
from .models import Ocrfiles, OcrConvertedImage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from validations.models import Validation as validation_models
from dirprojects.models import DirProject
from django.contrib.auth.models import User
from functools import reduce
# from win32com import client


# path = r"C:/Users/LJI006/workspace/Ocr_scanned_files/"
# image_path = r"C:/Users/LJI006/workspace/Ocr_scanned_files/temp_img/"


def validation(request, ocr_id, page_number):
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


def index(request):
    if DirProject.objects.filter(creator_id=request.user.id).exists() and request.user.is_authenticated:
        if 'project_select' in request.GET:
            id = request.GET['project_select']
            dir_projs = DirProject.objects.filter(id=id).first()
        else:
            dir_projs = DirProject.objects.filter(creator_id=request.user.id).latest('id')
    
        dir_select_form = DirProject.objects.filter(creator_id=request.user.id).order_by('id')

        ocr_files = Ocrfiles.objects.filter(dir_project=dir_projs)

        ocr_object = (Q(ocrfiles=ocr_file) for ocr_file in ocr_files)
        converted_image = OcrConvertedImage.objects.filter(reduce(operator.or_, ocr_object)).order_by('page_number').distinct()

        # add paginator
        paginator = Paginator(ocr_files, 12)
        page = request.GET.get('page')
        paged_ocrfiles = paginator.get_page(page)


        context = {
            'ocr_files': paged_ocrfiles,
            'converted_image': converted_image,
            'dir_select_form': dir_select_form,
            'dir_projs': dir_projs
        }
        return render(request, 'ocrfiles/ocrfiles.html', context=context)
    else:
        html = "<h1>Please Create Project Directory or Login to your account</h1>"
        html += "<button onclick='goBack()'>Go Back</button><script>function goBack() {window.history.back();}</script>"
        return HttpResponse(html)

def search(request):
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
