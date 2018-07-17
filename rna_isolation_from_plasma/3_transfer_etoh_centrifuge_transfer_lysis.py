##SCRIPT TO TRANSFER EtOH + CENTRIFUGE + ADD LYSIS BUFFER TO 48 well PLATE
##TIME TO RUN: ~XX minutes

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
    aspirate_speed=400,
    dispense_speed=700
)

#PROTOCOL
etoh_vol = float(sys.argv[1])

start = datetime.now()
print("Step 3: Add ethanol, centrifuge, decant supernatant, add lysis buffer")
print("%s" % (start))

src_row=1
for i in range(2):
    for dst_row in plates[i].rows():

        p1200_multi.pick_up_tip()

        p1200_multi.transfer(etoh_vol, 
            etoh.rows(str(src_row)), 
            dst_row.top(-10),
            new_tip="never",
            trash=False)

        p1200_multi.transfer(1000, 
            dst_row, 
            dst_row.bottom(),
            mix_before=(5,1000),
            new_tip="never",
            trash=False)

        #p1200_multi.drop_tip(trash)
        p1200_multi.return_tip()
        src_row += 1

robot.pause()
check = input("Seal and centrifuge plates for 1 min at 1000 RPM. Press enter when ready to continue.")
robot.resume()

robot.home()


for i in range(2):

    for row in plates[i].rows():
        
        p1200_multi.pick_up_tip()

        p1200_multi.transfer(5650, 
                row.bottom(15), 
                trash, 
                new_tip='never',
                trash = False)

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
        
        p1200_multi.return_tip()


robot.pause()
check = input("Replace tip box at position E1. Press enter to continue once complete.")
robot.resume()

robot.home()

#Manually tell it to start at E1 again
p1200_multi.start_at_tip(racks[0].rows(0))

src_row = 1
for i in range(2):
    for dst_row in plates[i].rows():
        p1200_multi.transfer(300, 
            lysis.rows(str(src_row)), 
            dst_row.bottom(), 
            mix_after=(5, 200),
            trash=False)

        src_row += 1

print("Seal and incubate for 10 min at 60C.")
print("Total time: %s" % (datetime.now()-start))

