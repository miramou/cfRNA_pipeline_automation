#from setup import *

racks = []
rack_slots = ["E1", "E2"] #"C1", "E1", "E2"]

for slot_i in rack_slots:
	racks.append(
		create_container_instance(
		    'rainin-tiprack-1200ul', #"rainin-tiprack-1000ul_long", "rainin-tiprack-1200ul"
		    grid =(8,12), #cols,rows
		    spacing=(9,9), #mm spacing between each col,row
		    diameter=8,
		    depth=110, #depth mm of each well 
		    slot=slot_i
		)
	)

# for slot_i in rack_slots:
# 	racks.append(
# 		create_container_instance(
# 		    'rainin-tiprack-1000ul_long', #"rainin-tiprack-1000ul_long", "rainin-tiprack-1200ul"
# 		    grid =(8,12), #cols,rows
# 		    spacing=(9,9), #mm spacing between each col,row
# 		    diameter=8,
# 		    depth=150, #depth mm of each well 
# 		    slot=slot_i
# 		)
# 	)


# plates = []
# plate_slots = ["B1","B2"]

# for slot_i in plate_slots:
# 	plates.append(
# 		create_container_instance(
# 			'48-well-7mL-EK-2043', #48-well-7mL-EK-2043_long_tips
# 			grid =(8,6), #cols,rows
# 			spacing=(9,18), #mm spacing between each col,row
# 			diameter=9,
# 			depth=65, #depth mm of each well 
# 			slot=slot_i
# 		)
# 	)


#Load trash

trash = create_container_instance(
    'trash_rows',
    grid =(8,6), #cols,rows
    spacing=(9,18), #mm spacing between each col,row
    diameter=9,
    depth=65, #depth mm of each well 
    slot='C1'
)
#trash = containers.load('trash-box', 'D2') 

vial_slots = ["B1"]
vial_rack_list = [containers.load('24-vial-rack', slot) for slot in vial_slots]


etoh =  create_container_instance(
    '96-well-150mL-EK-2299-2-Col-Divided',
    grid =(8,2), #cols,rows
    spacing=(9,54), #mm spacing between each col,row
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

# #Load final plate
plate_slots = ["B1","B2"]
final_plates = []

for slot_i in plate_slots:
	final_plates.append(
		create_container_instance(
		    '96-well-Norgen-filter',
		    grid =(8,12), #cols,rows
		    spacing=(8.8,8.8), #mm spacing between each col,row
		    diameter=8,
		    depth=15, #depth mm of each well 
		    slot=slot_i
		)
	)

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

#p1000.transfer(100, vial_rack_list[0].wells(), plates[0].wells())
p1200_multi.transfer(100, lysis.rows(), sample_plate.rows())


# for rack in range(1):
# 	for row in racks[rack].rows():
# 		p1200_multi.pick_up_tip(row)
# 		p1200_multi.return_tip()
# 		robot.home("z")


# for rack in range(1):
# 	for row in racks[rack].rows("2",to="12"):
# 		p1000.pick_up_tip(row)
# 		p1000.return_tip()
# 		robot.home("z")
# 	if rack == 0:
# 		robot.pause()
# 		check = input("Press enter once tip box moved to E2")
# 		robot.resume()


#p1200_multi.transfer(100, etoh.rows(), final_plates[0].rows())
#p1200_multi.transfer(100, etoh.rows(), final_plates[1].rows())


# for i in range(8):
# 	p1200_multi.transfer(100,src_rows[i], dest_rows[i])

#p1200_multi.transfer(100,lysis.rows(), plates[0].rows())
#p1200_multi.transfer(100,lysis.rows(), plates[1].rows())

#p1200_multi.transfer(100,etoh1.rows(), plates[0].rows())
#p1200_multi.transfer(100,etoh.rows(), plates[1].rows())


p1200_multi.transfer(100, etoh.rows(), sample_plate.rows())
p1200_multi.transfer(100, etoh.rows(), filter_plate.rows())
# p1000.transfer(100,lysis.wells(), plates[0].wells())
# p1000.transfer(100,lysis.wells(), plates[1].wells())

#p1200_multi.start_at_tip(racks[0].rows("3"))