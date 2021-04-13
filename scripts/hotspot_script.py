import csv
import os
import subprocess
import datetime

def main():
    info = getHotspotInfo()
    valid = False
    while not valid:
        newHotspots = createHotspotEntry(info)
        print(newHotspots)
        response = input("Does the entries above look correct? (y/n): ").lower()
        if response == 'y':
            valid = True


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
    divider = ['###########']
    hotspotDict = {}
    tempRow = []
    lines = []
    dictLineToDelete = []
    line_count = 0
    keyNum = 0
    error = False
    valid = False
    headerList = ['Category', 'Model Name', 'Location', 'Manufacturer',
                    'Purchase Date', 'Purchase Cost', 'Order Number',
                    'Asset Tag', 'Serial Number', 'Sim Card Number']
    file = ('../hotspots/' + str(info.get('isoDate') + "-PO" + info.get('poNumber') + "-hotspots.csv"))
    errorFile = '../hotspots/errorLog.csv'
    masterFile = '../hotspots/hotspot_master_list.csv'
    subprocess.call(['touch',masterFile])
    print("Now going to ask for information about each hotspot being added.")
    for n in range(0,counter):
        valid = False
        error = False
        while valid == False:
            serialNumber = input("Please enter the Serial Number (no spaces) for hotspot " + str(n + 1) + ": ")
            simCard = input("Please enter the Sim Card Number (no spaces) for hotspot " + str(n + 1) + ": ")
            print("You have entered hotspot " + str(n + 1) + "'s Serial Number as: " + str(serialNumber))
            print("and Sim Card Number as: " + simCard)
            response = input("Is that information correct? (y/n): ").lower()
            if response == 'y':
                valid = True
                subprocess.call(['touch',file])
                with open(masterFile, mode='r') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        if serialNumber in row:
                            error = True
                            print("Duplicate detected with Serial Number: " + serialNumber)
                            print("This hotspot record will not be added to csv file. This is recorded in ...ChromebookCheckoutTool/hotspots/errorLog.csv file.")
                            subprocess.call(['touch',errorFile])
                            timestamp = datetime.datetime.now()
                            tempLine = (timestamp, 'DUPLICATE ERROR', 'hotspot', info.get('brand'), 'MG Schools', info.get('manufacturer'),
                                        info.get('isoDate'), info.get('cost'), info.get('poNumber'),
                                        serialNumber, serialNumber, simCard)
                            with open(errorFile, mode='a') as error_file:
                                errors = csv.writer(error_file, delimiter=',')
                                errors.writerow(tempLine)
                                errors.writerow(divider)
            if error == False:
                hotspotDict.update({keyNum + 1 : {'Serial Number' : serialNumber,'Sim Card Number' : simCard}})
                keyNum += 1
                if counter == 1:
                    print("Nothing to be done... quitting program now! Yes, I am a quitter.")
                    exit()
            line_count += 1
        if line_count == 0:
            lines.append(headerList)
            line_count += 1
    for x in range(0,len(hotspotDict)):
        tempRow = ['hotspot', info.get('brand'), 'MG Schools', info.get('manufacturer'),
                    info.get('isoDate'), info.get('cost'), info.get('poNumber'),
                    hotspotDict[x + 1]['Serial Number'], hotspotDict[x + 1]['Serial Number'],
                    hotspotDict[x + 1]['Sim Card Number']]
        lines.append(tempRow)
    if lines != []:
        with open(masterFile, mode='a') as hotspot_file:
            for i in range(0,len(lines)):
                hotspotMaster = csv.writer(hotspot_file, delimiter=',')
                hotspotMaster.writerow(lines[i])
        with open(file, mode='w') as hotspotCsv:
            for z in range(0,len(lines)):
                hotspotCSV = csv.writer(hotspotCsv, delimiter=',')
                hotspotCSV.writerow(lines[z])
    return hotspotDict

main()
