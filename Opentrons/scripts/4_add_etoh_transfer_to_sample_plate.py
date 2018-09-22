##SCRIPT TO TRANSFER EtOH TO 48 well PLATE AND TRANSFER TO 96 well PLATE
##TIME TO RUN: ~15-20 minutes
##TOTAL TIPS USED: 1 boxes

from opentrons import robot, containers, instruments
from setup import *
from datetime import datetime

#PLATE SETUP
#Load custom containers using bug fix

#Pipette racks
racks = []
rack_slots = ["E1"]

for slot_i in rack_slots:
	racks.append(
		create_container_instance(
		    'rainin-tiprack-1200ul',
		    grid =(8,12), #cols,rows
		    spacing=(9,9), #mm spacing between each col,row
		    diameter=8,
		    depth=110, #depth mm of each well 
		    slot=slot_i
		)
	)
	
#Sample plates
plates = []
plate_slots = ["B2"]

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
    '96-well-Norgen-filter',
    grid =(8,12), #cols,rows
    spacing=(8.8,8.8), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot='B1'
)

#Load trash
trash = containers.load('trash-box', 'D2')

#Load etoh
lysis_etoh =  create_container_instance(
    '96-well-252mL-EK-2034-S-12-Col-Divided',
    grid =(8,12), #cols,rows
    spacing=(9,9), #mm spacing between each col,row
    diameter=8,
    depth=45, #depth mm of each well 
    slot='A2'
)

p1200_multi = instruments.Pipette(
	axis='a',
	min_volume=100,
	max_volume=1000,
	trash_container=trash,
	tip_racks=racks,
	channels=8,
    aspirate_speed=600,
    dispense_speed=700
)

#PROTOCOL
start = datetime.now()
print("Step 4: Add ethanol and transfer to 96-well plate")
print("%s" % (start))

row_96 = 1
src_row = 7

for i in range(2):
#Just under 6 min per plate

    robot.pause()
    check = input("Plate plate %s at position B2 after incubation. Remove seal. Remove seal from reservoir column %s at A2. Place filter plate + Axygen base at B1. Empty trash. Press enter to continue with EtOH addition + mixing. " % (i+1, src_row))
    robot.resume()

    loop_start = datetime.now()

    for row_48 in plates[0].rows():
        p1200_multi.pick_up_tip()

        p1200_multi.transfer(300, 
            lysis_etoh.rows(str(src_row)), 
            row_48.bottom(),
            air_gap = 20,
            new_tip="never",
        )

        p1200_multi.mix(5, 450, row_48.bottom(-2))
        robot.home("z")

        robot.pause()
        check = input("Seal and vortex. Press enter to continue. ")
        robot.resume()

        p1200_multi.aspirate(900, row_48.bottom(-4.2), rate=0.25) ## Consider this by hand since it seems like I cant get all the resin? Or put in a pause here and put it on a plate shaker
        p1200_multi.air_gap(20)
        p1200_multi.dispense(920, final_plate.rows(str(row_96)).bottom(12))
        p1200_multi.blow_out()

        p1200_multi.drop_tip()

        row_96 += 1

    print("Loop completion time: %s" % (datetime.now()-loop_start))

    if i==0:
        src_row += 1

    robot.home()

print("Total time: %s" % (datetime.now()-start))
robot.home()
