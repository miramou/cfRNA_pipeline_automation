##SCRIPT TO TRANSFER EtOH + CENTRIFUGE + ADD LYSIS BUFFER TO 48 well PLATE
##TIME TO RUN: ~XX minutes

from opentrons import robot, containers, instruments

#PLATE SETUP
#Load custom containers using bug fix

#Pipette racks
racks = []
rack_slots = ["A2", "B2", "C2"]

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
plate_slots = ["A1", "B1"]

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

sample_rows = plates[0].rows()+plates[1].rows()

#Load trash
trash = containers.load('trash-box', 'E2')

#Load EtOH, lysis buffer
etoh =  create_container_instance(
    '96-well-300mL-EK-2035-S',
    grid =(8,12), #cols,rows
    spacing=(8,8), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot='C1'
)

lysis =  create_container_instance(
    '96-well-300mL-EK-2035-S',
    grid =(8,12), #cols,rows
    spacing=(8,8), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot='D1'
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
etoh_vol = 3000

p1200_multi.transfer(etoh_vol, etoh.rows(), sample_rows, new_tip='always',mix_after=(20, 1200))
robot.comment("Seal and centrifuge plates for 1 min at 1000 RPM. Press resume when ready to continue.")
robot.pause()

p1200_multi.transfer(5800, sample_rows, trash, new_tip='always',)
p1200_multi.transfer(300, lysis.rows(), sample_rows, new_tip='always', mix_after=(20, 200))
robot.comment("Seal and incubate for 10 min at 60C.")

