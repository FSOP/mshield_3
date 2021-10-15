# file: index.py
# pwd  /project/app/main/index.py

from flask import Blueprint, request, render_template, flash, redirect, url_for, send_file
from flask import current_app as app
import os, datetime


main = Blueprint('main', __name__, url_prefix='/')

@main.route('/main', methods=['GET'])
def index():
    test_data = "testdata"

    # /main/index.html is located at /project/app/templates/main/index.html
    return render_template('/main/index.html', test_data=test_data)

@main.route('/list', methods=['GET'])
def list():
    list_dir = os.listdir('../tmp/')
    
    return str(list_dir)

@main.route('/test_down/cve', methods=['GET'])
def test_down():
    # step1. read data
    with open('../tmp/test.txt', 'rb') as fp:
        data = fp.read()

    # 2. extract metadata and binary
    metadata = data.split(b"##databegin##")[0]
    binary = data.split(b"##databegin##")[1]

    # 3. write binary file   
    now = datetime.datetime.strftime(datetime.datetime.now(), "%y%m%d_%H%M")
    fname = "../tmp/{}_cve.exe".format(now)
    with open(fname, "wb") as fp:
        fp.write(binary)
    
    # 4. return file
    fname = fname[3:]
    return send_file(fname, mimetype="application/octet-stream", attachment_filename="test.exe", as_attachment=True)
