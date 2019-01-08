##SCRIPT TO TRANSFER PLASMA SAMPLES TO 48 well PLATE
##TIME TO RUN: ~20 minutes per plate - 40 minutes total
##TOTAL TIPS USED: 2 boxes

from opentrons import robot, containers, instruments
from setup import *
from datetime import datetime
import sys

#PLATE SETUP
#Load vial racks
vial_rack = containers.load('24-vial-rack', "B1")

#Load custom containers using bug fix
racks = []
rack_slots = ["C1"]

for slot_i in rack_slots:
	racks.append(
		create_container_instance(
		    'rainin-tiprack-1200ul',
		    grid =(8,12), #cols,rows
		    spacing=(9.08,8.9), #mm spacing between each col,row
		    diameter=8,
		    depth=200, #depth mm of each well 
		    slot=slot_i
		)
	)

plate = create_container_instance(
    '48-well-7mL-EK-2043',
    grid =(8,6), #cols,rows
    spacing=(9,18), #mm spacing between each col,row
    diameter=9,
    depth=65, #depth mm of each well 
    slot="B2"
)

#Load trash
trash = containers.load('trash-box', 'C2')

p1000 = instruments.Pipette(
	axis='b',
	min_volume=100,
	max_volume=1000, 
	trash_container=trash,
	tip_racks=racks,
	channels=1,
    aspirate_speed=800,
    dispense_speed=1000
)

p1200_multi = instruments.Pipette(
	axis='a',
	min_volume=100,
	max_volume=1000,
	trash_container=trash,
	tip_racks=racks,
	channels=8,
    aspirate_speed=800,
    dispense_speed=1000
)

#PROTOCOL
sample_volume = float(sys.argv[1])
dest_well_list = ["A1", "A2", "A3", "A4", "A5", "A6", "B1", "B2", "B3", "B4", "B5", "B6", "C1", "C2", "C3", "C4", "C5", "C6", "D1", "D2", "D3", "D4", "D5", "D6",
				"E1", "E2", "E3", "E4", "E5", "E6","F1", "F2", "F3", "F4", "F5", "F6", "G1", "G2", "G3", "G4", "G5", "G6", "H1", "H2", "H3", "H4", "H5", "H6"]

start = datetime.now()
print("Step 2: Sample transfer protocol")
print("%s" % (start))

for i in range(1):

	robot.pause()
	check = input("Add 48-well sample plate %s to B2. Place first sample rack at position B1. Place clean tips at position C1. Make sure trash is empty. Press enter to continue. " % (i+1))
	robot.resume()

	for well in range(0,48):

		#loop_start = datetime.now()

		src_well_idx = get_source_idx(well)
		dest_well_idx = dest_well_list[well]

		p1000.pick_up_tip()

		p1000.transfer(sample_volume, 
			vial_rack.wells(src_well_idx), 
			plate.wells(dest_well_idx).bottom(),
			new_tip="never",
		)

		p1000.drop_tip()
		#print("Time for loop completion: %s" % (datetime.now() - loop_start))

		if well == 23:
			robot.pause()
			check = input("Please place second sample rack at position B1. Press enter to continue. ")
			robot.resume()

	robot.home()
	
	# robot.pause()
	# check = input("Remove sample rack from position B1. Press enter to continue. ")
	# robot.resume()

	# p1200_multi.start_at_tip(racks[0].rows(6))

	# loop_start = datetime.now()
	# ## Takes about 4 minutes to mix plate

	# for row in plate.rows():
	# 	p1200_multi.pick_up_tip()
	# 	p1200_multi.mix(6, 1000, row.bottom())
	# 	p1200_multi.drop_tip()

	print("Time for loop completion: %s" % (datetime.now() - loop_start))


print("Total time: %s" % (datetime.now()-start))
print("Seal and incubate for 10 min at 60C.")


	