import os
import sys
from io import BytesIO
import fitz
import shutil
from datetime import datetime
from PIL import Image
from django.core.files import File
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from dirprojects.models import DirProject
from . import tesseract_ocr, emptyDirClean
from ocrfiles.models import Ocrfiles, OcrConvertedImage
from validations.models import Validation
from . import emptyDirClean

# insert files properties into db
def create_ocrfiles(file_list, username, pk):
    now = datetime.now()
    # Change date format for db
    current = datetime.strptime(
        now.strftime("%Y-%m-%d"), "%Y-%m-%d").date()
    Ocr_save_img = OcrConvertedImage()
    Ocr_save_file = Ocrfiles()

    dir_id = str(pk)

    dirproject_obj = DirProject.objects.get(pk=pk)
    dir_name = dirproject_obj.name

    for f in file_list:
        f_name = f.name
        f_ext = f_name.split('.')[1].lower()
        f_size = f.size

        Ocr_save_file, created = Ocrfiles.objects.get_or_create(
            file_name=f_name,
            dir_project=dirproject_obj,)
        # if file_name is not existing and created
        if created:
            # Ocr_save_file = Ocrfiles.objects.filter(
                # file_name=f_name).first()
            try:
                Ocr_save_file.scanned_file.save(
                    f_name, File(f))
                new_path = os.path.join(settings.MEDIA_ROOT, "Ocr_Scanned_files", dir_name, dir_id, f_name)
                os.makedirs(os.path.join(settings.MEDIA_ROOT, "Ocr_Scanned_files", dir_name, dir_id), exist_ok=True)
                os.rename(Ocr_save_file.scanned_file.path, new_path)
                Ocr_save_file = Ocrfiles(id=Ocr_save_file.id, file_name=f_name, file_extension=f_ext, file_size=f_size, upload_date=current,scanned_file_url=str(os.path.join("Ocr_Scanned_files", dir_name, dir_id, f_name)), scanned_file=new_path, dir_project=dirproject_obj)
                # Ocr_save_file.scanned_file.name = os.path.join("Ocr_Scanned_files", dir_name, dir_id, f_name)
                Ocr_save_file.save()
            except Exception as e:
                print(str(e))
        else:
            try:
                f_name = f_name.split('.')[0] + now.strftime("%Y%m%d%H%M%S") + "." + f_ext
                Ocr_save_file, created = Ocrfiles.objects.get_or_create(
                    file_name=f_name,
                    dir_project=dirproject_obj,)
                Ocr_save_file.scanned_file.save(
                    f_name, File(f))
                new_path = os.path.join(settings.MEDIA_ROOT, "Ocr_Scanned_files", dir_name, dir_id, f_name)
                os.makedirs(os.path.join(settings.MEDIA_ROOT, "Ocr_Scanned_files", dir_name, dir_id), exist_ok=True)
                os.rename(Ocr_save_file.scanned_file.path, new_path)
                Ocr_save_file = Ocrfiles(id=Ocr_save_file.id, file_name=f_name, file_extension=f_ext, file_size=f_size, upload_date=current,scanned_file_url=str(os.path.join("Ocr_Scanned_files", dir_name, dir_id, f_name)), scanned_file=new_path, dir_project=dirproject_obj)
                # Ocr_save_file.scanned_file.name = os.path.join("Ocr_Scanned_files", dir_name, dir_id, f_name)
                Ocr_save_file.save()
            except Exception as e:
                print(str(e))

        # get just created row of ocr_files
        ocrObject = Ocr_save_file

        ocr_path = ocrObject.scanned_file.path
        # if file extention is pdf
        if f_ext == 'pdf':
            # convert pdf to images and save to dir and return new image path
            pdf2img(f_name, ocr_path, ocrObject, dir_name, dir_id)

        # if extention is image's extention
        elif f_ext == 'jpg' or f_ext == 'jpeg' or f_ext == 'png':
            # save image to db
            # set forigen key for converted_img
            Ocr_save_img = OcrConvertedImage()
            Ocr_save_img.image.save(f_name, File(f))

            new_path = os.path.join(settings.MEDIA_ROOT, "Ocr_Converted_files", dir_name, dir_id, f_name)
            os.makedirs(os.path.join(settings.MEDIA_ROOT, "Ocr_Converted_files", dir_name, dir_id), exist_ok=True)
            os.rename(Ocr_save_img.image.path, new_path)
            Ocr_save_img = OcrConvertedImage(
                id=Ocr_save_img.id, image_name=f_name, ocrfiles=ocrObject, page_number=1,image_url=str(os.path.join("Ocr_Converted_files", dir_name, dir_id, f_name)), image=new_path)
            # Ocr_save_img.image.name = os.path.join("Ocr_Converted_files", dir_name, dir_id, f_name)
            Ocr_save_img.save()

    # Delete empty dirs after save to models
    emptyDirClean.deleteDirs()

# Convert pdf file to img file(s)


