import csv
import subprocess
import datetime

def main():
    getWantedData()
    building = getBuilding()
    if building == 'ALL':
        file = 'needed_file/cartFull.csv'
        dest = 'carts/cartFull.csv'
        subprocess.call(['mv',file,dest])
        print("All cart data has been compiled into ...ChromebookCheckoutTool/carts/cartFull.csv")
        exit()
    cart = getCart(building)
    print("Requested data and files have been created.  Thank you!")
    exit()


def getBuilding():
    valid = False
    while not valid:
        buildingList = getBuildingNames()
        buildingList.append('ALL')
        building = input("Please enter the building wanted (" + str(', '.join(buildingList)) + "): ")
        building = building.upper()
        if building in buildingList:
            valid = True
            print("You chose",building)
            correct = input("Is that the correct building? (y/n) " )
            if correct.lower() != 'y':
                valid = False
            else:
                return building

def getWantedData():
    headerList = ['deviceId', 'autoUpdateExpiration', 'serialNumber', 'macAddress', 'model', 'orgUnitPath']
    #headerNum = [] #DEBUG INFO
    headerToNum = {}
    lines = []
    tempRow = []
    num = None
    with open('needed_file/full.csv') as csv_file:
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
                        #headerNum.append(num) #DEBUG INFO
                headerRow = ['deviceId','autoUpdateExpiration','Serial Number','macAddress','Model Name','notes','Location','Manufacturer','Category','Asset Tag']
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
                            row[headerToNum.get('orgUnitPath', "Error getting header number!")], row[headerToNum.get('model', "Error getting header number!")], category, assetTag]
                lines.append(tempRow)
                line_count += 1
        if tempRow != []:
            with open('needed_file/cartFull.csv', mode='w') as cart_file:
                for i in range(0,len(lines)):
                    cartFull = csv.writer(cart_file, delimiter=',')
                    cartFull.writerow(lines[i])
        else:
            print("Error: No lines added.  Bailing out now!")
            exit()


def getCart(building):
    tempCart = []
    num = None
    bookCount = 0
    cart = input("Please enter the cart name desired, or enter 'ALL' for all carts in " + building + ": ")
    cartUp = cart.upper()
    if cartUp != 'ALL':
        with open('needed_file/cartFull.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            lines = []
            nCol = len(next(csv_reader))
            csv_file.seek(0)
            for row in csv_reader:
                if line_count == 0:
                    for x in range(0,nCol):
                        columnName = str(row[x])
                        if columnName == 'Location':
                            num = x
                    lines.append(row)
                    line_count += 1
                else:
                    tempCart = row[num].split('/')
                    tempCart = tempCart[len(tempCart) - 1].upper()
                    if tempCart == cartUp:
                        lines.append(row)
                        line_count += 1
        with open('carts/single/' + cart + '.csv', mode='w') as cart_file:
            for i in range(0,len(lines)):
                cartFile = csv.writer(cart_file, delimiter=',')
                cartFile.writerow(lines[i])
    elif cartUp == 'ALL':
        listOfCarts = getNumOfCarts(building)
        newDir = building
        num = None
        newDirLocal = 'carts/'
        subprocess.call(['mkdir',newDirLocal + newDir])
        for b in range(0,len(listOfCarts)):
            with open('needed_file/cartFull.csv', mode='r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                lines = []
                nCol = len(next(csv_reader))
                csv_file.seek(0)
                for row in csv_reader:
                    if line_count == 0:
                        for x in range(0,nCol):
                            columnName = str(row[x])
                            if columnName == 'Location':
                                num = x
                        lines.append(row)
                        line_count += 1
                    else:
                        tempCart = row[num].split('/')
                        tempCart = tempCart[len(tempCart) - 1].upper()
                        if tempCart == listOfCarts[b].upper():
                            lines.append(row)
                        line_count += 1
            with open('carts/' + building + '/' + listOfCarts[b] + '.csv', mode='w') as cart_file:
                for i in range(0,len(lines)):
                    cartFile = csv.writer(cart_file, delimiter=',')
                    cartFile.writerow(lines[i])

def getNumOfCarts(building):
    cartNames = []
    tempCartNames = []
    tempList = []
    num = None
    with open('needed_file/cartFull.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        nCol = len(next(csv_reader))
        csv_file.seek(0)
        for row in csv_reader:
            if line_count == 0:
                for x in range(0,nCol):
                    columnName = str(row[x])
                    if columnName == 'Location':
                        num = x
                        line_count += 1
            else:
                if building in str(row[num]) and str(row[num]) not in tempList:
                    tempList.append(row[num])
    for z in range(0,len(tempList)):
        tempCartNames = tempList[z].split('/')
        if building in tempCartNames[len(tempCartNames) - 1]:
            cartNames.append(tempCartNames[len(tempCartNames) - 1])
    return cartNames

def getBuildingNames():
    buildingList = []
    tempBuilding = []
    num = None
    with open('needed_file/cartFull.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        nCol = len(next(csv_reader))
        csv_file.seek(0)
        for row in csv_reader:
            if line_count == 0:
                for x in range(0,nCol):
                    columnName = str(row[x])
                    if columnName == 'Location':
                        num = x
                        line_count += 1
            else:
                tempBuilding = row[num].split('/')
                if (len(tempBuilding)) > 3 and tempBuilding[2] not in buildingList:
                    buildingList.append(tempBuilding[2])
    return buildingList

main()
