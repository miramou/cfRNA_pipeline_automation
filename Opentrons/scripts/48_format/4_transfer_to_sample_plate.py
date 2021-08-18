##SCRIPT TO TRANSFER TO 96 well PLATE
##TIME TO RUN: ~4 minutes
##TOTAL TIPS USED: 1 box long tips

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
		    'rainin-tiprack-1000ul_long',
		    grid =(8,12), #cols,rows
		    spacing=(9,9), #mm spacing between each col,row
		    diameter=8,
		    depth=150, #depth mm of each well 
		    slot=slot_i
		)
	)
	
#Sample plates
plates = []
plate_slots = ["B1"]

for slot_i in plate_slots:
	plates.append(
		create_container_instance(
			"48-well-7mL-EK-2043_long_tips",
			grid =(8,6), #cols,rows
			spacing=(9,18), #mm spacing between each col,row
			diameter=9,
			depth=65, #depth mm of each well 
			slot=slot_i
		)
	)

#Load final plate
final_plate = create_container_instance(
    '96-well-Norgen-filter_long',
    grid =(8,12), #cols,rows
    spacing=(8.8,8.8), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot='A1'
)

#Load trash
trash = create_container_instance(
    'trash_rows',
    grid =(8,6), #cols,rows
    spacing=(9,18), #mm spacing between each col,row
    diameter=9,
    depth=65, #depth mm of each well 
    slot='C1'
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
print("Step 4: Transfer to 96-well filter plate")
print("%s" % (start))

row_96 = int(sys.argv[1])

#Just under 6 min per plate

robot.pause()
check = input("Place plate 1 at position B1. Place filter plate at position A1 moving filter plate to top left corner (when facing the OT). Remove seal. Empty trash at C1. Press enter to continue with sample transfer. " )
robot.resume()


for row_48 in plates[0].rows(): 
    loop_start = datetime.now()

    p1200_multi.pick_up_tip()

    #Slurry sediments so vortex regularly
    robot.pause()
    check = input("Seal and vortex plate. Press enter to continue. ")
    robot.resume()

    p1200_multi.mix(2, 500, row_48.bottom())
    p1200_multi.aspirate(950, row_48.bottom(), rate=0.75) 
    p1200_multi.delay(0.5)
    p1200_multi.aspirate(40, row_48.bottom(), rate=0.75)
    p1200_multi.air_gap(10)
    p1200_multi.dispense(1000, final_plate.rows(str(row_96)).bottom(20), rate=0.5)
    p1200_multi.blow_out()

    p1200_multi.drop_tip()

    row_96 += 1

    print("Loop completion time: %s" % (datetime.now()-loop_start))


print("Total time: %s" % (datetime.now()-start))
print("Centrifuge for 4 min at max speed (3900 RPM).")
robot.home()
