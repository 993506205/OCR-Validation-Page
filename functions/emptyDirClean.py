import os, sys
from django.conf import settings

def deleteDirs():
    media_path = settings.MEDIA_ROOT
    for root, dirs, files in os.walk(media_path, topdown=False):
        for name in dirs:
            try:
                if len(os.listdir( os.path.join(root, name) )) == 0: #check whether the directory is empty
                    try:
                        os.rmdir( os.path.join(root, name) )
                    except:
                        print( "FAILED :", os.path.join(root, name) )
                        pass
            except:
                pass