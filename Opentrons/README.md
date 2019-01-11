THIS README IS OLD AND NEEDS UPDATING :) TO BE UPDATED SOON

# Running cfRNA extraction from plasma pipeline using Opentrons
***Takes ~1.5 hours followed by 1.5 hours on Bravo.***
***Uses 7 tip boxes total***

# Overview
* Implements all steps up to using filter plate to clean up cfRNA extracted using Norgen kit. 
* Can process up to 1 mL of plasma in each well of 48 well plate (Max vol 7.5 mL).
* Protocol run time relies on reagent setup (configuration), head speed (see setup.py), and plunger speed (see each ind. script)

# Setup
* Make sure you have prepped reagents ahead of time (e.g. added 1.2% B-Met and 1:1000 ERCC to lysis buffer).
* Preheat both lysis and slurry for 10 minutes. Vortex slurry for 1 minute intermittently to dissolve precipitated slurry.
* Note that slurry, lysis buffer (Script 5), and EtOH (Script 4) all go in same 12 col divided reservoir:
	* Seal all columnns with plate sticker - remove plate sticker incremently when reagent is needed.
	* Slurry in Col 1,2 (12 mL each col) Wait for script to tell you to add to second plate. Slurry easily solidifies
	* Lysis buffer in Col 4,5 (20 mL each col)
	* EtOH in Col 7,8 (20 mL each col)

# How to run
* Each month, check that all screws are tightly fastened on robot
* Thoroughly clean Opentrons robot. Careful not to bump pipettes though they should be solidly in place.
* Check calibrations using 0_calibration file - uncommenting and commenting for objects in the same physical position as needed
* Line trash at D1 (liquid) and D2 (pipettes) with ziploc bags. Also add a few absorbent paper towels to D1. 
* Deploy bash script "run_cfRNA_pipeline.sh" to run pipeline (Note that pipeline currently set up to process 1 mL samples. Change buffer volumes if needed)

# The steps
* Refrigerate sample blocks
* Clean workspace thoroughly
* Thaw samples at room temp
* At the same time, run 1_add_slurry_lysis_to_plate.py
	* This script adds slurry and lysis buffer to 2 clean 48-well plates. 
* Run 2_transfer_sample_tube_to_48_well_plate.py to transfer samples.
* Run 3_transfer_etoh_centrifuge_remove_sup.py.
	* This script expects you to multitask with the robot. It will tell you when you should interface.
		* For instance, you might mix EtOH with sample for plate B1 as it adds reagent to plate B2. This is for speed.
	* You will seal and incubate plate 1 at 60C while plate 2 is being processed.
	* Decanting step has been optimzed and removes all supernatant with almost none remaining.
* Run 4_add_etoh_transfer_to_sample_plate.py
	* Start plate 1 immediately after it completes incubation at 60C. 
	* Protocol will wait for you to place plate 2 prior to starting that plate
* Once completed, go to Bravo to continue clean-up protocol. Bravo steps + vacuum manifold take ~1.5 hours
