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
liquid_trash = containers.load('trash-box', 'D1')
trash = containers.load('trash-box', 'D2')

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
            dst_row.top(-10),
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

to_remove_vol = [1000, 1000, 1000, 1000, 1000, 800]
to_remove_height = [25,25, 15, 6, 2, 0.1]

for i in range(2):
#Just over 7 minutes per plate

    loop_start = datetime.now()

    for row in plates[i].rows():
        
        p1200_multi.pick_up_tip()

        for i in range(len(to_remove_vol)):
            p1200_multi.transfer(to_remove_vol[i], 
                row.bottom(to_remove_height[i]), 
                liquid_trash,
                blow_out=True, 
                new_tip='never'
            )

        p1200_multi.drop_tip()

    print("Time for loop completion: %s" % (datetime.now() - loop_start)) #About 4 min

    robot.home()


src_row = 2
count = 1

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

        count += 1

        if count == 7:
            src_row += 1

        if count == 11:
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
