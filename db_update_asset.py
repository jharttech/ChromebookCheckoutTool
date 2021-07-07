from sys import argv, exit
import csv
import mysql.connector
from mysql.connector import Error
import datetime
import subprocess

def main():
    check = len(argv)

    if check != 2:
        print("Usage: python ./databaseTool.py 'cvsFile.csv'")
        exit(1)
    filename = str(argv[1])
    tool = None
    while tool != 'EXIT':
        tool = getDBTool()
        if tool == "EXIT":
            exit(1)
        elif tool != None:
            connected = connectToDB()
            if connected[0] == True:
                db = connected[1]
                print("Connected to Database!")
                returnDicts = getDBLocationData(db)
                localeToOU = returnDicts[0]
                ouToLocale = returnDicts[1]
                #print(localeToOU)
                #print(ouToLocale)
                lookForMovedLocales(localeToOU, ouToLocale, db, filename, tool)
                db.close()
            else:
                print("Error connecting to database:")
                print(connectToDB())

def connectToDB():
    try:
        db = mysql.connector.connect(
            host="FIXME",
            database='FIXME',
            user="FIXME",
            password="FIXME"
        )
        if db.is_connected():
            return [True, db]
    except Error as e:
        return [e, None]

def getDBLocationData(db):
    localeCodeToOUDict = {}
    ouToLocaleCodeDict = {}
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM locations")
    records = cursor.fetchall()
    for row in records:
        localeCodeToOUDict.update({row[0] : row[1]})
        ouToLocaleCodeDict.update({row[1] : row[0]})
    if (len(localeCodeToOUDict) != 0) and (len(ouToLocaleCodeDict) != 0):
        cursor.close()
        return [localeCodeToOUDict, ouToLocaleCodeDict]
    else:
        return "No Location Data Found!!"

def getDBTool():
    tool = None
    toolDict = {1 : "updateLocale", 2 : "updateDeprovisioned", 3 : "EXIT"}
    while tool not in [1,2,3]:
        tool = int(input("\nWhich Database action would you like to take?\n1) Update Chromebook Org Unit Locations\n2) Update Deprovisioned Chromebooks\n3) EXIT\n"))
        return(toolDict.get(tool))

def lookForMovedLocales(localeToOU, ouToLocale, db, filename, tool):
    file = filename
    line_count = 0
    assetTag = None
    errorCount = 0
    moved = 0
    divider = ['###################']
    errorFile = 'carts/errorLog.csv'
    logFile = 'carts/movingOU_logs.csv'
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        nCol = len(next(csv_reader))
        csv_file.seek(0)
        for row in csv_reader:
            if line_count == 0:
                for x in range(0,nCol):
                    colName = str(row[x])
                    if colName == 'Location':
                        orgUnitRow = x
                    if colName == 'Asset Tag':
                        assetTagRow = x
                line_count += 1
            else:
                realAssetTag = row[assetTagRow]
                realOU = row[orgUnitRow]
                convertedOU = ouToLocale.get(realOU)
                #pause = input("stopping here: press enter when ready")
                assetLocale = getDBAssetLocale(db)
                originalLocaleNum = assetLocale.get(realAssetTag)
                originalOU = localeToOU.get(originalLocaleNum)
                if originalLocaleNum == convertedOU:
                    continue
                elif convertedOU == None:
                    errorCount += 1
                    timestamp = datetime.datetime.now()
                    tempLine = (timestamp, "ORG UNIT ERROR", row)
                    subprocess.call(['touch', errorFile])
                    with open(errorFile, mode='a') as error_file:
                        errors = csv.writer(error_file, delimiter=',')
                        errors.writerow(tempLine)
                elif originalLocaleNum == None:
                    errorCount += 1
                    timestamp = datetime.datetime.now()
                    tempLine = (timestamp, "Unit was never in Snipe DB", row)
                    subprocess.call(['touch', errorFile])
                    with open(errorFile, mode='a') as error_file:
                        errors = csv.writer(error_file, delimiter=',')
                        errors.writerow(tempLine)
                elif originalLocaleNum != convertedOU:
                    moved += 1
                    updateDB(filename, db, realAssetTag, convertedOU, tool)
                    timestamp = datetime.datetime.now()
                    tempMoveLine = (timestamp, "Unit " + realAssetTag + " was moved from " + originalOU + " to " + realOU)
                    subprocess.call(['touch', logFile])
                    with open(logFile, mode='a') as log_file:
                        logs = csv.writer(log_file, delimiter=',')
                        logs.writerow(tempMoveLine)
                else:
                    print("Unknown error, check csv data in " + filename + "! Quitting now!")
                    exit(1)
        if errorCount > 0:
            print("There were some errors in the moving of units to new OU in database. Old unit location will remain as was.")
            print("Please check the error log for more details (/carts/errorLog.csv)")
            with open(errorFile, mode='a') as error_file:
                errors = csv.writer(error_file, delimiter=',')
                errors.writerow(divider)
        if moved > 0:
            with open(logFile, mode='a') as log_file:
                logs = csv.writer(log_file, delimiter=',')
                logs.writerow(divider)
        print(str(moved) + " units were moved.")
        print("All done moving chromebooks to new locations in snipe database. Thank you!")

def updateDB(filename, db, asset, rtd_location, tool):
    cursor = db.cursor()
    try:
        if tool == 'updateLocale':
            cursor.execute("UPDATE assets SET rtd_location_id=%s WHERE asset_tag=%s",(rtd_location, asset))
        elif tool == 'updateDeprovisioned':
            cursor.execute("UPDATE assets SET rtd_location_id=%s, location_id=%s, _snipeit_orgunitpath_4=%s WHERE asset_tag=%s",(rtd_location, rtd_location, "DEPROVISIONED", asset))
        db.commit()
        cursor.close()
    except Error as e:
        cursor.close()
        print("Error updating Table", e)

def getDBAssetLocale(db):
    assetLocale = {}
    cursor = db.cursor()
    cursor.execute("SELECT rtd_location_id, asset_tag FROM assets")
    tableRecords = cursor.fetchall()
    for row in tableRecords:
        assetLocale.update({row[1] : row[0]})
    if len(assetLocale) != 0:
        cursor.close()
        return assetLocale
    else:
        cursor.close()
        return "No Asset Data Found!!"

main()