def pdf2img(file_name, ocr_path, ocrObject, dir_name, dir_id):
    pdf_file = fitz.Document(ocr_path)
    pdf_name = file_name
    temp_path = settings.MEDIA_ROOT + r"/temp"
    
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
    os.makedirs(temp_path)
    for pg in range(pdf_file.pageCount):
        page = pdf_file[pg]
        rotate = int(0)
        zoom_x = 2  # (2-->1584*1224)
        zoom_y = 2
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        page_num = pg + 1
        f_name = '{0}_{1}.png'.format(pdf_name.split('.')[0], page_num)

        pix.writePNG(temp_path + "/" + f_name)
        pix = None
        # save image to db
        # set forigen key for converted_img
        with open(temp_path + "/" + f_name, 'rb') as f_save:
            Ocr_save_img = OcrConvertedImage()
            Ocr_save_img.image.save(
                f_name, File(f_save))

            new_path = os.path.join(settings.MEDIA_ROOT, "Ocr_Converted_files", dir_name, dir_id, f_name)
            os.makedirs(os.path.join(settings.MEDIA_ROOT, "Ocr_Converted_files", dir_name, dir_id), exist_ok=True)
            os.rename(Ocr_save_img.image.path, new_path)
            Ocr_save_img = OcrConvertedImage(
                id=Ocr_save_img.id, image_name=f_name, ocrfiles=ocrObject, page_number=page_num,image_url=str(os.path.join("Ocr_Converted_files", dir_name, dir_id, f_name)), image=new_path)
            # Ocr_save_img.image.name =  os.path.join("Ocr_Converted_files", dir_name, dir_id, f_name)
            Ocr_save_img.save()
        f_save.closed
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)




def create_validation(ocrfileObj, pageNumber):
    validation_obj = Validation()
    validation_obj = Validation.objects.filter(
        ocrfiles=ocrfileObj, page_number=pageNumber, is_exist=True).first()
    if validation_obj is None:
        converted_img = OcrConvertedImage.objects.filter(ocrfiles=ocrfileObj, page_number=pageNumber).first()
        t_ocr = tesseract_ocr.Tesseract_ocr(img_path=converted_img.image.path, preprocess='thresh', min_confidence=0.4)
        results = []
        results = t_ocr.start_ocr()

        all_endY = []
        all_startY = []
        all_endX = []
        all_startX = []

        for ((startX, startY, endX, endY), text) in results:
            if text == "" and text.isspace():
                continue
            else:
                v = Validation(ocrfiles=ocrfileObj, page_number=pageNumber, get_text=text, startX=startX, endX=endX, startY=startY, endY=endY,
                correction_rate=0, is_correct=False, feedback_text='', is_exist=True)
                v.save()
                all_endY.append(endY)
                all_startY.append(startY)
                all_endX.append(endX)
                all_startX.append(startX)
        
        
        # Crop image
        text_image = Image.open(converted_img.image.path)
        # convert RGBA image to RGB type avoid crop error
        text_rgb_image = text_image.convert('RGB')
        origW, origH = text_rgb_image.size
        # get file name
        f_name = converted_img.image_name

        if not all_endY or not all_startY or not all_endX or not all_startX:
            crop_height_b = origH
            crop_height_t = 0
            crop_width_r = origW
            crop_width_l = 0
        else:
            crop_height_b = max(all_endY)  * origH
            crop_height_t = min(all_startY) * origH
            crop_width_r = max(all_endX) * origW
            crop_width_l = min(all_startX) * origW
            
        crop_height = crop_height_b - crop_height_t
        crop_width = crop_width_r - crop_width_l

        if crop_height < 150:
            crop_height = 150
            crop_height_b = crop_height + crop_height_t

        crop_image = text_rgb_image.crop((crop_width_l, crop_height_t, crop_width_r, crop_height_b))

        for v in Validation.objects.filter(ocrfiles=ocrfileObj, page_number=pageNumber):
            startY = v.startY
            endY = v.endY
            startX = v.startX
            endX = v.endX

            v.startY = (origH * startY - crop_height_t) / crop_height
            v.endY = (origH * endY - crop_height_t) / crop_height
            v.startX = (origW * startX - crop_width_l) / crop_width
            v.endX = (origW * endX - crop_width_l) / crop_width
            v.save()

        # Create a file-like object to write crop_image data (crop_image data previously created
        # using PIL, and stored in variable 'crop_image')
        crop_image_io = BytesIO()
        crop_image.save(crop_image_io, format='JPEG')
        crop_image_io.seek(0)
        
        # Create a new Django file-like object to be used in models as ImageField using
        # InMemoryUploadedFile.  If you look at the source in Django, a
        # SimpleUploadedFile is essentially instantiated similarly to what is shown here
        crop_file = InMemoryUploadedFile(crop_image_io, 'ImageField', f_name, 'image/jpeg',
                                        sys.getsizeof(crop_image_io), None)

        # Get Dir Project by ocrfileObj
        dirproject_obj = ocrfileObj.dir_project
        dir_name = dirproject_obj.name
        dir_id = dirproject_obj.id
        converted_img.textRegion_image.save(
            f_name, File(crop_file))
        f_name = converted_img.image_name
        new_path = os.path.join(settings.MEDIA_ROOT, "Ocr_TextRegion_images", dir_name, str(dir_id), f_name)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, "Ocr_TextRegion_images", dir_name, str(dir_id)), exist_ok=True) 
        os.rename(converted_img.textRegion_image.path, new_path)
        # converted_img.textRegion_image.name =  os.path.join("Ocr_TextRegion_images", dir_name, str(dir_id), f_name)
        converted_img.textRegion_image_url = str(os.path.join("Ocr_TextRegion_images", dir_name, str(dir_id), f_name))
        converted_img.save()

    temp_path = os.path.abspath(os.getcwd()) + r"/temp"
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
    emptyDirClean.deleteDirs()
