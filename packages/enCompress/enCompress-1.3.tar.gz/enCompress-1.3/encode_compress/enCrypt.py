#!/auto/vgapps-cstg02-vapps/csap/python/bin/python3
# -*- coding: utf-8 -*-

#  /auto/vgapps-cstg02-vapps/csap/python/bin/python3 encryptFile.py

# Set up time: 2:00 PM IST

import argparse
import os

import pyminizip


def usage():
    print("encryptFile.py -filePath <filePath> -fileName <fileName> -user <cecid>")
    exit()

def parse_options():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("--filePath",
                        default='',
                        help='Input File path',
                        type=str,
                        metavar='en')
    parser.add_argument("--fileName",
                        default='',
                        help='Input File Name',
                        type=str,
                        metavar='en')
    parser.add_argument("--user",
                        default='',
                        help='Users CEC Id',
                        type=str,
                        metavar='en')
    args = parser.parse_args()
    return args

def get_password( cecid ):

    empId = 201595
    pswd = cecid[0] + cecid[:1] + empId

    return pswd

def encrypt_file(iFile, oFile, cecId):

    compression_level = 5

    try:
        pyminizip.compress(iFile, oFile, get_password(cecId), compression_level)
        return 0
    except Exception as e:
        print("Exception occured ... \n\n",e)
        return -1

def main():
    options = parse_options()

    if not options.filePath:
        print("Please specify the input file ...")
        usage()
        exit(-1)
    if not options.fileName:
        print("Please specify the output file ...")
        usage()
        exit(-1)

    if not options.user:
        print("Please specify the cec user id...")
        usage()
        exit(-1)

    # Check if file name starts with /
    if fileName[0] == "/" or fileName[0] == "//":
        print("Please provide only relative paths in file names.")
        exit(-1)

    # Check if path exists
    if os.path.exists(filePath):
        # Check if path is a directory
        if os.path.isdir(filePath):

            # Check if directory is writeable
            if os.access(filePath, os.W_OK) is not True:
                print("Input file path directory is not writeable ")
                exit(-1)

            file = filePath + "/" + fileName
            base = os.path.basename(fileName)

            oFile = filePath + "/" + os.path.splitext(base)[0] + ".zip"

            # Check if file exists
            if os.path.exists(file):
                if  os.access(file, os.R_OK) is not True:
                    print(" Input file is not readable")
                    exit(-1)
                encrypt_file(file, oFile , options.user)
            else:
                print("Input file does not exists ")
                exit(-1)
        else:
            print("Input file path is not a directory")
            exit(-1)
    else:
        print("Input file path directory does not exists")
        exit(-1)

if __name__ == "__main__":
    main()



