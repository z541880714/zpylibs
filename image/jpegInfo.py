# encoding=utf-8
import sys
import os
import exifread
import re
from datetime import datetime
import requests


def get_city_from_gps(_longitude, _latitude):
    url = "https://restapi.amap.com/v3/geocode/regeo?key=6169f44183f51488a26aa0302e868b9c&location={},{}".format(
        _longitude, _latitude)
    print('url:', url)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chro'
                      'me/53.0.2785.104 Safari/537.36 Core/1.53.2372.400 QQBrowser/9.5.10548.400'
    }
    r = requests.get(url, headers=headers)
    print("response :", r.text)


# 高德  key 名称:pyHttp;  key:6169f44183f51488a26aa0302e868b9c
# url: https://restapi.amap.com/v3/geocode/regeo?key=6169f44183f51488a26aa0302e868b9c&location=116.310003,39.991957
def get_exif_datetime(img_path):
    global longitude
    pass
    with open(img_path, 'rb') as f:
        tags = exifread.process_file(f)
    key_list = ['Image DateTime', 'EXIF DateTimeOriginal', 'EXIF DateTimeDigitized']
    ret_datetime = None
    for key in key_list:
        if not tags.__contains__(key):
            continue
        datetime_str = str(tags[key])
        # print(datetime_str)
        pattern = r'^(\d+):(\d+):(\d+) (\d+):(\d+):(\d+)$'
        ret = re.match(pattern, datetime_str.strip(), re.I)
        if ret is None:
            continue
        # print("regix ret:", ret.groups())
        ret_groups = ret.groups()
        ret_datetime = datetime(int(ret_groups[0]), int(ret_groups[1]), int(ret_groups[2]),
                                int(ret_groups[3]), int(ret_groups[4]), int(ret_groups[5]))
        break

    def analyze_coordination(_key):
        content = str(tags[_key])
        _ret = re.match(r'^\[(\d+), (\d+),.*]$', content.strip(), re.I)
        return float(_ret.group(1)) + float(_ret.group(2)) / 60

    longitude, latitude = 0, 0
    if tags.__contains__('GPS GPSLongitude'):
        longitude = analyze_coordination('GPS GPSLongitude')

    if tags.__contains__('GPS GPSLatitude'):
        latitude = analyze_coordination('GPS GPSLatitude')
    coord_info = None if longitude * latitude == 0 else (longitude, latitude)
    get_city_from_gps(longitude, latitude)
    return ret_datetime, coord_info


def main(img_path):
    if os.path.isdir(img_path):
        err_list = []
        no_jpeg_count = 0
        for root, dirs, files in os.walk(img_path):
            for f_path in files:
                _path = os.path.join(root, f_path)
                if not _path.endswith('.jpeg'):
                    no_jpeg_count += 1
                    continue
                ret_datetime, ret_coord = get_exif_datetime(_path)
                if ret_datetime is None:
                    err_list.append(_path)
        print("\n".join(err_list))
        print("No. of JPEG Images: {}".format(no_jpeg_count))
    elif os.path.isfile(img_path):
        _datetime, coord = get_exif_datetime(img_path)
        print("datetime:", _datetime, " gps:", coord)
    else:
        print("image path not exist...")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
