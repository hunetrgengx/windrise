from PIL import Image
from PIL.ExifTags import TAGS
def get_exif_data(fname):
    """Get embedded EXIF data from image file."""
    ret = {}
    try:
        img = Image.open(fname)
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
    except IOError:
        print('IOERROR ' + fname)
    return ret

if __name__ == '__main__':
    fileName = 'E:\\日常应用\\照片\\20180821-内蒙古\\IMG_20180819_180213.jpg'
    exif = get_exif_data(fileName)
    print(exif)