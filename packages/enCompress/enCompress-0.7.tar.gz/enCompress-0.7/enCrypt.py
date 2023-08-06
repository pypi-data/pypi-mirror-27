# -*- coding: utf-8 -*-

#  enCompress.py

# Set up time: 2:00 PM IST

import os

import pyminizip
import json
import urllib.request

def get_password( cecid ):

    pswd = cecid[0] + cecid[:1] + get_cec_empId(cecid)

    return pswd

def encrypt_file(iFile, oFile, cecId):

    compression_level = 5

    try:
        pyminizip.compress(iFile, oFile, get_password(cecId), compression_level)
        return 0
    except Exception as e:
        print("Exception occured ... \n\n",e)
        return -1

def get_cec_empId(cecid):
    weburl = urllib.request.urlopen("http://directory.cisco.com/dir/details-json/"+cecid)
    data = weburl.read()

    if (data != b'$employee.toJSONObject()\n' and data != b'$employee.toJSONObject()\r\n'):
        encoding = weburl.info().get_content_charset('utf-8')
        datar=json.loads(data.decode(encoding))
        if 'eid' in datar:
            empId = datar['eid']
            return empId

def encodeFile(filePath, fileName, user):

    if not filePath:
        print("Please specify the input file ...")
        usage()
        return -1
    if not fileName:
        print("Please specify the output file ...")
        usage()
        return -1

    if not user:
        print("Please specify the cec user id...")
        usage()
        return -1

    # Check if file name starts with /
    if fileName[0] == "/" or fileName[0] == "//":
        print("Please provide only relative paths in file names.")
        return -1

    # Check if path exists
    if os.path.exists(filePath):
        # Check if path is a directory
        if os.path.isdir(filePath):

            # Check if directory is writeable
            if os.access(filePath, os.W_OK) is not True:
                print("Input file path directory is not writeable ")
                return -1

            file = filePath + "/" + fileName
            base = os.path.basename(fileName)

            oFile = filePath + "/" + os.path.splitext(base)[0] + ".zip"

            # Check if file exists
            if os.path.exists(file):
                if  os.access(file, os.R_OK) is not True:
                    print(" Input file is not readable")
                    return -1
                return encrypt_file(file, oFile , user)

            else:
                print("Input file does not exists ")
                return -1
        else:
            print("Input file path is not a directory")
            return -1
    else:
        print("Input file path directory does not exists")
        return -1



