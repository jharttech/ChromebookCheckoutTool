import csv
import os
import subprocess

def main():
    getWantedData()
    building = getBuilding()
    if building == 'ALL':
        file = '../needed_file/studentFull.csv'
        dest = '../students/studentFull.csv'
        subprocess.call(['mv',file,dest])
        print("All student data has been compiled into ..ChromebookCheckoutTool/students/studentFull.csv")
        exit()
    else:
        getStudentsInfo(building)
        print('Requested student data has been compiled into ..ChromebookCheckoutTool/students/"SelectedBuilding".csv')
        exit()

def getWantedData():
    headerList = ['primaryEmail', 'name.givenName', 'name.familyName', 'orgUnitPath']
    headerToNum = {}
    lines = []
    tempRow = []
    num = None
    with open('../needed_file/full_student.csv') as csv_file:
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
                headerRow = ['Email', 'First Name', 'Last Name', 'Location', 'Notes', 'Username']
                lines.append(headerRow)
                line_count += 1
                print(headerToNum)
            else:
                notes = 'Initial Import'
                if row[headerToNum.get('primaryEmail')] != '':
                    username = row[headerToNum.get('primaryEmail')].split('@')
                    username = username[0]
                else:
                    username = row[headerToNum.get('primaryEmail')]
                tempRow = [row[headerToNum.get('primaryEmail', "Error getting header number")],
                            row[headerToNum.get('name.givenName', "Error getting header number!")],
                            row[headerToNum.get('name.familyName', "Error getting header number!")],
                            row[headerToNum.get('orgUnitPath', "Error getting header number!")],
                            notes, username]
                lines.append(tempRow)
        if tempRow != []:
            with open('../needed_file/studentFull.csv', mode='w') as student_file:
                for i in range(0,len(lines)):
                    studentFull = csv.writer(student_file, delimiter=',')
                    studentFull.writerow(lines[i])
        else:
            print('Error: no student data to add.  Bummer! Now going to exit!')
            exit()

def getStudentsInfo(building):
    with open('../needed_file/studentFull.csv', mode='r') as csv_file:
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
                tempBuilding = row[num].split('/')
                tempBuilding = tempBuilding[len(tempBuilding) - 1].upper()
                if tempBuilding == building:
                    lines.append(row)
    with open('../students/' + building + '.csv', mode='w') as student_file:
        for i in range(0,len(lines)):
            studentFile = csv.writer(student_file, delimiter=',')
            studentFile.writerow(lines[i])

def getBuilding():
    valid = False
    while not valid:
        buildingList = getBuildingNames()
        buildingList.append('ALL')
        building = input("Please enter the building wanted (" + str(', '.join(buildingList)) + "): ")
        building = building.upper()
        if building in buildingList:
            valid = True
            print("You chose", building)
            correct = input("Is that the correct building? (y/n) ")
            if correct.lower() != 'y':
                valid = False
            else:
                return building

def getBuildingNames():
    buildingList = []
    tempBuilding = []
    num = None
    with open('../needed_file/studentFull.csv', mode='r') as csv_file:
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
                if tempBuilding[len(tempBuilding) - 1] not in buildingList:
                    buildingList.append(tempBuilding[len(tempBuilding) - 1])
    return buildingList

main()
