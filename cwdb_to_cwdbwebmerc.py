#-------------------------------------------------------------------------------
# Name:        cwdb_to_cwdbwebmerc.py
# Purpose:     Synchronizes CWDB data to cwdb_webmerc.gdb
#              Copies features/views/tables that are not replica-compatible
#              (spatial and materialized views, unversioned features...)
#
# Author:      bschnick
#
# Created:     20/01/2015
# Copyright:   (c) bschnick 2015
# License:     MIT
#-------------------------------------------------------------------------------

# Import modules
import arcpy, time
from arcpy import env
from time import gmtime, strftime
from utilities import *

# Constants
DLIST = ["ORMPROJECTS_L", "ORMPROJECTS_P", "ORMWATERS_L", "ORMWATERS_P", "PestManagement_A",
         "GE_CONTROLMONUMENT_P_DISPLAY", "REALPROPERTY_P_REMIS_VW"]
TLIST = ["REMIS_IMPROVEMENT", "REMIS_OUTGRANT", "REMIS_PROJECT", "REMIS_PROPERTY", "REMIS_TRACT",
         "ChemControlAttributes", "LicensedPesticideApplicator", "PestControlJoin",
         "PesticideAppSponsor", "BioControlAttributes", "MechControlAttributes"]
GDB1 = "<sde connection file>"
GDB2 = "<path to>cwdb_webmerc.gdb"
SCRATCHGDB = "D:\\temp\\scratch.gdb"

def synch(f, GDB1, GDB2):
    # Set the necessary product code
    try:
        import arceditor

        arcpy.env.overwriteOutput = True

        Geographic_Transformations = "WGS_1984_(ITRF08)_To_NAD_1983_2011"

        # Process: Synchronize Changes
        tempEnvironment0 = arcpy.env.geographicTransformations

        arcpy.env.geographicTransformations = "WGS_1984_(ITRF08)_To_NAD_1983_2011"

        arcpy.SynchronizeChanges_management(GDB1, "CWDB.cwdb_webmerc", GDB2, "FROM_GEODATABASE1_TO_2", "IN_FAVOR_OF_GDB1", "BY_OBJECT", "DO_NOT_RECONCILE")

        arcpy.env.geographicTransformations = tempEnvironment0
        arcpy.env.overwriteOutput=True

        s = "cwdb replica synchronization complete, continuing to copy unsupported items."
        log(f, s)
    except Exception as e:
        s = "Could not synchronize CWDB to cwdb_webmerc.gdb\n"
        s += e.message
        log(f, s)

def project_DLIST(DLIST, GDB1, GDB2, SCRATCHGDB, f):
    # Project features to web_mercator_auxillary_sphere in SCRATCHGDB
    # (project must write to disk + not in_memory)
    projectedList = []
    for d in DLIST:
        try:
            ind = GDB1 + "\\CWDB." + d
            outd = SCRATCHGDB + "\\" + d
            desc = arcpy.Describe(ind)
            sr = desc.spatialReference.Name
            if sr == 'GCS_North_American_1983':
                arcpy.Project_management(ind, outd, "E:/eGIS/replication/webmerc.prj", "WGS_1984_(ITRF00)_To_NAD_1983")
                projectedList.append(outd)
                s = d + " projected"
                log(f, s)
            elif sr == 'GCS_NAD_1983_2011':
                arcpy.Project_management(ind, outd, "E:/eGIS/replication/webmerc.prj", "WGS_1984_(ITRF00)_To_NAD_1983_2011")
                projectedList.append(outd)
                s = d + " projected"
                log(f, s)
            else:
                s = d + " has projection " + sr
                log(f, s)
        except Exception as e:
            s = "Could not project " + ind + " to SCRATCHGDB\n"
            s += e.message
            log(f, s)
    return projectedList

def delete_DLIST(GDB2, projectedList, f):
    # Delete features from cwdb_webmerc in prep for new features
    env.workspace = GDB2
    for ea in projectedList:
        try:
            arcpy.Delete_management(ea.rsplit("\\", 1)[1])
            s = "Deleted " + ea.rsplit("\\", 1)[1] + " from cwdb_webmerc.gdb"
            log(f, s)
        except Exception as e:
            s = "Could not delete " + ea.rsplit("\\", 1)[1] + " from cwdb_webmerc.gdb\n"
            s += e.message
            log(f, s)

def copy_DLIST(GDB2, projectedList, f):
    # Copy the projected features to the replica gdb
    env.workspace = GDB2
    arcpy.env.overwriteOutput = 1
    for ea in projectedList:
        try:
            arcpy.FeatureClassToFeatureClass_conversion(ea, GDB2, ea.rsplit("\\", 1)[1],"","","")
            s = ea + " copied to cwdb_webmerc.gdb"
            log(f, s)
        except Exception as e:
            s = "Could not copy " + ea + " to cwdb_webmerc.gdb.\n"
            s += e.message
            log(f, s)

def features(DLIST, GDB1, GDB2, SCRATCHGDB, f):
    projectedList = project_DLIST(DLIST, GDB1, GDB2, SCRATCHGDB, f)
    # delete_DLIST(GDB2, projectedList, f)
    copy_DLIST(GDB2, projectedList, f)

def tables(TLIST, GDB1, GDB2, f):
    # For tables
    for t in TLIST:
        try:
            arcpy.TableToTable_conversion((GDB1 + "\\" + t), GDB2, t, "", "", "")
            s = t + " copied"
            log(f, s)
        except Exception as e:
            s = "Could not copy " + t + " to cwdb_webmerc.gdb\n"
            s += e.message
            log(f, s)

def main():
    starttime = time.clock()
    f = createLogFile("E:/eGIS/replication/logs/cwdb_to_cwdbwebmerc.txt")
    synch(f, GDB1, GDB2)
    features(DLIST, GDB1, GDB2, SCRATCHGDB, f)
    tables(TLIST, GDB1, GDB2, f)
    check_spatial_reference(f, GDB2, 'WGS_1984_Web_Mercator_Auxiliary_Sphere')
    now = time.localtime()
    finishtime = time.clock()
    log(f, "Finished: " + strftime("%d%b%Y%H%M", now) + "\n")
    elapsedtime = time.gmtime(finishtime - starttime)
    log(f, "Elapsedtime: " + time.strftime("%HH:%MM:%SS", elapsedtime))

if __name__ == "__main__":
    main()