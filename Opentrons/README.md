# Running cfRNA extraction from plasma pipeline using Opentrons
Pipeline to run OT to process 96 samples as described in accompanying manuscript

***Takes ~4.5 hours on OT to run the entire pipeline. Process 48 samples at a time through Norgen kit and then pool for DNAse digestion and cleaning/concentrating (Zymo)***
***Uses 9 tip boxes total***

# Overview
* Can process up to 1 mL of plasma in each well of 48 well plate (Max vol 7.5 mL).
* Protocol run time relies on reagent setup (configuration), head speed (see setup.py), and plunger speed (see each ind. script)

# Getting started
* Install miniconda if you do not have it already
* Git clone this repo
* Change into this directory
* Create a virtual environment to run the associated launch script
		> conda env create -f env/ot.yaml
* Download OT app version 2.5.2 for OT1 via https://opentrons.com/ot-app/
* Copy the "run_cfRNA_pipeline.sh" provided in example/
* In run_cfRNA_pipeline.sh, change $ROOT_DIR specified as appropriate

# Setting up and calibrating OT1
* Follow manufacturer instructions. 
* See calibration file under "calibration/" for some starting positions. Note may need tweaking however its a good start for your calibration file
	* Copy that file over to "path_prefix/otone_data/calibrations/" where path_prefix can be found by opening the OT1 app, clicking File > Open Containers Folder, and navigating one folder out to find "calibrations/"
* Ensure proper calibration by using GUI portal for OT and checking that the specified positions work with the pipette hooked up

# Lab reagents required
* 8 channel 1.2 mL Rainin pipette (Rainin 17014496)
* Associated pipettes both 8 boxes standard length (Rainin 30389231) and 1 box long (Rainin 30389223)
* 8 or 12 channel 20 uL pipette and 3 boxes associated tips
* 2 48 well plates (Agilent 201236-100)
* 1 Norgen cfRNA purifiication kit (Norgen 29500)
* 1 Zymo clean and concentrate (Zymo R1080)
* 6 2 mL 96 deep well plate and prepared water balances (Thermo 278743)
* 4 2 column reservoirs, deep well, pyramid bottom (Agilent 203852-100)
* 2 12 column reservoirs, pyramid bottom (Agilent 201256-100)
* 100% Ethanol
* Baseline DNAse and master mix (Lucigen DB0715K)
* 96 well PCR plate with full skirt (Biorad HSP9631)

# Setup
* Make sure you have prepped reagents ahead of time (e.g. added 1.2% B-Met, and ethanol where needed).
* Preheat both lysis and slurry for at least 10 minutes [Make sure there is no precipitate. This will affect the protocol]. Vortex slurry for 1 minute intermittently to dissolve precipitated slurry.

# How to run
* Each month, check that all screws are tightly fastened on robot
* Thoroughly clean Opentrons robot. Careful not to bump pipettes though they should be solidly in place.
* Check calibrations using 0_calibration file - uncommenting and commenting for objects in the same physical position as needed
* Follow instructions in bash script. Pipette trash is ziploc bag. Liquid trash is old pipette box with top removed.
* Deploy bash script "run_cfRNA_pipeline.sh" to run pipeline as follows. Note that pipeline currently set up to process 1 mL samples and you will have to modify volumes to process other sample volumes.
		> bash <path_to_run_cfRNA_pipeline.sh> <expt_prefix>
* Log file can be found at "cfRNA_pipeline_automation/Opentrons/logs/expt_prefix.$DATETIME.log" where expt_prefix represents the argument you passed to the bash script above and $DATETIME represents the date and time the pipeline was run

# The steps
* Clean workspace thoroughly
* Thaw samples at room temp. Give enough space between samples so that they can more quickly thaw.
* Deploy bash script. This will process 48 samples.
	* First time through - run until it asks if you'd like to continue to Zymo processing. Here, select 0 (aka no). Place first 48 samples at 4C.
	* Rerun the same bash script to process the next 48 samples. Once you reach Zymo processing, select 1 (aka yes).
* Steps that require small volume pipetting will be done by hand.
	* Adding DNAse + Buffer master mix to samples
	* Adding 12.5 uL NF-H2O during final elution
	* Aliquoting final extracted RNA into barcoded plates for future library prep and qPCR

# Notes
* DO NOT use vacuum manifold - this results in inconsistent yields due to variable pull-through
* Prep all reagents before hand but no need to aliquot into plates.
* Make a spreadsheet to log experiment.
