import csv
import os
import subprocess

def main():
    getWantedData()

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
            with open('../needed_file/fullStudent.csv', mode='w') as student_file:
                for i in range(0,len(lines)):
                    studentFull = csv.writer(student_file, delimiter=',')
                    studentFull.writerow(lines[i])

def getStudentOU():
    studentBuilding = getBuilding()

def getBuilding():
    return

main()
