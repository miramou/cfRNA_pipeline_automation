# Running cfRNA extraction from plasma pipeline using Opentrons
***Takes ~6 hours on OT to run the entire pipeline. Process 48 samples at a time through Norgen kit and then pool for DNAse and Zymo***
***Uses 9 tip boxes total***

# Overview
* Implements all steps up to using filter plate to clean up cfRNA extracted using Norgen kit, DNase treatment, and Zymo kit. 
* Can process up to 1 mL of plasma in each well of 48 well plate (Max vol 7.5 mL).
* Protocol run time relies on reagent setup (configuration), head speed (see setup.py), and plunger speed (see each ind. script)

# Setup
* Make sure you have prepped reagents ahead of time (e.g. added 1.2% B-Met and 1:1000 ERCC to lysis buffer).
* Preheat both lysis and slurry for at least 10 minutes [Make sure there is no precipitate. This will affect the protocol]. Vortex slurry for 1 minute intermittently to dissolve precipitated slurry.

# How to run
* Each month, check that all screws are tightly fastened on robot
* Thoroughly clean Opentrons robot. Careful not to bump pipettes though they should be solidly in place.
* Check calibrations using 0_calibration file - uncommenting and commenting for objects in the same physical position as needed
* Follow instructions in bash script. Pipette trash is ziploc bag. Liquid trash is old pipette box with top removed.
* Deploy bash script "run_cfRNA_pipeline.sh" to run pipeline (Note that pipeline currently set up to process 1 mL samples.)
	* Deploy bash script "run_cfRNA_pipeline_750uL.sh" for 0.75 mL volumes
* Indicate log file to record steps

# The steps
* Clean workspace thoroughly
* Thaw samples at room temp or in incubator with door open. Give enough space between samples so that they can more quickly thaw.
* Deploy bash script. This will process 48 samples.
	* First time through - run until it asks if you'd like to continue to Zymo processing. Here, select 0 (aka no). Place samples at 4C.
	* Rerun the same bash script to process the next 48 samples. Once you reach Zymo processing, select 1 (aka yes).
* Steps that require small volume pipetting will be done by hand.
	* Adding DNAse + Buffer master mix to samples
	* Adding 12.5 uL NF-H2O during final elution
	* Aliquoting final extracted RNA into barcoded plates for future library prep and qPCR

# Notes
* DO NOT use vacuum manifold - this results in inconsistent yields due to variable pull-through
* Make sure centrifuge is at 4C
* Prep all reagents before hand but no need to aliquot into plates.
* Make a spreadsheet to log experiment.
