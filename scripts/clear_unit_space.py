import subprocess
import csv


class Stage_CSV:
    def __init__(self):
        self.g_headers = [
            "deviceId",
            "diskVolumeReports.0.volumeInfo.0.storageFree",
            "diskVolumeReports.0.volumeInfo.0.storageTotal",
            "orgUnitPath",
            "serialNumber"
        ]

        self.header_to_num = {}
        self.lines = []
        self.i_filename = "full_devices.csv"
        self.result = self.stage()

    def stage(self):
        with open(f"needed_file/{self.i_filename}", mode="r") as self.csv_file_read:
            self.csv_reader = csv.reader((line.replace('\0','') for line in self.csv_file_read), self.csv_file_read, delimiter=",")
            self.n_col = len(next(self.csv_reader))
            self.csv_file_read.seek(0)
            self.line_count = 0

            for row in self.csv_reader:
                if self.line_count == 0:
                    for x in range(0,self.n_col):
                        self.col_name = str(row[x])
                        if self.col_name in self.g_headers:
                            self.header_to_num.update({self.col_name: x})
                    self.line_count += 1
                else:
                    try:
                        self.temp_row = [
                            row[
                                self.header_to_num.get("deviceId", "Error getting header number for deviceId")
                            ],
                            row[
                                self.header_to_num.get("diskVolumeReports.0.volumeInfo.0.storageTotal", "Error getting header number for diskVolumeReports.0.volumeInfo.0.storageTotal")
                            ],
                            row[
                                self.header_to_num.get("diskVolumeReports.0.volumeInfo.0.storageFree", "Error getting header number for diskVolumeReports.0.volumeInfo.0.storageFree")
                            ],
                            row[
                                self.header_to_num.get("orgUnitPath", "Error geting header number for orgUnitPath")
                            ],
                            row[
                                self.header_to_num.get("serialNumber", "Error getting header number")
                            ]
                        ]
                        if ("staff" in str(self.temp_row[3])):
                            self.result = "FOUND"
                            return self.result
                    except:
                        ...

        def __str__(self):
            return f"{self.result}"
            

def main():
    stage = Stage_CSV()
    print(stage)


if __name__ == "__main__":
    main()