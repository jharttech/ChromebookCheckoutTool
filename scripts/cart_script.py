import csv
import subprocess
import datetime

def main():
    #building = getBuilding()
    test = getWantedData()
    print(test)

def getBuilding():
    buildingList = ['ES', 'MS', 'HS', 'OMTC', 'ALC']
    while not valid:
        building = input("Please enter the building wanted (ES, MS, HS, OMTC, ALC): ")
        building = building.toupper()
        if building in buildingList:
            valid = True
            print("You chose",building)
            correct = input("Is that the correct building? (y/n)" )
            if correct.tolower() != 'y':
                valid = False
            else:
                return building

def getWantedData():
    headerList = ['deviceId', 'autoUpdateExpiration', 'serialNumber', 'macAddress', 'model', 'orgUnitPath']
    #headerNum = []
    headerToNum = {}
    lines = []
    tempRow = []
    num = None
    with open('../needed_file/full.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        nCol = len(next(csv_reader))
        csv_file.seek(0)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                for x in range(0,nCol):
                    colName = str(row[x])
                    if colName in headerList:
                        num = headerToNum.update({colName : x})
                        #headerNum.append(num)
                line_count += 1
            else:
                notes = 'Initial Import'
                category = 'Chromebook'
                if row[headerToNum.get('autoUpdateExpiration')] != '':
                    updateExp = datetime.datetime.fromtimestamp(float(row[headerToNum.get('autoUpdateExpiration')])/1000.0)
                    updateExp = updateExp.strftime('%Y-%m-%d')
                else:
                    updateExp = row[headerToNum.get('autoUpdateExpiration')]
                assetTag = row[headerToNum.get('serialNumber')]
                if len(assetTag) > 14:
                    tempAssetTag = list(assetTag)
                    while len(tempAssetTag) > 14:
                        tempAssetTag.remove(tempAssetTag[0])
                    assetTag = ''.join(tempAssetTag)
                #testVar = headerToNum.get(, "Error getting header number!")
                tempRow = [row[headerToNum.get('deviceId', "Error getting header number!")],
                            updateExp, row[headerToNum.get('serialNumber')],
                            row[headerToNum.get('macAddress')], row[headerToNum.get('model')], notes,
                            row[headerToNum.get('orgUnitPath')], row[headerToNum.get('model')], category, assetTag]
                lines.append(tempRow)
                line_count += 1
        if tempRow != []:
            with open('cartName.csv', mode='w') as cart_file:
                for i in range(0,len(lines)):
                    cartName = csv.writer(cart_file, delimiter=',')
                    cartName.writerow(lines[i])
        return

main()
