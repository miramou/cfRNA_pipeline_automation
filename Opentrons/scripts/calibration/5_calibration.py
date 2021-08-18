##SCRIPT TO ADD WASH BUFFER 3X TO NORGEN FILTER and ELUTE
##TIME TO RUN: ~5 minutes + 22 minutes centrifuge
##TOTAL TIPS USED: 4 rows

#PLATE SETUP
#Load custom containers using bug fix

#Pipette racks
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
	

#Load filter plate
plate_slots = ["B1", "B2"]
filter_plates = []

for slot_i in plate_slots: #Only use up to row 11 on B2.
    filter_plates.append(
        create_container_instance(
            '96-well-Norgen-filter',
            grid =(8,12), #cols,rows
            spacing=(8.8,8.8), #mm spacing between each col,row
            diameter=8,
            depth=30, #depth mm of each well 
            slot=slot_i
        )
    )

#Load trash
trash = containers.load('trash-box', 'D2')

#Load wash
wash =  create_container_instance(
    '96-well-150mL-EK-2299-2-Col-Divided',
    grid =(8,2), #cols,rows
    spacing=(9,54), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot='A1'
)

elution =  create_container_instance(
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
src_row = 1 #wash source row
elu_src_row = 9

start_row = 1
last_row = 7

max_vol = 1000
disposal_vol = 50
wash_vol = 400
elu_vol = 100 

p1200_multi.start_at_tip(racks[0].rows("6")) ## Continue from  step 3 where 5 rows were used.

for i in range(4): 
#Just under 5.5 min per plate
    
    if i < 3:
        p1200_multi.pick_up_tip()

        max_iters = (max_vol-disposal_vol) // wash_vol
        iters = max_iters
        
        p1200_multi.aspirate(max_vol, wash.rows(str(src_row)))

        for row_i in range(start_row, last_row):
            p1200_multi.dispense(wash_vol, filter_plates[0].rows(str(row_i)).bottom(22))
            iters -= 1

            if iters == 0 and row_i < (last_row-1):
                row_dif = last_row - row_i
                iters = max_iters

                p1200_multi.dispense((max_vol - iters*wash_vol), wash.rows(str(src_row)))

                if row_dif < max_iters:
                    p1200_multi.aspirate((row_dif*wash_vol+disposal_vol), wash.rows(str(src_row)))
                else:
                    p1200_multi.aspirate(max_vol, wash.rows(str(src_row)))


        p1200_multi.drop_tip()

    else:
        p1200_multi.pick_up_tip()

        max_iters = (max_vol-disposal_vol) // elu_vol
        iters = max_iters
        
        p1200_multi.aspirate(max_vol, elution.rows(str(elu_src_row)))

        for row_i in range(start_row, last_row):
            p1200_multi.dispense(elu_vol, filter_plates[1].rows(str(row_i)).bottom(22))
            iters -= 1

            if iters == 0 and row_i < (last_row-1):
                row_dif = last_row - row_i
                iters = max_iters

                p1200_multi.dispense((max_vol - iters*elu_vol), elution.rows(str(elu_src_row)))

                if row_dif < max_iters:
                    p1200_multi.aspirate((row_dif*elu_vol+disposal_vol), elution.rows(str(elu_src_row)))
                else:
                    p1200_multi.aspirate(max_vol, elution.rows(str(elu_src_row)))


        p1200_multi.drop_tip()

