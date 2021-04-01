import subprocess

def main():
    building = getBuilding()

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

def getHeaderValues():


main()
