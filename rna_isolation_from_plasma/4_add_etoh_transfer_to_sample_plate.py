##SCRIPT TO TRANSFER EtOH TO 48 well PLATE AND TRANSFER TO 96 well PLATE
##TIME TO RUN: ~XX minutes

from opentrons import robot, containers, instruments
from setup import *
from datetime import datetime

#PLATE SETUP
#Load custom containers using bug fix

#Pipette racks
racks = []
rack_slots = ["E1", "E2"]

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
plate_slots = ["B1", "B2"]

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

#Load final plate
final_plate = create_container_instance(
    '96-well-1mL-Axygen',
    grid =(8,12), #cols,rows
    spacing=(8,8), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot='A1'
)

#Load trash
trash = containers.load('trash-box', 'D1')

#Load etoh
etoh =  create_container_instance(
    '96-well-300mL-EK-2035-S',
    grid =(8,12), #cols,rows
    spacing=(8,8), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot='A2'
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
start = datetime.now()
print("Step 4: Add ethanol and transfer to 96-well plate")
print("%s" % (start))

src_row=1
for i in range(2):
    for dst_row in plates[i].rows():

        p1200_multi.transfer(300, 
            etoh.rows(str(src_row)), 
            dst_row.bottom(),
            new_tip="always",
            trash=False
        )

        src_row += 1

robot.home()

dst_row = 1
for i in range(2):
    for src_row in plates[i].rows():
        p1200_multi.transfer(800, 
            src_row, 
            final_plate.rows(str(dst_row)), 
            mix_before=(10,400),
            new_tip="always", 
            trash=False
        )

        dst_row += 1

print("Total time: %s" % (datetime.now()-start))
