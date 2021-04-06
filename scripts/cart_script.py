import csv
import subprocess

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
    headerList = ['deviceId', 'serialNumber', 'model', 'orgUnitPath',
                    'autoUpdateExpiration']
    headerNum = []
    lines = []
    tempRow = []
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
                        headerNum.append(x)
                line_count += 1
            else:
                tempRow = [row[headerNum[0]],row[headerNum[1]],row[headerNum[2]],row[headerNum[3]],row[headerNum[4]]]
                lines.append(tempRow)
                line_count += 1
        if tempRow != []:
            with open('cartName.csv', mode='w') as cart_file:
                for i in range(0,len(lines)):
                    cartName = csv.writer(cart_file, delimiter=',')
                    cartName.writerow(lines[i])
        return line_count

main()
