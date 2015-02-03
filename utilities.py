#-------------------------------------------------------------------------------
# Name:        utilities
# Purpose:     Contains functions to be imported by other scripts
#
# Author:      bschnick
#
# Created:     20/01/2015
# Copyright:   (c) bschnick 2015
# License:     MIT
#-------------------------------------------------------------------------------

import arcpy, time
from arcpy import env
from time import strftime

def createLogFile(f):
    # Create log file if needed, open in 'append' mode
    now = time.localtime()
    logfile = open(f, 'w') # Write mode clears the file; only most recent run is stored
    logfile.write("========================================\n")
    logfile.close()
    s = "Start: " + strftime("%d%b%Y%H%M", now) + "\n"
    log(f, s)
    return f

def log(f, s):
    # Print message if script is being run in console
    print(s)
    # AddMessage if script is being run in script tool
    arcpy.AddMessage(s)
    # Write to log file for permanence
    logfile = open(f,'a')
    now = time.localtime()
    s = strftime("%d %b %Y %H:%M:%S    ", now) + str(s) + "\n"
    logfile.write(s)
    logfile.close()

def check_spatial_reference(f, workspace, spatial_reference):
    env.workspace = workspace
    fcList = arcpy.ListFeatureClasses()
    coordSysSet = set()
    badFCList = []
    for ea in fcList:
        desc = arcpy.Describe(ea)
        sr = desc.spatialReference.Name
        if sr != spatial_reference:
            badFCList.append(ea)
        coordSysSet.add(sr)

    log(f, "\nThe following coordinate systems were found in " + workspace + ":")
    for ea in coordSysSet:
        log(f, ea + "\n")
    if badFCList:
        log(f, "\nThese features are not projected in " + spatial_reference + ":")
        log(f, badFCList)
    else:
        log(f, "\nAll features are projected in  " + spatial_reference + "!")

def main():
    pass

if __name__ == '__main__':
    main()
