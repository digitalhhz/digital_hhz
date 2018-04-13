#!/usr/bin/python

# Import required modules
import sys
import os

# Execute index.js which starts the janitor service 
pathToFile = "/home/hhz/Scripts/janitor_service/node-enocean-server-template/index.js"
cmd = "node " + pathToFile

p = os.popen(cmd,"r")

