import os
import stat
import uuid

from flask import current_app
from werkzeug.utils import secure_filename

from app.models import db
from app.libs.utils import date_to_str
from app.models import Image


def upload_file(file):
    config_upload = current_app.config['UPLOAD']
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    filename = file.filename
    ext = filename.rsplit(".", 1)[1]
    # if ext not in config_upload['ext']:
    #     resp['code'] = -1
    #     resp['msg'] = "不允许的扩展类型文件"
    #     return resp
    root_path = current_app.root_path + config_upload['prefix_url']
    file_dir = date_to_str(format="%Y%m%d")
    save_dir = root_path + file_dir
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
        os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)

    file_name = str(uuid.uuid4()).replace("-", "") + "." + ext
    file.save("{0}/{1}".format(save_dir, file_name))

    with db.auto_commit():
        model_image = Image()
        model_image.file_key = file_dir + "/" + file_name
        db.session.add(model_image)

    resp['data'] = {
        'file_key': model_image.file_key
    }
    return resp
