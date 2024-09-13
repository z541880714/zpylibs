# encoding=utf-8
import sys
import os
import exifread
import re
from datetime import datetime


def get_exif_datetime(img_path):
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
                                int(ret_groups[3]),
                                int(ret_groups[4]), int(ret_groups[5]))
        break
    return ret_datetime


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
                ret_datetime = get_exif_datetime(_path)
                if ret_datetime is None:
                    err_list.append(_path)
        print("\n".join(err_list))
        print("No. of JPEG Images: {}".format(no_jpeg_count))
    elif os.path.isfile(img_path):
        ret = get_exif_datetime(img_path)
        # print("datetime:", ret)
    else:
        print("image path not exist...")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
