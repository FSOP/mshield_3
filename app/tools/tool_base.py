from app.tools.interface import *
from datetime import datetime
import os, subprocess, datetime

def get_module_list():
    list_dir = os.listdir(LOC_MODULES)
    list_module = []

    for file in list_dir:
        # print(LOC_MODULES+file)
        list_module.append(read_module(file))

    return list_module

# 모듈의 메타데이터만 읽어서 반환하는 함수; 반환형식: dictionary
def read_module(fname):
    module_data = {}
    fpath = LOC_MODULES + fname
    with open(fpath, 'rb') as fp:
        data = fp.read()

    # 모듈 상단, 메타데이터만 읽음
    data = data.split(b"##databegin##")
    for line in data[0].splitlines():
        # 주석 처리; 맨 앞의 두 문자가 ##인 경우 주석으로 처리
        if line[:2] == b"##":  continue
        tmp = line.split(b":")
        if len(tmp)==1: continue

        module_data[tmp[0].decode()] = tmp[1].strip().decode()

    module_data['title'] = fname
    module_data['content'] = data[1]

    return module_data

def drop_file(module_name):
    loc_proc = ""
    dict_module_data = read_module(module_name)

    drop_file_c()



def drop_file_c(code, name, out_name):
    # 1. save code as file
    code_name = NAME_CODE_C.format(datetime.strftime(datetime.now(),"%y%m%d_%H%M"), name)

    with open(LOC_TMP+code_name, 'wb') as fp:
        fp.write(code)

    # 2. compile C code
    command = ["gcc", "-o", out_name, LOC_TMP+code_name]
    res = subprocess.call(command)

    print(res)

    return res

