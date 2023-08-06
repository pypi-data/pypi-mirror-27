# -*- coding: utf-8 -*-

#  enCompress.py

# Set up time: 2:00 PM IST

import os

import pyminizip



def get_password( cecid ):

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

def enCompress(filePath, fileName, user):

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
    if fileName[0] == "/" || fileName[0] == "//":
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




