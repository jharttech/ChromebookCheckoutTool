from sys import argv, exit
import csv
import mysql.connector
from mysql.connector import Error

check = len(argv)

if check != 2:
    print("Usage: python ./databaseTool.py 'cvsFile.csv'")
    exit(1)
filename = str(argv[1])

#Connect to database
try:
    db = mysql.connector.connect(
        host="FIXME",
        database='FIXME',
        user="FIXME",
        password="FIXME"
    )
    if db.is_connected():
        print("Connected to database! ")
        cursor = db.cursor()
        with open(filename, "r") as inputCsv:

            #Create DictReader
            reader = csv.DictReader(inputCsv, delimiter=",")

            #Iterate over CSV file
            for row in reader:

                #Change Field values
                asset_tag = row["Asset Tag"]
                #sanity check
                print(asset_tag)

                cursor.execute("UPDATE assets SET rtd_location_id=%s, location_id=%s, _snipeit_orgunitpath_4=%s WHERE asset_tag=%s",("88","88","DEPROVISIONED", asset_tag))
                db.commit()
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (db.is_connected()):
        cursor.close()
        db.close()
