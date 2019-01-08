##SCRIPT TO ADD WASH BUFFER 3X TO NORGEN FILTER and ELUTE
##TIME TO RUN: ~5.5 minutes + 22 minutes centrifuge/vacuum
##TOTAL TIPS USED: 4 rows

from opentrons import robot, containers, instruments
from setup import *
from datetime import datetime
import sys

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
		    depth=150, #depth mm of each well 
		    slot=slot_i
		)
	)
	

#Load filter plate
plate_slots = ["B1", "B2"]
filter_plates = []

for slot_i in plate_slots:
    filter_plates.append(
        create_container_instance(
            '96-well-Norgen-filter',
            grid =(8,12), #cols,rows
            spacing=(8.8,8.8), #mm spacing between each col,row
            diameter=8,
            depth=15, #depth mm of each well 
            slot=slot_i
        )
    )

#Load trash
trash = containers.load('trash-box', 'D2')

#Load wash
wash =  create_container_instance(
    '96-well-150mL-EK-2299-2-Col-Divided',
    grid =(8,2), #cols,rows
    spacing=(9,54), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot='A1'
)

elution =  create_container_instance(
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
print("Step 5: Wash filter plate and elute")
print("%s" % (start))

src_row = 1 #wash source row
elu_src_row = 7

start_row = int(sys.argv[1])
last_row = int(sys.argv[2])+1

for i in range(4):
#Just under 5.5 min per plate
    
    loop_start = datetime.now()

    if i < 3:
        print("Wash %s" % (i+1))

        robot.pause()
        check = input("Place filter plate at position B1 after centrifugation. Remove seal from 2-column wash plate at A1 and add 24 mL wash. Empty trash. Press enter to continue with wash addition. ")
        robot.resume()

        p1200_multi.pick_up_tip()

        for row_i in range(start_row,last_row):

            p1200_multi.transfer(400, 
                wash.rows(str(src_row)), 
                filter_plates[0].rows(str(row_i)).bottom(22), 
                air_gap = 20,
                new_tip="never",
            )

        p1200_multi.drop_tip()

        robot.pause()
        if i<2:
            print("Apply vacuum for 3 minutes. Add 24 mL wash buffer to 2-column wash reservoir at col 1. ")
        else:
            print("Apply vacuum for 3 minutes. Pat bottom. Centrifuge for 5 minutes at max speed. ")
        robot.resume()

    else:
        ## Elute
        robot.pause()
        check = input("Add 8 mL elution buffer to position %s in 12 column reservoir at A2. Move filter plate to B2. Press enter to continue. " % (elu_src_row))
        robot.resume()

        p1200_multi.pick_up_tip()

        for row_i in range(start_row, last_row):

            p1200_multi.transfer(120,
                elution.rows(str(elu_src_row)),
                filter_plates[1].rows(str(row_i)).bottom(22),
                air_gap = 20,
                new_tip = "never"
            )

        p1200_multi.drop_tip()

    
    print("Loop completion time: %s" % (datetime.now()-loop_start))
    print()

print("Total time: %s" % (datetime.now()-start))
print("Centrifuge at max speed for 6 minutes. ")
robot.home()
