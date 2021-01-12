#!/bin/bash
##################################################################
# This script will compile the needed chargers for each chrome cart
# into csv files for MG Campus
##################################################################
# 20200716 Hartgrave
# - Initial roll out of script
##################################################################
# Note this script requires files that are not provided
# in the repository, that were generated using carts_script.sh
##################################################################
while true; do
	read -p "Please enter the building your desired cart resides in (ES, MS, HS, OMTC, ALC): " Building
	if ([ "$Building" == "ES" ] || [ "$Building" == "MS" ] || [ "$Building" == "HS" ] || [ "$Building" == "OMTC" ] || [ "$Building" == "ALC" ]);
	then
		echo "You chose "$Building""
		read -p "Is this correct? y/n: " _Yn
		if [ "$_Yn" == "y" ];
		then
			read -p "Please enter the number of carts you want to get charger data from: " NumCarts
			if [ "$NumCarts" -gt 1 ];
			then
				Counter=1;
				echo "Now going to get chargers for "$NumCarts" and write cart charger files"
				sleep 3
				mkdir chargers
				mkdir chargers/"$Building"
				while [ "$Counter" -le "$NumCarts" ];
				do
					CurrentCart=$(ls carts/"$Building" | grep "$Building"CB"$Counter".csv)
					if [ "$CurrentCart" == "" ];
					then
						break;
					else if [ "$CurrentCart" == ""$Building"CB"$Counter".csv" ];
					then
						cd chargers
						cp ../needed_file/chargers_template.csv "$Building"/"$Building"CB"$Counter"_chargers.csv
						cat ../carts/"$Building"/"$CurrentCart" | grep "$Building"CB"$Counter" | awk -F, '{print echo ""$7","$8","$3",charger,1"}' >> "$Building"/"$Building"CB"$Counter"_chargers.csv
					fi
					fi
					Counter=$((Counter+1))
					cd ../
				done
				exit
			else if [ "$NumCarts" -eq 1 ];
			then
				read -p "Please enter the name of the cart you want to pull charger data from: " CartName
				read -p "You want to pull charger data from cart "$CartName", is this correct? y/n" YesNo
				if [ "$YesNo" == "y" ];
				then
					echo "Getting charger data from cart "$CartName" and writing to file 'single/"$CartName"_chargers.csv'."
					sleep 3
					mkdir chargers
					cd chargers
					mkdir single
					cp ../needed_file/chargers_template.csv single/"$CartName"_chargers.csv
					cat ../carts/"$Building"/"$CartName".csv | grep "$CartName" | awk -F, '{print echo ""$7","$8","$3",charger,1"}' >> single/"$CartName"_chargers.csv
					break
				fi
			fi
			fi
		fi
	fi
done
exit
