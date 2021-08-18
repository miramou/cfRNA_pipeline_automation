##SCRIPT TO TRANSFER EtOH + CENTRIFUGE + REMOVE SUP FROM 48 well PLATE + LYSIS/ETOH ADDITION
##TIME TO RUN: ~25 minutes (+10 min incubation)
##TOTAL TIPS USED: 15 rows

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

#Load etoh
lysis_etoh =  create_container_instance(
    '96-well-252mL-EK-2034-S-12-Col-Divided',
    grid =(8,12), #cols,rows
    spacing=(9,9), #mm spacing between each col,row
    diameter=8,
    depth=45, #depth mm of each well 
    slot='A2'
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
			depth=70, #depth mm of each well 
			slot=slot_i
		)
	)

#Load trash
liquid_trash = create_container_instance(
    'trash_rows',
    grid =(8,6), #cols,rows
    spacing=(9,18), #mm spacing between each col,row
    diameter=9,
    depth=65, #depth mm of each well 
    slot='C1'
)

trash = containers.load('trash-box', 'D2')

#Load EtOH, lysis buffer
etoh =  create_container_instance(
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
etoh_vol = 3000

src_row_etoh=2 
src_row_lysis_etoh=3

max_vol = 1000
disposal_vol = 50
lysis_etoh_vol = 300

start_row =  1
last_row = 7


for i in range(3):
    
    if i == 0:
    #Total time per plate: 8 minutes

        p1200_multi.start_at_tip(racks[0].rows("3"))
    
        for j in range(2):
            
            if j == 0:
                p1200_multi.pick_up_tip()

            for dst_row in plates[i].rows(): 
               
                if j == 0:
                    p1200_multi.transfer(etoh_vol,
                        etoh.rows(str(src_row_etoh)),
                        dst_row.top(-5),
                        new_tip= "never"
                    )

                if j == 1: #Increased pipette mixing.
                    p1200_multi.pick_up_tip()
                    p1200_multi.mix(4, 1000, dst_row.bottom(8))
                    p1200_multi.mix(4, 1000, dst_row.bottom(20))
                    p1200_multi.mix(4, 1000, dst_row.bottom(34))
                    p1200_multi.drop_tip()

            if j == 0:
                p1200_multi.drop_tip()

    # elif i == 1:    
    #     to_remove_vol = [980, 980, 980, 980, 980, 980]
    #     to_remove_height = [25,20, 15, 6, 2, 1.5]  

    #     trash_row = 1

    #     #Just about 9 minutes per plate
    #     for row in plates[(i-1)].rows():  

    #         p1200_multi.pick_up_tip()

    #         for j in range(len(to_remove_vol)):

    #             p1200_multi.aspirate(to_remove_vol[j], row.bottom(to_remove_height[j]))
    #             if j == 0:
    #                 p1200_multi.aspirate(20, row.top())
    #             else:
    #                 p1200_multi.aspirate(10, row.top())

    #             #Liquid trash should be flush with top right corner of C1 when facing the OT
    #             p1200_multi.dispense((to_remove_vol[j]+20), liquid_trash.rows(str(trash_row)).bottom(35))
    #             p1200_multi.delay(0.2)
    #             p1200_multi.blow_out()
    #             p1200_multi.aspirate(10, liquid_trash.rows(str(trash_row)).bottom(35))

    #         p1200_multi.drop_tip()
    #         trash_row += 1
            
    else: 
        plate_pos = (i-1)

        p1200_multi.pick_up_tip()

        max_iters = (max_vol-disposal_vol) // lysis_etoh_vol
        iters = max_iters
        
        p1200_multi.aspirate(max_vol, lysis_etoh.rows(str(src_row_lysis_etoh)))

        for row_i in range(start_row, last_row):
            p1200_multi.dispense(lysis_etoh_vol, plates[plate_pos].rows(str(row_i)).top(-20))
            iters -= 1

            if iters == 0 and row_i < (last_row-1):
                row_dif = last_row - row_i
                iters = max_iters

                p1200_multi.dispense((max_vol - iters*lysis_etoh_vol), lysis_etoh.rows(str(src_row_lysis_etoh)))

                if row_dif < max_iters:
                    p1200_multi.aspirate((row_dif*lysis_etoh_vol+disposal_vol), lysis_etoh.rows(str(src_row_lysis_etoh)))
                else:
                    p1200_multi.aspirate(max_vol, lysis_etoh.rows(str(src_row_lysis_etoh)))


        p1200_multi.drop_tip()

        if i == 2:
            src_row_lysis_etoh += 2