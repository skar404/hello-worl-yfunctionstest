import math
import os
import time
import shutil
import requests
from pip._internal.utils.misc import get_installed_distributions

DATE_START = time.time()


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def handler(event, context):
    req = requests.get('https://sputnik.bot.assa.dev/backend/ping')
    total, used, free = shutil.disk_usage("/tmp/")

    fs_info = 'Not error'
    try:
        with open('/tmp/file.tmp', "wb") as f:
            f.seek(10*1024**2)
            f.write(b"\0")
    except OSError as e:
        fs_info = e.strerror

    return {
        'statusCode': 408,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'isBase64Encoded': False,
        'body': {
            "FS": fs_info,
            "time": {
                'dif': time.time() - DATE_START,
                'start': DATE_START,
            },
            "disk_usage": {
                "total": convert_size(total),
                "use": convert_size(used),
                "free": convert_size(free)
            },
            "req": {
                "json": req.json(),
                "code": req.status_code
            },
            "lib": {i.key: i.version for i in get_installed_distributions()},
        },
    }
