from sys import argv, exit
import csv
import mysql.connector
from mysql.connector import Error
import datetime
import subprocess

sanityCheck = ['y','n']

def main():
    check = len(argv)

    if check != 2:
        print("Usage: python ./db_move_user.py 'cvsFile.csv'")
        exit(1)
    filename = str(argv[1])
    tool = None
    dbBackedUp = None
    while dbBackedUp not in sanityCheck:
        dbBackedUp = input("Have you backed up your database? (y/n)\n").lower()
        if dbBackedUp == 'n':
            askBackup = None
            while askBackup not in sanityCheck:
                askBackup = input("Would you like to backup the snipeIT database now? (y/n)\n").lower()
                if askBackup == 'y':
                    dbUsername = input("Please enter the DB user name: \n")
                    dbname = input("Please enter the name of the DB: \n")
                    sqlName = input("Please enter the desired file name of the sql dump: \n")
                    sqlName = (sqlName + '.sql')
                    with open(sqlName, 'wb') as file:
                        writeDump = subprocess.Popen(["mysqldump","-u",dbUsername,"-p","--routines","--triggers",dbname], stdout=file)
                        writeDump.communicate()
                        writeDump.wait()
                else:
                    continue
        else:
            continue
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
    toolDict = {1 : "updateLocale", 2 : "EXIT"}
    while tool not in [1,2]:
        tool = int(input("\nWhich Database action would you like to take?\n1) Update Users Org user Locations\n2) EXIT\n"))
        return(toolDict.get(tool))

def lookForMovedLocales(localeToOU, ouToLocale, db, filename, tool):
    file = filename
    line_count = 0
    username = None
    errorCount = 0
    moved = 0
    divider = ['###################']
    errorFile = 'students/errorLog.csv'
    logFile = 'students/movingOU_logs.csv'
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        nCol = len(next(csv_reader))
        csv_file.seek(0)
        for row in csv_reader:
            if line_count == 0:
                for x in range(0,nCol):
                    colName = str(row[x])
                    if colName == 'Location':
                        orgUnitCol = x
                    if colName == 'Username':
                        usernameCol = x
                line_count += 1
            else:
                realUsername = row[usernameCol]
                realOU = row[orgUnitCol]
                convertedOU = ouToLocale.get(realOU)
                #pause = input("stopping here: press enter when ready")
                userLocale = getDBUserLocale(db)
                originalLocaleNum = userLocale.get(realUsername)
                originalOU = localeToOU.get(originalLocaleNum)
                if originalLocaleNum == convertedOU:
                    continue
                elif convertedOU == None:
                    errorCount += 1
                    timestamp = datetime.datetime.now()
                    tempLine = (timestamp, "ORG user ERROR", row)
                    makeErrorFile = subprocess.Popen(["touch",errorFile])
                    makeErrorFile.communicate()
                    with open(errorFile, mode='a') as error_file:
                        errors = csv.writer(error_file, delimiter=',')
                        errors.writerow(tempLine)
                elif originalLocaleNum == None:
                    errorCount += 1
                    timestamp = datetime.datetime.now()
                    tempLine = (timestamp, "User was never in Snipe DB", row)
                    makeErrorFile = subprocess.Popen(["touch",errorFile])
                    makeErrorFile.communicate()
                    with open(errorFile, mode='a') as error_file:
                        errors = csv.writer(error_file, delimiter=',')
                        errors.writerow(tempLine)
                elif originalLocaleNum != convertedOU:
                    moved += 1
                    updateDB(filename, db, realUsername, convertedOU, tool)
                    timestamp = datetime.datetime.now()
                    tempMoveLine = (timestamp, "user " + realUsername + " was moved from " + originalOU + " to " + realOU)
                    makeLogFile = subprocess.Popen(["touch",logFile])
                    makeLogFile.communicate()
                    with open(logFile, mode='a') as log_file:
                        logs = csv.writer(log_file, delimiter=',')
                        logs.writerow(tempMoveLine)
                else:
                    print("Unknown error, check csv data in " + filename + "! Quitting now!")
                    exit(1)
        if errorCount > 0:
            print("There were some errors in the moving of users to new OU in database. Old user location will remain as was.")
            print("Please check the error log for more details (/students/errorLog.csv)")
            with open(errorFile, mode='a') as error_file:
                errors = csv.writer(error_file, delimiter=',')
                errors.writerow(divider)
        if moved > 0:
            with open(logFile, mode='a') as log_file:
                logs = csv.writer(log_file, delimiter=',')
                logs.writerow(divider)
        print(str(moved) + " users were moved.")
        print("All done moving students to new locations in snipe database. Thank you!")

def updateDB(filename, db, user, location, tool):
    cursor = db.cursor()
    try:
        if tool == 'updateLocale':
            cursor.execute("UPDATE users SET location_id=%s WHERE username=%s",(location, user))
        db.commit()
        cursor.close()
    except Error as e:
        cursor.close()
        print("Error updating Table", e)

def getDBUserLocale(db):
    userLocale = {}
    cursor = db.cursor()
    cursor.execute("SELECT location_id, username FROM users")
    tableRecords = cursor.fetchall()
    for row in tableRecords:
        userLocale.update({row[1] : row[0]})
    if len(userLocale) != 0:
        cursor.close()
        return userLocale
    else:
        cursor.close()
        return "No User Data Found!!"

main()
