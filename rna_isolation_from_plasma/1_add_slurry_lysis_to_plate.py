##SCRIPT TO TRANSFER SLURRY + LYSIS BUFFER TO 48 well PLATE
##TIME TO RUN: ~XX minutes

from opentrons import robot, containers, instruments

#PLATE SETUP
#Load custom containers using bug fix

#Pipette racks
racks = []
rack_slots = ["A2", "B2", "C2"]

for slot_i in rack_slots:
	racks.append(
		create_container_instance(
		    'rainin-tiprack-1200ul',
		    grid =(8,12), #cols,rows
		    spacing=(9.1,8.8), #mm spacing between each col,row
		    diameter=8,
		    depth=110, #depth mm of each well 
		    slot=slot_i
		)
	)

#Sample plates
plates = []
plate_slots = ["A1", "B1"]

for slot_i in plate_slots:
	plates.append(
		create_container_instance(
			'48-well-7mL-EK-2043',
			grid =(8,6), #cols,rows
			spacing=(9,18), #mm spacing between each col,row
			diameter=9,
			depth=65, #depth mm of each well 
			slot=slot_i
		)
	)

sample_rows = plates[0].rows()+plates[1].rows()

#Load trash
trash = containers.load('trash-box', 'E2')

#Load slurry, lysis buffer
slurry =  create_container_instance(
    '96-well-300mL-EK-2035-S',
    grid =(8,12), #cols,rows
    spacing=(8,8), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot='C1'
)

lysis =  create_container_instance(
    '96-well-300mL-EK-2035-S',
    grid =(8,12), #cols,rows
    spacing=(8,8), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot='D1'
)

p1200_multi = instruments.Pipette(
	axis='a',
	min_volume=100,
	max_volume=1200,
	trash_container=trash,
	tip_racks=racks,
	channels=8
)

#PROTOCOL
lysis_volume = 1800
p1200_multi.transfer(200, slurry.rows(), sample_rows, new_tip='always')
p1200_multi.transfer(1800, lysis.rows(), sample_rows, new_tip='always')
robot.comment("Run transfer_sample_tube_to_48_well_plate.py next to add plasma.")
