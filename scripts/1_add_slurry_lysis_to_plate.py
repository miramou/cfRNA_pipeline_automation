##SCRIPT TO TRANSFER SLURRY + LYSIS BUFFER TO 48 well PLATE
##TIME TO RUN: ~8 minutes

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
trash = containers.load('trash-box', 'D2')

#Load slurry, lysis buffer
lysis =  create_container_instance(
    '96-well-300mL-EK-2035-S',
    grid =(8,12), #cols,rows
    spacing=(9,9), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot='A1'
)

slurry =  create_container_instance(
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
lysis_volume = float(sys.argv[1])

start=datetime.now()
print("Step 1: Add lysis and slurry to plate")
print("%s" % (start))

src_row = 1
p1200_multi.pick_up_tip()

for i in range(2):
#Just under 3 minutes per plate
#Works well if added 200 mL lysis buffer + 1.2% B-met

	loop_start = datetime.now()

	for dst_row in plates[i].rows():

		p1200_multi.transfer(lysis_volume,
			lysis.rows(str(src_row)), 
			dst_row.bottom(), 
			new_tip="never",
			blow_out=True,
			air_gap=20
		)

		src_row += 1

	print("Time for loop completion: %s" % (datetime.now() - loop_start))

p1200_multi.drop_tip()
robot.home()

p1200_multi.pick_up_tip()
src_row = str(1)

for i in range(2):
#Just about 3 minutes and 30 seconds per plate
#Works well if add 21 mL slurry to column 1 of divided plate holder

	loop_start = datetime.now()

	for dst_row in plates[i].rows():
		#Separated transfer wrapper into distinct steps for further control on apsiration rate and movement
		p1200_multi.mix(3, 1000, slurry.rows(src_row))
		p1200_multi.blow_out(slurry.rows(src_row))
		p1200_multi.aspirate(220, slurry.rows(src_row),rate=0.1)
		p1200_multi.delay(3)
		p1200_multi.dispense(200, dst_row.top(-12))
		p1200_multi.blow_out(slurry.rows(src_row))
		
	print("Time for loop completion: %s" % (datetime.now() - loop_start))


p1200_multi.drop_tip()

print("Total time: %s" % (datetime.now()-start))
robot.home()
