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
read -p "Have you thoroughly cleaned the workstation using Bleach, EtOH, and RNAse away in that order? (y/n) " yn
while true; do
	case $yn in
		[Yy]* ) break;;
		* ) read -p "Please clean space and then enter yes. " yn;;
	esac
done

read -p "Check the positions of: Tip boxes: Slurry: A1. Lysis: A2. Sample plates: B1, B2. Trash: D1. Type go to start 1_add_slurry_lysis_to_plate. " go
while true; do
	case $go in
		[Gg]* ) break ;;
		* ) read -p "Please enter go when you've confirmed object locations " go;;
	esac
done

python $STEP_1 $LYSIS_VOL

read -p "Add sample, mix, and incubate for 10 min at 60C by hand using variably spaced 1.2 mL multichannel pipeptte. Type go once completed. " go
while true; do
	case $go in
		[Gg]* ) break ;;
		* ) read -p "Please enter go when you've completed the task. " go;;
	esac
done

# python $STEP_2 $SAMPLE_VOL

read -p "Check the positions of: Tip boxes: E1, E2. EtOH: A1. Lysis: A2. Sample plates: B1, B2. Trash: D1. Type go to start 3_transfer_etoh_centrifuge_transfer_lysis. " go
while true; do
	case $go in
		[Gg]* ) break ;;
		* ) read -p "Please enter go when you've confirmed object locations " go;;
	esac
done

python $STEP_3 $ETOH_VOL 

read -p "Check the positions of: Tip boxes: E1, E2. EtOH: A2. Final plate: A1. Sample plates: B1, B2. Trash: D1. Type go to start 4_add_etoh_transfer_to_sample_plate. " go
while true; do
	case $go in
		[Gg]* ) break ;;
		* ) read -p "Please enter go when you've confirmed object locations " go;;
	esac
done

python $STEP_4
