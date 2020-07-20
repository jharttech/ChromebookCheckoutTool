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
	if ([ "$OrgUnit" == "FIXME" ] || [ "$OrgUnit" == "FIXME" ] || [ "$OrgUnit" == "FIXME" ] || [ "$OrgUnit" == "FIXME" ] || [ "$OrgUnit" == "FIXME" ] || [ "$OrgUnit" == "FIXME" ]);
	then
		read -p "You chose "$OrgUnit", is this correct? y/n " _Yn
		if [ "$_Yn" == "y" ];
		then
			echo "Now going to gather student info and write to files."
			sleep 3
			mkdir students
			cd students
			mkdir $OrgUnit
			cp ../studentUser_template.csv "$OrgUnit"/"$OrgUnit".csv
			cat ../needed_file/full_student.csv | grep "$OrgUnit" | awk -F, '{split($1,z,"@"); print echo ""$1","$25","$23","$26",,"z[1]}' >> "$OrgUnit"/"$OrgUnit".csv # This line requires files from GAM
			break
		fi
	fi
done
exit
