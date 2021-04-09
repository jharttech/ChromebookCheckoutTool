import csv
import os
import subprocess

def main():
    info = getHotspotInfo()
    test = createHotspotEntry(info)
    print(test)

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
    hotspotDict = {}
    tempRow = []
    line_count = 0
    valid = False
    headerList = ['Category', 'Model Name', 'Location', 'Manufacturer',
                    'Purchase Date', 'Purchase Cost', 'Order Number',
                    'Asset Tag', 'Serial Number', 'Sim Card Number']
    file = str(info.get('isoDate') + "-PO" + info.get('poNumber') + "-hotspots.csv")
    errorFile = 'errorLog.txt'
    masterFile = '../needed_file/hotspot_master_list.csv'
    subprocess.call(['touch',masterFile])
    print("Now going to ask for information about each hotspot being added.")
    for i in range(0,counter):
        valid = False
        while valid == False:
            serialNumber = input("Please enter the Serail Number (no spaces) for hotspot " + str(i + 1) + ": ")
            simCard = input("Please enter the Sim Card Number (no spaces) for hotspot " + str(i + 1) + ": ")
            print("You have entered hotspot " + str(i + 1) + "'s Serial Number as: " + str(serialNumber))
            print("and Sim Card Number as: " + simCard)
            response = input("Is that information correct? ").lower()
            if response == 'y':
                valid = True
                hotspotDict.update({i + 1 : {'Serial Number' : serialNumber,'Sim Card Number' : simCard}})
    with open(masterFile, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            line_count += 1
        if line_count == 0:
            with open('../needed_file/' + masterFile, mode='w') as hotspot_file:
                hotspotFile = csv.writer(hotspot_file, delimiter=',')
                hotspotFile.writerow(headerList)
                line_count += 1
    return hotspotDict

main()
