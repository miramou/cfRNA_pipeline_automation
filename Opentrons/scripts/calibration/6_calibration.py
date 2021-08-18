##SCRIPT TO ZYMO CLEAN AND CONCENTRATE
##TIME TO RUN: ~1 hour (with centrifugation) for 12 rows
##TOTAL TIPS USED: 17 rows

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
		    depth=150, #depth mm of each well 
		    slot=slot_i
		)
	)
	

#Load sample plate
sample_plate = create_container_instance(
    '96-well-2mL',
    grid =(8,12), #cols,rows
    spacing=(9,9), #mm spacing between each col,row
    diameter=8,
    depth=40, #depth mm of each well 
    slot="C1"
)

#Load filter plate
filter_plate = create_container_instance(
    '96-well-Zymo-filter',
    grid =(8,12), #cols,rows
    spacing=(8.8,8.8), #mm spacing between each col,row
    diameter=8,
    depth=40, #depth mm of each well 
    slot="B1"
)

#Load trash
trash = containers.load('trash-box', 'D2')

#Load reagents
binding_etoh =  create_container_instance(
    '96-well-150mL-EK-2299-2-Col-Divided',
    grid =(8,2), #cols,rows
    spacing=(9,54), #mm spacing between each col,row
    diameter=8,
    depth=15, #depth mm of each well 
    slot='D1'
)

wash =  create_container_instance(
    '96-well-150mL-EK-2299-2-Col-Divided',
    grid =(8,2), #cols,rows
    spacing=(9,54), #mm spacing between each col,row
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
binding_etoh_src_row = 1 #binding and etoh
wash_src_row = 1 #prep and wash buffers 

start_row = 1
last_row = 13
max_vol = 1000
disposal_vol = 50

volumes = [226, 339, 400, 700, 400] #Binding, EtOH, RNA Prep, Wash, Wash
what_to_add = ["27 mL binding buffer", "50 mL EtOH", "48 mL RNA prep", "84 mL wash buffer","48 mL wash buffer"]

for i in range(5):  

    if i < 2:
        p1200_multi.pick_up_tip()

        max_iters = (max_vol-disposal_vol) // volumes[i]
        iters = max_iters
        
        p1200_multi.aspirate(max_vol, binding_etoh.rows(str(binding_etoh_src_row)))

        for row_i in range(start_row, last_row):
            p1200_multi.dispense(volumes[i], sample_plate.rows(str(row_i)).bottom(30))
            iters -= 1

            if iters == 0 and row_i < (last_row-1):
                row_dif = last_row - row_i
                iters = max_iters

                p1200_multi.dispense((max_vol - iters*volumes[i]), binding_etoh.rows(str(binding_etoh_src_row)))

                if row_dif < max_iters:
                    p1200_multi.aspirate((row_dif*volumes[i]+disposal_vol), binding_etoh.rows(str(binding_etoh_src_row)))
                else:
                    p1200_multi.aspirate(max_vol, binding_etoh.rows(str(binding_etoh_src_row)))


        p1200_multi.drop_tip()


        if i == 1:

            if last_row > 6:
                p1200_multi.start_at_tip(racks[0].rows("1"))

            for row_i in range(start_row, last_row): 
                
                p1200_multi.pick_up_tip()
                p1200_multi.mix(3, 500, sample_plate.rows(str(row_i)).bottom())
                p1200_multi.aspirate(900, sample_plate.rows(str(row_i)).bottom())
                p1200_multi.delay(0.5)
                p1200_multi.aspirate(100, sample_plate.rows(str(row_i)).top())
                p1200_multi.dispense(1000, filter_plate.rows(str(row_i)).bottom(10))
                p1200_multi.aspirate(200, filter_plate.rows(str(row_i)).bottom(25)) #air gap
                p1200_multi.drop_tip()

            p1200_multi.start_at_tip(racks[0].rows("1"))
            
        binding_etoh_src_row += 1

    else:
        p1200_multi.pick_up_tip()

        max_iters = (max_vol-disposal_vol) // volumes[i]
        iters = max_iters
        
        p1200_multi.aspirate(max_vol, wash.rows(str(wash_src_row)))

        for row_i in range(start_row, last_row):
            p1200_multi.dispense(volumes[i], filter_plate.rows(str(row_i)).bottom(22))
            iters -= 1

            if iters == 0 and row_i < (last_row-1):
                row_dif = last_row - row_i
                iters = max_iters

                p1200_multi.dispense((max_vol - iters*volumes[i]), wash.rows(str(wash_src_row)))

                if row_dif < max_iters:
                    p1200_multi.aspirate((row_dif*volumes[i]+disposal_vol), wash.rows(str(wash_src_row)))
                else:
                    p1200_multi.aspirate(max_vol, wash.rows(str(wash_src_row)))


        p1200_multi.drop_tip()

        if i == 2:
            wash_src_row += 1
    