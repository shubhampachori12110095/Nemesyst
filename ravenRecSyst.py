#!/usr/bin/env python3
# @Author: George Onoufriou <georgeraven>
# @Date:   2018-05-16
# @Filename: app.py
# @Last modified by:   archer
# @Last modified time: 2018-06-14
# @License: Please see LICENSE file in project root



import os, sys, json, inspect
from src.helpers import argz, installer, updater
from src.log import Log



def main():

    # imported here to allow for update first
    from RavenPythonLib.mongodb.mongo import Mongo
    mongodb = Mongo(isDebug=True, mongoUser=args['user'], mongoPath=args['dir'],
        mongoPass=args['pass'], mongoIp=args['ip'], mongoDbName=args['name'],
        mongoCollName="cycles", mongoPort=args['port'], mongoUrl=args['url'])

    mongodb.debug(print=print) # passing in print to use logger
    mongodb.start(print=print)
    mongodb.addUser(print=print)
    mongodb.stop(print=print)

##### testing above first

    print("Sucess init", 3)

    # create databases (has to be on host system)
    if(args["toInitDb"] == True):
        print("init db ...", 3)

    # clean + add data (can be remote)
    if(os.path.isfile(args["cleaner"]) == True) and (os.path.exists(args["newData"])):
        print("cleaning new files in: " + args["newData"] + " using: "
            + args["cleaner"] + "...", 3)

    # predicting (can be remote)
    if(None):
        None



#
# following section is just preamble to set some defaults and to update
#

# declaring usefull global variables
home = os.path.expanduser("~")
name = os.path.basename(sys.argv[0])

fileAndPath = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(fileAndPath))

prePend = "[ " + name + " ] "
description = name + "; " + "RavenRecSyst entry point."

dependancies = ["https://github.com/DreamingRaven/RavenPythonLib"]

# capture arguments in dict then put into json for bash
args = argz(sys.argv[1:], description=description)
args_json = json.loads(json.dumps(args))

# setting fallback logger here pre-update
log = Log(logLevel=args["loglevel"])
print = log.print

# attempting update/ falling back
try: # TODO: devise a method to make erros in nested try, catch
    from RavenPythonLib.updaters.gitUpdate import Gupdater
    nucleon = Gupdater(path=path, urls=dependancies)
    nucleon.install()
    nucleon.update()
    print("main updater success", 3)
except:
    print("Gupdater failed, falling back: " + str(sys.exc_info()[1]), 1)
    installer(path=path, urls=dependancies)
    updater(path=path, urls=dependancies)

# attempting set logger from external lib/ falling back
try:
    from RavenPythonLib.loggers.basicLog import Log
    log = Log(logLevel=args["loglevel"])
    print = log.print # note no '()' as function address desired not itself
    print("main logger success", 3)
except:
    log = Log(logLevel=args["loglevel"])
    print = log.print
    print("Main logger could not be loaded, falling back: " +
        str(sys.exc_info()[1]), 1)

# if level3 (debug) prepare for some verbose shnitzel
if(args["loglevel"] >= 3):
    main()
else:
    try:
        main()
        # raise ValueError('A very specific bad thing happened.')

    except:
        print(str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]), 2)
