##SCRIPT TO TRANSFER EtOH + CENTRIFUGE + ADD LYSIS BUFFER TO 48 well PLATE
##TIME TO RUN: ~30 minutes


## Things to fix: Pipette usage,
from opentrons import robot, containers, instruments
from setup import *
from datetime import datetime
import sys

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
		    spacing=(9,8.9), #mm spacing between each col,row
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

#Load trash
trash = containers.load('trash-box', 'D1')

#Load EtOH, lysis buffer
etoh =  create_container_instance(
    '96-well-300mL-EK-2035-S',
    grid =(8,12), #cols,rows
    spacing=(9,9), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot='A1'
)

lysis =  create_container_instance(
    '96-well-300mL-EK-2035-S',
    grid =(8,12), #cols,rows
    spacing=(9,9), #mm spacing between each col,row
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
	channels=8,
    aspirate_speed=600,
    dispense_speed=700
)

#PROTOCOL
etoh_vol = float(sys.argv[1])

start = datetime.now()
print("Step 3: Add ethanol, centrifuge, decant supernatant, add lysis buffer")
print("%s" % (start))

src_row=1
for i in range(2):
#Just under 4 minutes per plate
    loop_start = datetime.now()

    p1200_multi.pick_up_tip()

    for dst_row in plates[i].rows():
        p1200_multi.transfer(etoh_vol, 
            etoh.rows(str(src_row)), 
            dst_row.top(-12),
            new_tip="never"
        )

        src_row += 1

    p1200_multi.drop_tip()
    
    print("Time for loop completion: %s" % (datetime.now() - loop_start))
    robot.home()

    if i==0:
        robot.pause()
        check = input("Remove B1 and mix. Press enter to continue with adding EtOH to B2 ")
        robot.resume()



robot.pause()
check = input("Mix B2, seal both plates and centrifuge for 1 min at 1000 RPM. Press enter when ready to continue. ")
robot.resume()

robot.home()

for i in range(2):
#Just over 7 minutes per plate

    loop_start = datetime.now()

    for row in plates[i].rows():
        
        p1200_multi.pick_up_tip()

        p1200_multi.transfer(5000, 
            row.bottom(25), 
            trash, 
            new_tip='never'
        )

        p1200_multi.drop_tip()

    print("Time for loop completion: %s" % (datetime.now() - loop_start)) #About 4 min

    robot.home()

    if i==0:
        robot.pause()
        check = input("Remove B1 and finish supernatant removal. Press enter to continue with supernatant removal for B2 ")
        robot.resume()

        # has_more = int(input("More supernatant to aspirate? (True/False)"))

        # while has_more:
        #     to_remove = float(input("Enter how much to aspirate (uL)."))
        #     height = int(input("Enter how far from the bottom of the well you'd like to aspirate in mm."))

        #     p1200_multi.transfer(to_remove, 
        #         row.bottom(height), 
        #         trash, 
        #         new_tip='never',
        #         trash = False)

        #     has_more = bool(input("More supernatant to aspirate? (True/False)"))
        
        #p1200_multi.drop_tip(trash)
        

src_row = 1
for i in range(2):
#Just over 4 minutes per plate

    loop_start = datetime.now()

    for dst_row in plates[i].rows():
        p1200_multi.transfer(300, 
            lysis.rows(str(src_row)),
            dst_row.bottom(),
            mix_after=(10,200), 
            new_tip="always"
        )

        src_row += 1

        if src_row == 11:
            robot.pause()
            check = input("Replace tip rack E1. Press enter to continue. ")
            robot.resume()
            p1200_multi.start_at_tip(racks[0].rows("1"))

    print("Time for loop completion: %s" % (datetime.now() - loop_start)) #About 4 min

    if i==0:
        robot.pause()
        check = input("Remove B1, seal, and incubate for 10 min at 60C. Press enter to continue with lysis addition + mixing for B2 ")
        robot.resume()

print("Seal and incubate B2 for 10 min at 60C.")
print("Total time: %s" % (datetime.now()-start))
robot.home()
