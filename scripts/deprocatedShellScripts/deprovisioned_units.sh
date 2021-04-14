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
_NewFile="$(date +%Y_%m_%d_%H%M%S)_depro_mast.csv"
cd carts
mkdir Deprovisioned
cd Deprovisioned
_Rotate=$(ls | grep master)
if [ "$_Rotate" == "deprovisioned_master.csv" ];
then
	cp deprovisioned_master.csv "$_NewFile"
fi
cp ../../needed_file/cart_template.csv deprovisioned_master.csv #This line requires files from GAM
cat ../../needed_file/deprovisioned_full.csv | awk -F, '{print "echo -n "$1",;echo -n $(date -d @$(("$35" / 1000)) +%Y%m%d);echo -n ,"$1464","$289","$290",initial import,"DEPROVISIONED","$290",chromebook,"; if (length($1464)>13) {print "echo "substr($1464,length($1464)-13,length($1464))}else{print "echo "$1464}}' | sh >> deprovisioned_master.csv # This line requires files from GAM
exit
