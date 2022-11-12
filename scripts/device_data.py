import csv
import subprocess
import datetime


class Full_Device_Data:
    def __init__(self):
        self.filename = f"needed_file/full_devices.csv"
        subprocess.Popen(["touch",filename], stdout=subprocess.PIPE)

        self.write_data(self.filename)

    def write_data(self,filename):
        print("Now going to collect all device data from GAM")
        self.filename = filename
        with open(self.filename, mode='w') as self.o_file:
            self.write_out = subprocess.Popen(["gam","print","cros","full","query","status:provisioned"], stdout=self.o_file)
            self.write_out.wait()

class Wanted_Devices_Data:
    def __init__(self):
        self.header_list = [
            'deviceId',
            'autoUpdateExpiration',
            'serialNumber',
            'macAddress',
            'model',
            'orgUnitPath',
            #REMAINING SPACE ON DEVICE
        ]
        self.header_to_num = {}
        self.lines = []
        self.temp_row = []
        self.num = None
        
        self.create_file(self.header_list,self.header_to_num,self.lines,self.temp_row,self.num)
        
    def create_file(self,header_list,header_to_num,lines,temp_row,num):
        self.header_list = header_list
        self.header_to_num = header_to_num
        self.lines = lines
        self.temp_row = temp_row
        self.num = num
        
        with open("needed_file/full_devices.csv") as self.csv_file:
            self.csv_reader = csv.reader((line.replace('\0', '') for line in self.csv_file), csv_file, delimiter=',')
            self.n_col = len(next(self.csv_reader))
            self.csv_file.seek(0)
            self.line_count = 0
            for row in self.csv_reader:
                if self.line_count = 0:
                    for x in range(0,self.n_col):
                        self.col_name =  str(row[x])
                        if self.col_name in self.header_list:
                            self.num = self.header_to_num.update({self.col_name : x})
                    self.header_row = []


def main():
    Full_Device_Data()
    wanted_devices_data = Wanted_Devices_Data()


if __name__ == "__main__":
    main()