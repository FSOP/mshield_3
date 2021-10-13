# file: index.py
# pwd  /project/app/main/index.py

from flask import Blueprint, request, render_template, flash, redirect, url_for, send_file
from flask import current_app as app
from app.tools.tool_base import get_module_list, read_module, drop_file_c
from app.tools.interface import *

import os, datetime


bp = Blueprint('test', __name__, url_prefix='/test')


@bp.route('/', methods=['GET'])
def list():
    list_module = get_module_list()
    
    return render_template('/list_module.html', list_modules=list_module)


@bp.route('/get_module/<title>', methods=['GET'])
def test_down(title):
    module = read_module(title)




    return module['content'].decode()