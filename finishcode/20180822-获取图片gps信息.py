def exifread_infos(photo):
    import exifread 
    #加载 ExifRead 第三方库  https://pypi.org/project/ExifRead/
    #获取照片时间、经纬度信息
    #photo参数：照片文件路径
    
    # Open image file for reading (binary mode) 
    f = open(photo, 'rb')
    # Return Exif tags
    tags = exifread.process_file(f)

    try:
        #拍摄时间
        EXIF_Date=tags["EXIF DateTimeOriginal"].printable
        #纬度
        LatRef=tags["GPS GPSLatitudeRef"].printable
        Lat=tags["GPS GPSLatitude"].printable[1:-1].replace(" ","").replace("/",",").split(",")
        Lat=float(Lat[0])+float(Lat[1])/60+float(Lat[2])/float(Lat[3])/3600
        if LatRef != "N":
            Lat=Lat*(-1)
        #经度
        LonRef=tags["GPS GPSLongitudeRef"].printable
        Lon=tags["GPS GPSLongitude"].printable[1:-1].replace(" ","").replace("/",",").split(",")
        Lon=float(Lon[0])+float(Lon[1])/60+float(Lon[2])/float(Lon[3])/3600
        if LonRef!="E":
            Lon=Lon*(-1)
        f.close()
    except :
        return "ERROR:请确保照片包含经纬度等EXIF信息。"
    else:
        return EXIF_Date,Lat,Lon

a=exifread_infos('E:\\日常应用\\照片\\20180821-内蒙古\\IMG_20180819_090802.jpg')
print(a)