from app.tools.interface import *

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

    # 모듈 상단, 메타데이터만 읽음-48+
    data = data.split(b"####databegin####")
    for line in data[0].splitlines():
        # 주석 처리; 맨 앞의 두 문자가 ##인 경우 주석으로 처리
        if line[:2] == b"##":  continue
        tmp = line.split(b":")
        if len(tmp)==1: continue

        module_data[tmp[0].decode()] = tmp[1].strip().decode()

    module_data['title'] = fname
    module_data['content'] = data[1]

    return module_data

def drop_file(module_name, options):
    loc_proc = "/error"
    str_now = datetime.datetime.strftime(datetime.datetime.now(),"%y%m%d_%H%M")
    dict_module_data = read_module(module_name)

    # 1. 선택한 모듈의 정보 읽기
    data = read_module(module_name)
    out_name = "{}_{}".format(str_now, data['title'])

    # 2. 모듈의 타입별로 처리 함수로 전달; 처리 함수는 결과 파일의 위치 반환
    if data['type'] == 'C':
        ## 코드를 넘기면서 옵션 값 삽입 (insert_option)
        loc_proc = drop_file_c(code=insert_option(data['content'], options), out_name=out_name, extension=data['extension'])
    if data['type'] == 'javascript':
        loc_proc = drop_file_javascript(code=insert_option(data['content'], options), out_name=out_name)
    if data['type'] == 'binary':
        loc_proc = drop_file_binary(code=insert_option(data['content'], options), out_name=out_name, extension=data['extension'])

    # 3. 처리 결과 파일의 위치를 반환함
    return loc_proc

# 모듈의 코드에 옵션 값 삽입
def insert_option(code, dict_option):
    res = code
    for opt in dict_option.keys():
        res = res.replace("<{}>".format(opt).encode(), dict_option[opt].encode())

    return res

def drop_file_binary(code, out_name, extension):
    print("DROP binary file")
    fname = NAME_FILE_BINARY.format(out_name)
    if extension != "":
        fname += "."+extension
    with open(LOC_TMP+fname, 'wb') as fp:
        fp.write(code)
    print("DROP Binary File End")
    return fname

def drop_file_javascript(code, out_name):
    print("DROP JAVASCRIPT HTML FILE")
    # 1. save code as html file
    fname = NAME_CODE_HTML.format(out_name)
    with open(LOC_TMP+fname, 'wb') as fp:
        fp.write(code)

    # 2. return file name
    print("DROP JAVASCRIPT HTML END")
    return fname

# C type 파일 읽기
def drop_file_c(code, out_name, extension):
    print("DROP FILE C function called")
    # 1. save code as file
    code_name = NAME_CODE_C.format(out_name)
    with open(LOC_TMP+code_name, 'wb') as fp:
        fp.write(code)

    # 2. compile C code
    compiler = ""
    if extension == "exe":
        compiler = COMPILER_WINDOWS_C
        out_name = out_name + ".exe"

    elif extension == "LINUX":
        compiler = COMPILER_LINUX_C

    command = [compiler, "-o", LOC_TMP+out_name, LOC_TMP+code_name]
    print(command)
    res = subprocess.call(command)

    return out_name


if __name__ == "__main__":
    data = read_module("CVE-2021-36934")
    print(data.keys())
    #drop_file("cve-1234-1234")
