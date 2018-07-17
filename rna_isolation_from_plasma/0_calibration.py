racks = []
rack_slots = ["E1"] #"C2", "D2", "E2"]


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
#trash = containers.load('trash-box', 'E1')
#trash = containers.load('trash-box', 'D1')


etoh =  create_container_instance(
    '96-well-300mL-EK-2035-S',
    grid =(8,12), #cols,rows
    spacing=(8,8), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot='A1'
)

lysis =  create_container_instance(
    '96-well-300mL-EK-2035-S',
    grid =(8,12), #cols,rows
    spacing=(8,8), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot='A2'
)

# #Load final plate
# final_plate = create_container_instance(
#     '96-well-1mL-Axygen',
#     grid =(8,12), #cols,rows
#     spacing=(8,8), #mm spacing between each col,row
#     diameter=8,
#     depth=15, #depth mm of each well 
#     slot='A1'
# )

p1200_multi = instruments.Pipette(
	axis='a',
	min_volume=100,
	max_volume=1200,
	trash_container=trash,
	tip_racks=racks,
	channels=8
)

p1000 = instruments.Pipette(
	axis='b',
	min_volume=100,
	max_volume=1000, 
	trash_container=trash,
	tip_racks=racks,
	channels=1
)

p1200_multi.transfer(100, etoh.rows(), final_plate.rows())
p1200_multi.transfer(100,etoh.rows(), plates[1].rows())

p1200_multi.transfer(100,lysis.rows(), plates[0].rows())
p1200_multi.transfer(100,lysis.rows(), plates[1].rows())

p1000.transfer(100,etoh.wells(), plates[0].wells())
p1000.transfer(100,etoh.wells(), plates[1].wells())

p1000.transfer(100,lysis.wells(), plates[0].wells())
p1000.transfer(100,lysis.wells(), plates[1].wells())