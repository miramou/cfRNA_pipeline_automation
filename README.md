# Running cfRNA extraction from plasma pipeline using Opentrons
## Takes ~1.5 hours followed by 1.5 hours on Bravo.

* Implements all steps up to using filter plate to clean up cfRNA extracted using Norgen kit. 
* Can process up to 1 mL of plasma in each well of 48 well plate (Max vol 7.5 mL).
* Keep your eye on the robot! Sometimes tips dont come off all the way (rarely) and you need to step in. This is the only somewhat difficult step to watch for
* The slowest steps on this robot are by far moving the pipette over. The motors are slow so this has been optimized to reduce the number of large movements like tips on/tips off

#How to run
* Thoroughly clean Opentrons robot and check calibrations using 0_calibration file - uncommenting and commenting for objects in the same physical position as needed
* Deploy bash script "run_cfRNA_pipeline.sh" to run pipeline (Note that pipeline currently set up to process 1 mL samples. Change buffer volumes if needed)

#The steps
* Clean workspace thoroughly
* Thaw samples at room temp
* At the same time, run 1_add_slurry_lysis_to_plate.py
	* This script adds slurry and lysis buffer to 2 clean 48-well plates. 
* Add samples by hand using variably spaced 1.2 mL multichannel. The included script takes too long
* Run 3_transfer_etoh_centrifuge_transfer_lysis.py
	* This script expects you to multitask with the robot. It will tell you when you should interface.
		* For instance, you might mix EtOH with sample for plate B1 as it adds reagent to plate B2. This is for speed.
	* You will seal and incubate plate 1 at 60C while plate 2 is being processed.
	* Carefully watch decanting step. The height of the pipette has yet to be optimizedy
* Run 4_add_etoh_transfer_to_sample_plate.py
	* Start plate 1 immediately after it completes incubation at 60C. 
	* Protocol will wait for you to place plate 2 prior to starting that plate
* Once completed, go to Bravo to continue clean-up protocol. Bravo steps + vacuum manifold take ~1.5 hours
