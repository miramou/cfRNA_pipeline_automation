##SCRIPT TO TRANSFER PLASMA SAMPLES TO 48 well PLATE
##TIME TO RUN: ~20 minutes

from opentrons import robot, containers, instruments

#PLATE SETUP
#Load vial racks
vial_slots = ["A1", "C1"]
vial_rack_list = [containers.load('24-vial-rack', slot) for slot in vial_slots]

#Load custom containers using bug fix
racks = []
rack_slots = ["D1"] #["A2", "B2", "C2"]

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

plate = create_container_instance(
    '48-well-7mL-EK-2043',
    grid =(8,6), #cols,rows
    spacing=(9,18), #mm spacing between each col,row
    diameter=9,
    depth=65, #depth mm of each well 
    slot="B1"
)

#Load trash
trash = containers.load('trash-box', 'D2')

p1000 = instruments.Pipette(
	axis='b',
	min_volume=100,
	max_volume=1000, 
	trash_container=trash,
	tip_racks=racks,
	channels=1
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
sample_volume=1000
dest_well_list = ["A1", "A2", "A3", "A4", "A5", "A6", "B1", "B2", "B3", "B4", "B5", "B6", "C1", "C2", "C3", "C4", "C5", "C6", "D1", "D2", "D3", "D4", "D5", "D6",
					"E1", "E2", "E3", "E4", "E5", "E6","F1", "F2", "F3", "F4", "F5", "F6", "G1", "G2", "G3", "G4", "G5", "G6", "H1", "H2", "H3", "H4", "H5", "H6"]

for well in range(0,48):
	src_rack_idx, src_well_idx = get_source_idx(well)
	dest_well_idx = dest_well_list[well]

	vial_rack = vial_rack_list[src_rack_idx]

	p1000.transfer(sample_volume, 
		vial_rack.wells(src_well_idx), 
		plate.wells(dest_well_idx).bottom(),
		new_tip="always"
	)

p1200_multi.transfer(1200, plate.rows(), plate.rows(), mix_after=(19,1000), new_tip='always')
robot.comment("Seal and incubate for 10 min at 60C.")

	