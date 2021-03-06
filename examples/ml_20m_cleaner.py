#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-06-19
# @Filename: cleaner.py
# @Last modified by:   archer
# @Last modified time: 2018-08-07
# @License: Please see LICENSE file in project root



import csv, sys, os, argparse
import pandas as pd
import numpy as np

from fnmatch import fnmatch # file matching


# this is the default file called for cleaning, modify this to you're needs,
# or pass call ravenRecSyst with -c argument and specify path to whatever
# cleaning file you have created
def clean(chunk):

    # cleaning code goes here!!!!

    # This should be able to clean on "chunks" which
    # could be portions of files. These chunks are used to ensure that
    # memory usage does not exceed availiable memory

    # some operations on chunks, whatever you want to clean up
    # chunk = chunk.dropna(axis='rows')


    return chunk



def main(args):

    # the neccessary arguments are passed to main through "args"
    # you can see each availiable argument in the argz function below
    # to use one of these arguments call it using args["cleaner"]
    # once you have cleaned the files (or not) they will be automagically
    # added to mongodb

    path = os.path.abspath(args["newData"])
    chunkSize = args["chunkSize"]
    suffix = args["suffix"]

    if(os.path.isfile(path)):
        filePaths = [path]
        folderPath, file = os.path.split(path)

    elif(os.path.isdir(path)):
        filePaths = []
        pattern = "*.csv"
        folderPath = path
        # since path points to folder, find all matching files in subdirs
        for path_t, subdirs, files in os.walk(path):
            for name in files:
                # if file name matches a pattern
                if fnmatch(name, pattern):
                    filePath = os.path.join(path_t, name)
                    filePaths.append(filePath)

    else:
        filePaths = []
        raise ValueError(str("Could not find valid files using path: " + path))

    print("clearing any previous '" + suffix + "' files in: " + folderPath)
    clearFiles(folderPath, pattern=str("*" + suffix))
    print("generating '" + suffix + "' documents in: " + folderPath)

    for filePath in filePaths:

        destFilePath = str(filePath + suffix)
        for chunk in pd.read_csv(filePath, chunksize=chunkSize):
            chunk = clean(chunk)
            writeToFile(df=chunk, filePath=destFilePath)



def clearFiles(path_t, pattern="*.data"):

    if(os.path.isfile(path_t)):
        os.remove(path_t)

    elif(os.path.isdir(path_t)):
        for path, subdirs, files in os.walk(path_t):
            for name in files:
                if fnmatch(name, pattern):
                    filePath = os.path.join(path, name)
                    os.remove(filePath)



def writeToFile(df, filePath):

    if(os.path.isfile(filePath) == False):
        df.to_csv(filePath, mode='w', header=True,  index=False)
        # print("Write: ", filePath)

    else:
        df.to_csv(filePath, mode='a', header=False, index=False)
        # print("Append: " + filePath)



def argz(argv, description=None):
    if(description == None):
        description = "MongoDb related args"

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-c", "--cleaner",      default="",     required=True,
        help="file inclusive path to cleaner file, for data specific cleaning, should also specify --newData")
    parser.add_argument("-d", "--newData",      default="",     required=True,
        help="the directory or file of the new data to be added and cleaned, should also specify --cleaner")
    parser.add_argument("--suffix",             default=".data", required=False,
        help="suffix to be appended to generated cleaned data files")
    parser.add_argument("--chunkSize",         default=10**8,   required=False,
        help="sets the size in rows of csv to be read in as chunks", type=int)
    parser.add_argument("--timeSteps",         default=30,      required=True,
        help="sets the length of timesteps to use. E.G 30 for 30 rows long", type=int)

    return vars(parser.parse_args(argv))



# setting up to make things nice
cleanerName = os.path.basename(os.path.abspath(sys.argv[0]))
prePend = "[ " + cleanerName + " ] "

description = str("cleaner file for adaptation to users needs, " +
              "these files deal with data cleaning")

args = argz(sys.argv[1:], description=description)

try:
    main(args=args)
except:
    print(prePend + "could not clean data:\n" +
        str(sys.exc_info()[0]) + " " +
        str(sys.exc_info()[1])
        )
