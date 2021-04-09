import csv
import os
import subprocess

def main():
    info = getHotspotInfo()
    createHotspotEntry(info)

def getHotspotInfo():
    valid = False
    collectedInfo = {
    'count' : None,
    'isoDate' : '',
    'manufacturer' : None,
    'brand' : None,
    'cost' : None,
    'poNumber' : None
    }
    while not valid:
        while type(collectedInfo.get('count')) != int:
            count = int(input("Please enter the amount of hotspots you would like to add to the campus: "))
            print(count)
            collectedInfo.update({'count' : count})
        while len(collectedInfo.get('isoDate')) != 8:
            isoDate = input("Please enter the date in ISO format (ex: YYYYMMDD): ")
            collectedInfo.update({'isoDate' : isoDate})
        manufacturer = input("Please enter the manufacturer of the hotspots: ")
        collectedInfo.update({'manufacturer' : manufacturer})
        brand = input("Please enter the brand of the hotspots: ")
        collectedInfo.update({'brand' : brand})
        while type(collectedInfo.get('cost')) != float:
            cost = float(input("Please enter the cost, in decimal format, of each hotspot: "))
            collectedInfo.update({'cost' : cost})
        poNumber = input("Please enter the PO Number or Project Title used to purchase the hotspots: ")
        collectedInfo.update({'poNumber' : poNumber})
        print(collectedInfo)
        response = input("Does the information you provided look correct? (y/n) ").lower()
        if response == 'y':
            valid = True
    return collectedInfo

def createHotspotEntry(info):
    counter = info.get('count')
    file = str(info.get('isoDate') + "-PO" + info.get('poNumber') + "-hotspots.csv")
    errorFile = 'errorLog.txt'
    masterFile = 'hotspot_master_list.csv'
    subprocess.call(['touch',masterFile])

main()
