import csv
import subprocess
import datetime

def main():
    getWantedData()
    print("All cart data with OS Versions has been compiled into ...ChromebookCheckoutTool/carts/unitOsVersions.csv")
    exit()

def getWantedData():
    headerList = ['deviceId', 'autoUpdateExpiration', 'serialNumber', 'macAddress', 'model', 'orgUnitPath', 'osVersion']
    #headerNum = [] #DEBUG INFO
    headerToNum = {}
    lines = []
    tempRow = []
    num = None
    with open('needed_file/full.csv') as csv_file:
        csv_reader = csv.reader((line.replace('\0', '') for line in csv_file), csv_file, delimiter=',')
        nCol = len(next(csv_reader))
        csv_file.seek(0)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                for x in range(0,nCol):
                    colName = str(row[x])
                    if colName in headerList:
                        num = headerToNum.update({colName : x})
                        #headerNum.append(num) #DEBUG INFO
                headerRow = ['deviceId','autoUpdateExpiration','Serial Number','macAddress','Model Name','notes','Location','Manufacturer','Category','Asset Tag', 'osVersion']
                lines.append(headerRow)
                line_count += 1
            else:
                notes = 'Initial Import'
                category = 'Chromebook'
                if row[headerToNum.get('autoUpdateExpiration', "Error getting header number!")] != '':
                    updateExp = datetime.datetime.fromtimestamp(float(row[headerToNum.get('autoUpdateExpiration')])/1000.0)
                    updateExp = updateExp.strftime('%Y-%m-%d')
                else:
                    updateExp = row[headerToNum.get('autoUpdateExpiration', "Error getting header number!")]
                assetTag = row[headerToNum.get('serialNumber')]
                if len(assetTag) > 14:
                    tempAssetTag = list(assetTag)
                    while len(tempAssetTag) > 14:
                        tempAssetTag.remove(tempAssetTag[0])
                    assetTag = ''.join(tempAssetTag)
                tempRow = [row[headerToNum.get('deviceId', "Error getting header number!")],
                            updateExp, row[headerToNum.get('serialNumber', "Error getting header number!")],
                            row[headerToNum.get('macAddress', "Error getting header number!")], row[headerToNum.get('model', "Error getting header number!")], notes,
                            row[headerToNum.get('orgUnitPath', "Error getting header number!")], row[headerToNum.get('model', "Error getting header number!")], category, assetTag, row[headerToNum.get('osVersion', "Error getting OS Version!")]]
                lines.append(tempRow)
                line_count += 1
        if tempRow != []:
            with open('needed_file/unitOsVersions.csv', mode='w') as cart_file:
                for i in range(0,len(lines)):
                    osVersion = csv.writer(cart_file, delimiter=',')
                    osVersion.writerow(lines[i])
        else:
            print("Error: No lines added.  Bailing out now!")
            exit()

main()
