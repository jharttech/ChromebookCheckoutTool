import csv
import subprocess
import datetime

def main():
    setup()
    getWantedData()

def getWantedData():
    headerList = ['deviceId', 'autoUpdateExpiration', 'serialNumber', 'macAddress', 'model', 'orgUnitPath']
    headerToNum = {}
    lines = []
    tempRow = []
    num = None
    with open('../needed_file/deprovisioned_full.csv') as csv_file:
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
                headerRow = ['deviceId', 'autoUpdateExpiration', 'Serial Number', 'macAddress',
                                'Model Name', 'notes', 'Location', 'Manufacturer', 'Category', 'Asset Tag']
                lines.append(headerRow)
                line_count += 1
            else:
                notes = 'Removed From Campus'
                location = "DEPROVISIONED"
                category = 'Chromebook'
                if row[headerToNum.get('autoUpdateExpiration', "Error getting header number!")] != '':
                    updateExp = datetime.datetime.fromtimestamp(float(row[headerToNum.get('autoUpdateExpiration')])/1000.0)
                    updateExp = updateExp.strftime('%Y-%m-%d')
                else:
                    updateExp = row[headerToNum.get('autoUpdateExpiration', 'Error getting header number!')]
                assetTag = row[headerToNum.get('serialNumber')]
                if len(assetTag) > 14:
                    tempAssetTag = list(assetTag)
                    while len(tempAssetTag) > 14:
                        tempAssetTag.remove(tempAssetTag[0])
                    assetTag = ''.join(tempAssetTag)
                tempRow = [row[headerToNum.get('deviceId', "Error getting header number!")],
                            updateExp, row[headerToNum.get('serialNumber', "Error getting header number!")],
                            row[headerToNum.get('macAddress', "Error getting header number!")], row[headerToNum.get('model', "Error getting header number!")], notes,
                            location, row[headerToNum.get('model', "Error getting header number!")], category, assetTag]
                lines.append(tempRow)
                line_count += 1
        if tempRow != []:
            with open('../carts/deprovisioned/deprovisionedFull.csv', mode='w') as cart_file:
                for i in range(0,len(lines)):
                    deproFull = csv.writer(cart_file, delimiter=',')
                    deproFull.writerow(lines[i])
    return

def setup():
    dir = '../carts/deprovisioned'
    subprocess.call(['mkdir',dir])

main()
