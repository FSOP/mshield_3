# file: index.py
# pwd  /project/app/main/index.py

from flask import Blueprint, request, render_template, flash, redirect, url_for, send_file
from flask import current_app as app
from app.tools.tool_base import get_module_list, read_module, drop_file
from app.tools.interface import *

import os, datetime


bp = Blueprint('test', __name__, url_prefix='/test')


@bp.route('/', methods=['GET'])
def list():
    list_module = get_module_list()
    
    return render_template('/list_module.html', list_modules=list_module)


@bp.route('/get_module/<title>/', methods=['POST'])
def down(title):
    out_file = drop_file(title, request.form.to_dict())

    return send_file(LOC_TMP+out_file, mimetype="application/octet-stream", attachment_filename=out_file, as_attachment=True)


@bp.route('/option_module/<title>/', methods=['GET'])
def option_module(title):
    option = []
    module = read_module(title)

    return render_template('/option_module.html', options=module['options'].split(","), title=module['title'])


# view raw module
@bp.route('/view_raw/<title>/', methods=['GET'])
def view_module(title):
    data = ""
    fpath = BASE+"/modules/{}".format(title)
    meta = read_module(title)

    with open(fpath, 'rb') as fp:
        data = fp.read()
        if meta['type'] == "binary":
            data = data.split(b"####databegin####")[0]
            data += b"\n\n !! binary contents are not shown !! "
    return "<textarea cols=100 rows=40>" +data.decode() + "</textarea>"


# 다운로드 테스트
@bp.route('/<filename>/', methods=['GET'])
def test_down(filename):

    return send_file(LOC_TMP+filename, mimetype="application/octet-stream", attachment_filename="test.zip", as_attachment=True)