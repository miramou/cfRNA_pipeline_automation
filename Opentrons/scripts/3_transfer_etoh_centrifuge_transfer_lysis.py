##SCRIPT TO TRANSFER EtOH + CENTRIFUGE + REMOVE SUP FROM 48 well PLATE
##TIME TO RUN: ~30 minutes
##TOTAL TIPS USED: 1.5 boxes

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
etoh_vol = float(sys.argv[1])

start = datetime.now()
print("Step 3: Add ethanol, centrifuge, decant supernatant")
print("%s" % (start))

p1200_multi.start_at_tip(racks[0].rows("6"))

src_row=1
for i in range(2):
#Just under 4 minutes per plate
#200 mL EtOH in reservoir per plate

    loop_start = datetime.now()

    count = 1

    for dst_row in plates[i].rows():
        if count == 1 or count % 2 == 0:
            p1200_multi.pick_up_tip()
        
        p1200_multi.transfer(etoh_vol, 
            etoh.rows(str(src_row)), 
            dst_row.top(-10),
            new_tip="never"
        )

        src_row += 1
        count += 1

        if count % 2 == 0:
            p1200_multi.drop_tip()

    print("Time for loop completion: %s" % (datetime.now() - loop_start))
    robot.home()

    if i==0:
        robot.pause()
        check = input("Remove B1 and mix. Replace EtOH in reservoir to 200 mL. Press enter to continue with adding EtOH to B2 ")
        robot.resume()



robot.pause()
check = input("Mix B2, seal both plates and centrifuge for 1 min at 1000 RPM. Press enter when ready to continue. ")
robot.resume()

robot.home()

to_remove_vol = [980, 980, 980, 980, 980, 900]
to_remove_height = [25,25, 15, 6, 2, 0.12]

for i in range(2):
#Just over 7 minutes per plate

    loop_start = datetime.now()

    for row in plates[i].rows():
        
        p1200_multi.pick_up_tip()

        for i in range(len(to_remove_vol)):
            p1200_multi.transfer(to_remove_vol[i], 
                row.bottom(to_remove_height[i]), 
                liquid_trash,
                air_gap = 20,
                blow_out=True, 
                new_tip='never'
            )

        p1200_multi.drop_tip()

    print("Time for loop completion: %s" % (datetime.now() - loop_start))

    robot.home()

print("Total time: %s" % (datetime.now()-start))
robot.home()
