#!/bin/bash
#####################################################
# This script will help in recording hotspot info for
# the MG Campus
#####################################################
# 20200720 Hartgraves
# - Initial roll out of script
#####################################################
while true; do
	read -p "Please enter the amount of hotspots you would like to add to campus: " ItemCount
	read -p "Please enter purchase date in ISO format (ex. 20200720): " IsoDate
	read -p "Please enter the Manufacturer of the hotspots: " Manufacturer
	read -p "Please enter the Brand of the hotspots: (ex. Moxee) " Brand
	read -p "Please enter the Purchase Cost of each hotspot: " Cost
	read -p "Please enter the PO Number used to purchase the hotspots: " PONum
	read -p "You have entered an amount of "$ItemCount" "$Brand" made by "$Manufacturer" hotspots purchased on "$IsoDate", with a cost of "$Cost" each, using PO Number "$PONum". Is that correct? y/n " _Yn
	if [ "$_Yn" == "y" ];
	then
		Counter=1
		mkdir hotspots
		cd hotspots
		FileName="$IsoDate"-PO"$PONum"-hotspots.csv
		touch $FileName
		touch errorLog.txt
		FirstRun=$(ls | grep hotspot_master_list.csv)
		while [ "$FirstRun" == "" ];
		do
			cp ../needed_file/hotspot_template.csv hotspot_master_list.csv
			FirstRun=$(ls | grep hotspot_master_list.csv)
		done
		cp ../needed_file/hotspot_template.csv "$FileName"
		while [ "$Counter" -le "$ItemCount" ];
		do
			echo "Now going to ask for information specific to each hotspot."
			sleep 3
			read -p "Please enter the Serial Number (with no spaces) for hotspot "$Counter": " SerialNum
			read -p "Please enter the Sim Card Number (with no spaces) for hotspot "$Counter": " SimNum
			read -p "You have entered Serial Number "$SerialNum" and Sim Card Number "$SimNum", is that correct? y/n " YesNo
			if [ "$YesNo" == "y" ];
			then
				Duplicate=$(cat hotspot_master_list.csv | grep "$SerialNum")
				if [ "$Duplicate" != "" ];
				then
					TimeStamp=$(date +%Y_%m_%d_%H%M%S)
					echo "Duplicate detected with Serial Number "$SerialNum"! Skipping entry. Please check 'errorLog.txt' for information."
					echo ""$TimeStamp" POSSIBLE DUPLICATE: " >> errorLog.txt
					echo "     hotspot,"$Brand",MG Schools,"$Manufacturer","$IsoDate","$Cost","$PONum","$SerialNum","$SerialNum","$SimNum"" >> errorLog.txt
					sleep 4
					Counter=$((Counter+1))
					break
				fi
				if [ "$Duplicate" == "" ];
				then
					echo "hotspot,"$Brand",MG Schools,"$Manufacturer","$IsoDate","$Cost","$PONum","$SerialNum","$SerialNum","$SimNum"" >> "$FileName"
					echo "hotspot,"$Brand",MG Schools,"$Manufacturer","$IsoDate","$Cost","$PONum","$SerialNum","$SerialNum","$SimNum"" >> hotspot_master_list.csv
					Counter=$((Counter+1))
					break
				fi
				break
			fi
		done
		break
	fi
done
exit

