#!/bin/bash
ROOT_DIR=/Users/miramou/Documents/Grad/Lab/Projects/cfRNA_scale_up_test/Automation
DATETIME=$(date "+%Y_%m_%d_%H_%M_%S")
LOGFILE=$ROOT_DIR/log/cfRNA_extraction.$DATETIME.log

STEP_1=$ROOT_DIR/scripts/1_add_slurry_lysis_to_plate.py
STEP_2=$ROOT_DIR/scripts/2_transfer_sample_tube_to_48_well_plate.py
STEP_3=$ROOT_DIR/scripts/3_transfer_etoh_centrifuge_transfer_lysis.py
STEP_4=$ROOT_DIR/scripts/4_add_etoh_transfer_to_sample_plate.py

LYSIS_VOL=1800
ETOH_VOL=3000
SAMPLE_VOL=1000

echo "cfRNA plasma pipeline to run on opentrons"
echo $DATETIME

source activate py36
echo "Connect your computer using the USB port to the Opentrons robot"
read -p "Have you thoroughly cleaned the workstation using RNAse away and EtOH? (yes/no) " yn
while true; do
	case $yn in
		[Yy]* ) make install; break;;
		[Nn]* ) exit;;
		* ) echo "Please answer yes or no.";;
	esac
done

read -p "Check the positions of: Tip boxes: C2, D2. Slurry: A1. Lysis: C1. Sample plates: B1, B2. Trash: A2. (yes/no)" yn
while true; do
	case $yn in
		[Yy]* ) make install; break;;
		[Nn]* ) exit;;
		* ) echo "Please answer yes or no.";;
	esac
done
python STEP_1 $LYSIS_VOL

read -p "Check the positions of: Tip boxes: C2. A-D Plasma: A1. E-H Plasma: C1. Sample plate 1: B1. Trash: A2. (yes/no)" yn
while true; do
	case $yn in
		[Yy]* ) make install; break;;
		[Nn]* ) exit;;
		* ) echo "Please answer yes or no.";;
	esac
done
python STEP_2 $SAMPLE_VOL

read -p "Check the positions of: Tip boxes: C2. A-D Plasma: A1. E-H Plasma: C1. Sample plate 2: B1. Trash: A2. (yes/no)" yn
while true; do
	case $yn in
		[Yy]* ) make install; break;;
		[Nn]* ) exit;;
		* ) echo "Please answer yes or no.";;
	esac
done
python STEP_2 $SAMPLE_VOL


read -p "Check the positions of: Tip boxes: C2, D2, E2. EtOH: A1. Lysis: C1. Sample plates: B1, D1. Trash: A2. (yes/no)" yn
while true; do
	case $yn in
		[Yy]* ) make install; break;;
		[Nn]* ) exit;;
		* ) echo "Please answer yes or no.";;
	esac
done
python STEP_3 $ETOH_VOL

read -p "Check the positions of: Tip boxes: C2, D2, E2. EtOH: A1. Final plate: C1. Sample plates: B1, D1. Trash: A2. (yes/no)" yn
while true; do
	case $yn in
		[Yy]* ) make install; break;;
		[Nn]* ) exit;;
		* ) echo "Please answer yes or no.";;
	esac
done
python STEP_4
