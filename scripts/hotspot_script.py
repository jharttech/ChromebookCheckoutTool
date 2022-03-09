import csv
import subprocess
import datetime
import shutil

def main():
    info = getHotspotInfo()
    valid = False
    while not valid:
        newHotspots = createHotspotEntry(info)
        print(newHotspots)
        response = input("Does the entries above look correct? (y/n): ").lower()
        if response == 'y':
            valid = True
    if valid == True:
        print('Requested hotspot data has been compiled into ...ChromebookCheckoutTool/hotspots/"createdFileName", Thank You!')
        exit()


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
    errorNum = 0
    error = False
    valid = False
    headerList = ['Category', 'Model Name', 'Location', 'Manufacturer',
                    'Purchase Date', 'Purchase Cost', 'Order Number',
                    'Asset Tag', 'Serial Number', 'Sim Card Number']
    file = ('hotspots/' + str(info.get('isoDate') + "-PO" + info.get('poNumber') + "-hotspots.csv"))
    template = ('needed_file/hotspot_template.csv')
    #copyTemplate = ('cat ' + template + ' > ' + file)
    errorFile = 'hotspots/errorLog.csv'
    masterFile = 'hotspots/hotspot_master_list.csv'
    touchMasterFile = subprocess.Popen(["touch",masterFile])
    touchMasterFile.communicate()
    touchMasterFile.wait()
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
                touchFile = subprocess.Popen(["touch",file])
                touchFile.communicate()
                touchFile.wait()
                shutil.copy(template,file)
                with open(masterFile, mode='r') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        line_count += 1
                        if serialNumber in row:
                            error = True
                            errorNum += 1
                            print("Duplicate detected with Serial Number: " + serialNumber)
                            print("This hotspot record will not be added to csv file. This is recorded in ...ChromebookCheckoutTool/hotspots/errorLog.csv file.")
                            touchErrFile = subprocess.Popen(["touch",errorFile])
                            touchErrFile.communicate()
                            touchErrFile.wait()
                            timestamp = datetime.datetime.now()
                            tempLine = (timestamp, 'DUPLICATE ERROR', 'hotspot', info.get('brand'), 'MG Schools', info.get('manufacturer'),
                                        info.get('isoDate'), info.get('cost'), info.get('poNumber'),
                                        serialNumber, serialNumber, simCard)
                            with open(errorFile, mode='a') as error_file:
                                errors = csv.writer(error_file, delimiter=',')
                                errors.writerow(tempLine)
            if error == False:
                hotspotDict.update({keyNum + 1 : {'Serial Number' : serialNumber,'Sim Card Number' : simCard}})
                keyNum += 1
        if line_count == 0:
            lines.append(headerList)
            line_count += 1
    print(errorNum)
    if errorNum > 0:
        with open(errorFile, mode='a') as error_file:
            errors = csv.writer(error_file, delimiter=',')
            errors.writerow(divider)
    if counter == errorNum:
        print("Nothing to be done... quitting program now! Yes, I am a quitter.")
        exit()
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
        with open(file, mode='a') as hotspotCsv:
            for z in range(0,len(lines)):
                hotspotCSV = csv.writer(hotspotCsv, delimiter=',')
                hotspotCSV.writerow(lines[z])
    else:
        print("Noting to be done!... Pulling rip cord now.")
        exit()
    return hotspotDict

main()
