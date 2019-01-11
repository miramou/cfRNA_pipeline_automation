#!/bin/bash
(
ROOT_DIR=/Users/miramou/Documents/Grad/Lab/Projects/cfRNA_scale_up_test/Automation/Opentrons
DATETIME=$(date "+%Y_%m_%d_%H_%M_%S")
LOG_FILE=$ROOT_DIR/logs/$1.$DATETIME.log

STEP_1=$ROOT_DIR/scripts/48_format/1_add_slurry_lysis_to_plate.py
STEP_3=$ROOT_DIR/scripts/48_format/3_transfer_etoh_centrifuge_remove_sup_add_etoh.py
STEP_4=$ROOT_DIR/scripts/48_format/4_transfer_to_sample_plate.py
STEP_5=$ROOT_DIR/scripts/48_format/5_norgen_add_wash_buffer_elute.py
STEP_6=$ROOT_DIR/scripts/48_format/6_zymo_clean_conc.py

LYSIS_VOL=1800
ETOH_VOL=3000
START_ROW=1
STOP_ROW=6

echo "cfRNA plasma pipeline to run on opentrons"
echo $DATETIME

source activate py36

if [ $# -eq 0 ]
	then
		#nothing happens
		echo "Please type in log file path to start. "
else
	python $STEP_1 $LYSIS_VOL | tee -a "$LOG_FILE"
	echo

	read -p "Step 2: Add samples manually, mix, and incubate. Type y once ready to proceed. " yn
	while true; do
		case $yn in
			[Yy]* ) break;;
			* ) read -p "Type y to proceed. " yn;;
		esac
	done

	python $STEP_3 $ETOH_VOL | tee -a "$LOG_FILE"
	echo
	read -p "Which filter row to start at? " FILTER_ROW 
	while true; do
		case $FILTER_ROW in
			[1]* ) break ;;
			[7]* ) break ;;
			* ) read -p "Enter row 1 or 7 (depending on if first or second plate). " FILTER_ROW;;
		esac
	done
	python $STEP_4 $FILTER_ROW | tee -a "$LOG_FILE"
	echo

	python $STEP_5 $START_ROW $STOP_ROW | tee -a "$LOG_FILE"
	echo

	read -p "Proceed to Zymo? (0/1) " if_zymo
	while true; do
		case $if_zymo in
			[0]* ) break ;;
			[1]* ) break ;;
			* ) read -p "Enter 1 (yes) or 0 (no).  " if_zymo;;
		esac
	done

	if [ $if_zymo -eq 1 ]
		then
			read -p "Which Zymo row to stop at ? " ZYMO_STOP 
			while true; do
				case $ZYMO_STOP in
					[1-9]* ) break ;;
					1[0-2]* ) break ;;
					* ) read -p "Enter row between 1 and 12. " ZYMO_STOP;;
				esac
			done
			python $STEP_6 $START_ROW $ZYMO_STOP | tee -a "$LOG_FILE"
	fi
fi

echo
echo
echo "All done ! :)"

) 2>&1 | tee $LOG_FILE