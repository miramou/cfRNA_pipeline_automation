##SCRIPT TO ZYMO CLEAN AND CONCENTRATE
##TIME TO RUN: ~27 minutes (with centrifugation)
##TOTAL TIPS USED: 11 rows

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
	

#Load sample plate
sample_plate = create_container_instance(
    '96-well-Axygen',
    grid =(8,12), #cols,rows
    spacing=(8.8,8.8), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot="B2"
)


#Load filter plate
filter_plate = create_container_instance(
    '96-well-Zymo-filter',
    grid =(8,12), #cols,rows
    spacing=(8.8,8.8), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot="B1"
)

#Load trash
trash = containers.load('trash-box', 'D2')

#Load wash
binding_etoh =  create_container_instance(
    '96-well-252mL-EK-2034-S-12-Col-Divided',
    grid =(8,12), #cols,rows
    spacing=(9,9), #mm spacing between each col,row
    diameter=8,
    depth=45, #depth mm of each well 
    slot='A2'
)

wash =  create_container_instance(
    '96-well-150mL-EK-2299-2-Col-Divided',
    grid =(8,2), #cols,rows
    spacing=(9,54), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot='A1'
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
print("Step 5: Prep sample")
print("%s" % (start))

src_row = 9 #binding + etoh source row
wash_src_row = 1 #prep and wash buffers 

start_row = int(sys.argv[1])
last_row = int(sys.argv[2])+1

volumes = [226, 339, 400, 700, 400] #Binding, EtOH, RNA Prep, Wash, Wash
what_to_add = ["24 mL RNA prep", "42 mL wash buffer","24 mL wash buffer"]

for i in range(5): 
    loop_start = datetime.now()

    if i < 2:
        robot.pause()
        if i == 0:
            check = input("Place sample plate at position B2 after incubation. Remove seal from 12-column plate at A2 and add 13.5 mL RNA binding buffer to position 9. Empty trash. Press enter to continue. ")
        else:
            check = input("Place sample plate at position B2 after incubation. Place filter plate + 2 mL Fisher base at B1. Remove seal from 12-column plate at A2 and add 21 mL EtOH to position 11. Empty trash. Press enter to continue. ")
        robot.resume()

        p1200_multi.pick_up_tip()

        for row_i in range(start_row,last_row):

            p1200_multi.transfer(volumes[i], 
                binding_etoh.rows(str(src_row)), 
                sample_plate.rows(str(row_i)).bottom(22), 
                air_gap = 20,
                new_tip="never",
            )

        p1200_multi.drop_tip()
        
        src_row += 2

        if i == 1:

            for row_i in range(start_row, last_row):
                p1200_multi.pick_up_tip()
                p1200_multi.mix(3, 500, sample_plate.rows(str(row_i)).bottom())
                p1200_multi.aspirate(980, sample_plate.rows(str(row_i)).bottom())
                p1200_multi.delay(0.5)
                p1200_multi.aspirate(20, sample_plate.rows(str(row_i)).top())
                p1200_multi.dispense(1000, filter_plate.rows(str(row_i)).bottom())

                # p1200_multi.transfer(980,
                #     sample_plate.rows(str(row_i)).bottom(),
                #     filter_plate.rows(str(row_i)),
                #     mix_before = (3, 500),
                #     air_gap = 20,
                #     new_tip = "always"
                # )


    else:
        robot.pause()
        check = input("Place filter plate at B1. Add %s to column %s at A1 reservoir. Press enter to continue. " % (what_to_add[(i-2)], wash_src_row))
        robot.resume()

        p1200_multi.pick_up_tip()

        for row_i in range(start_row, last_row):
            p1200_multi.transfer(volumes[i],
                wash.rows(str(wash_src_row)),
                filter_plate.rows(str(row_i)).bottom(22),
                air_gap = 20,
                new_tip = "never"
            )

        p1200_multi.drop_tip()

        if i == 2:
            wash_src_row += 1

    if i > 0:
        print("Centrifuge for 5 min at 3000-5000*g. ")

    if i == 1:
        p1200_multi.start_at_tip(racks[0].rows("1"))
        robot.pause()
        check = input("Change tip rack at E1. Press enter to continue. " % (what_to_add[(i-2)], wash_src_row))
        robot.resume()
    
    print("Loop completion time: %s" % (datetime.now()-loop_start))

print("Total time: %s" % (datetime.now()-start))
robot.home()