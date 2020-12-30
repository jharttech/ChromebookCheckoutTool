#!/bin/bash
###############################################################
# This script will compile the needed chrome cart data into csv
# files for the MG Campus
###############################################################
# 20200707 Hartgraves
# - Initial roll out of script
# 20200716 Hartgraves
# - Updated awk call to adjust for import requirements
# 20200716 Hartgraves
# - Updated directory and file structures
# 20201230 Hartgraves
# - Adjusted this version of script for deprovisioned devices
###############################################################
# Note this script requires files from GAM that are not provided
# in the repository
###############################################################
while true; do
	read -p "Please enter the building wanted (ES, MS, HS, OMTC, ALC): " Building
	if ([ "$Building" == "ES" ] || [ "$Building" == "MS" ] || [ "$Building" == "HS" ] || [ "$Building" == "OMTC" ] || [ "$Building" == "ALC" ]);
	then
		echo "You chose "$Building""
		read -p "Is this correct? y/n: " _Yn
		if [ "$_Yn" == "y" ];
		then
			read -p "Please enter the number of carts you want: " NumCarts
			if [ "$NumCarts" -gt 1 ];
			then
				counter=1
				mkdir carts
				cd carts
				mkdir "$Building"
				mkdir "$Building"/"$Building"_Deprovisioned
				echo "Now going to get cart info and write cart files"
				sleep 3
				while [ "$counter" -le "$NumCarts" ];
				do
					cp ../needed_file/cart_template.csv "$Building"/"$Building"_Deprovisioned/"$Building"CB"$counter"_deprovisioned.csv # This line requires files from GAM
					cat ../needed_file/deprovisioned_full.csv | grep -w ""$Building"CB"$counter"" | awk -F, '{print "echo -n "$1",;echo -n $(date -d @$(("$35" / 1000)) +%Y%m%d);echo -n ,"$1450","$275","$276",initial import,"DEPROVISIONED","$276",chromebook,"; if (length($1450)>13) {print "echo "substr($1450,length($1450)-13,length($1450))}else{print "echo "$1450}}' | sh >> "$Building"/"$Building"_Deprovisioned/"$Building"CB"$counter"_deprovisioned.csv # This line requires files from GAM
					_lineCount=$(wc -l ""$Building"/"$Building"_Deprovisioned/"$Building"CB"$counter"_deprovisioned.csv")
					if [ "$_lineCount" == "1 "$Building"/"$Building"_Deprovisioned/"$Building"CB"$counter"_deprovisioned.csv" ];
					then
						rm "$Building"/"$Building"_Deprovisioned/"$Building"CB"$counter"_deprovisioned.csv
					fi
					counter=$((counter+1))
				done
				exit
			else if [ "$NumCarts" -eq 1 ];
			then
				read -p "Please enter the cart name you want: " CartName
				read -p "You want information for cart "$CartName", is that correct? y/n: " YesNo
				if [ "$YesNo" == "y" ];
				then
					echo "Getting information for cart "$CartName" and writing to file 'single/"$CartName".csv'."
					sleep 3
					mkdir carts
					cd carts
					mkdir single
					cp ../needed_file/cart_template.csv single/"$CartName"_deprovisioned.csv # This line requires files from GAM
					cat ../needed_file/deprovisioned_full.csv | grep -w ""$CartName"" | awk -F, '{print "echo -n "$1",;echo -n $(date -d @$(("$35" / 1000)) +%Y%m%d);echo -n ,"$1450","$275","$276",initial import,DEPROVISIONED,"$276",chromebook,"; if (length($1450)>13) {print "echo "substr($1450,length($1450)-13,length($1450))}else{print "echo "$1450}}' | sh >> single/"$CartName"_deprovisioned.csv # This line requires files from GAM
					break
				fi
			fi
			fi
		fi
	fi
done
exit
