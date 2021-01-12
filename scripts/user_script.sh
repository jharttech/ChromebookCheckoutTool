#!/bin/bash
################################################
# This script will compile the needed student info
# files for the MG Campus
################################################
# 20200720 Hartgraves
# - Initial roll out of script
################################################
# Note this script requires files from GAM that are
# not provided in the repository
################################################
while true; do
	read -p "Please enter the OU you want student data from: " OrgUnit
	if ([ "$OrgUnit" == "MGES" ] || [ "$OrgUnit" == "MGHS" ] || [ "$OrgUnit" == "MGMS" ] || [ "$OrgUnit" == "ALC" ] || [ "$OrgUnit" == "OMTC" ] || [ "$OrgUnit" == "RISE" ]);
	then
		read -p "You chose "$OrgUnit", is this correct? y/n " _Yn
		if [ "$_Yn" == "y" ];
		then
			#if [ "$OrgUnit" == "ALC" ];
			#then
				#OrgUnit=$((MGHS/ALC))
				#break
			#else if [ "$OrgUnit" == "RISE" ];
			#then
				#OrgUnit=$((MGMS/RISE))
				#break
			#fi
			#fi
			echo "Now going to gather student info and write to files."
			sleep 3
			mkdir students
			cd students
			mkdir $OrgUnit
			cp ../needed_file/studentUser_template.csv "$OrgUnit"/"$OrgUnit".csv
			cat ../needed_file/full_student.csv | grep "$OrgUnit" | awk -F, '{split($1,z,"@"); print echo ""$1","$24","$22","$25",,"z[1]}' >> "$OrgUnit"/"$OrgUnit".csv
			break
		fi
	fi
done
exit
