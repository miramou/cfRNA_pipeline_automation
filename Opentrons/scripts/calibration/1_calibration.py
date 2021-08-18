racks = []
rack_slots = ["E1"]

for slot_i in rack_slots:
	racks.append(
		create_container_instance(
		    'rainin-tiprack-1200ul',
		    grid =(8,12), #cols,rows
		    spacing=(9,9), #mm spacing between each col,row
		    diameter=8,
		    depth=110, #depth mm of each well 
		    slot=slot_i
		)
	)

#Sample plates
plates = []
plate_slots = ["B2", "B1"]

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
    '96-well-150mL-EK-2299-2-Col-Divided',
    grid =(8,2), #cols,rows
    spacing=(9,54), #mm spacing between each col,row
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
	max_volume=1000,
	trash_container=trash,
	tip_racks=racks,
	channels=8,
    aspirate_speed=600,
    dispense_speed=700
)

#PROTOCOL
lysis_volume = 1800

src_row_slurry = 1
src_row_lysis = 1

#tips_on_set = set([1,3,5])
#tips_off_set = set([2,4,6])

tips_on_set = set([1])
tips_off_set = set([6])

dispense_vol = lysis_volume
dispense_iters = 1
air_gap_vol = 100

if lysis_volume > 1000:
	dispense_iters = 5
	dispense_vol /= dispense_iters
	air_gap_vol = 1000 - dispense_vol

for i in range(2):
#Just under 3 minutes per plate
#Lysis: Works well if added 220 mL lysis buffer + 1.2% B-met
#Slurry: Works well if add 10.5 mL slurry to column 1,2 of divided plate holder. Do so when instructed to.

	count = 1

	if i == 0:
		for dst_row in plates[i].rows():
			#Separated transfer wrapper into distinct steps for further control on apsiration rate and movement
			if count in tips_on_set:
				p1200_multi.pick_up_tip()

			p1200_multi.mix(1, 500, slurry.rows(str(src_row_slurry)))
			p1200_multi.blow_out(slurry.rows(str(src_row_slurry)))
			p1200_multi.aspirate(200, slurry.rows(str(src_row_slurry)).bottom(),rate=0.1)
			p1200_multi.delay(1.5)
			p1200_multi.aspirate(50, slurry.rows(str(src_row_slurry)).top(30), rate=1.0) #air gap
			p1200_multi.dispense(250, dst_row.top(-30))
			
			if count in tips_off_set:
				p1200_multi.drop_tip()

			count += 1

	else:
		for dst_row in plates[i].rows():

			if count in tips_on_set:
				p1200_multi.pick_up_tip()

			for i in range(dispense_iters):
				p1200_multi.aspirate(dispense_vol, lysis.rows(str(src_row_lysis)).bottom(), rate=1.0)
				p1200_multi.delay(0.2)
				p1200_multi.aspirate(air_gap_vol, lysis.rows(str(src_row_lysis)).top(30), rate=1.0) #air gap
				p1200_multi.dispense((dispense_vol+air_gap_vol), dst_row.top(-20))

			if count in tips_off_set:
				p1200_multi.drop_tip()

			count += 1
