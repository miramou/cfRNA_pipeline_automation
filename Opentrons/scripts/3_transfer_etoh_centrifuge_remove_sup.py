##SCRIPT TO TRANSFER EtOH + CENTRIFUGE + REMOVE SUP FROM 48 well PLATE
##TIME TO RUN: ~35 minutes
##TOTAL TIPS USED: 3 boxes

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
			depth=65, #depth mm of each well 
			slot=slot_i
		)
	)

#Load trash
liquid_trash = [containers.load('trash-box', 'C1'), containers.load('trash-box', 'C2')]
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
etoh_vol = float(sys.argv[1])

start = datetime.now()
print("Step 3: Add ethanol, centrifuge, decant supernatant, add lysis, incubate")
print("%s" % (start))

src_row_etoh=1 
src_row_lysis=4

for i in range(2): 
    #150 mL EtOH in reservoir per plate
    #Total time per plate: 7 minutes

    loop_start_a = datetime.now()

    for dst_row in plates[i].rows():
       
        loop_start_d = datetime.now()

        p1200_multi.pick_up_tip()

        p1200_multi.transfer(etoh_vol,
            etoh.rows(str(src_row_etoh)),
            dst_row.top(-20),
            new_tip= "never"
        )
        
        p1200_multi.mix(2, 1000, dst_row.bottom())
        p1200_multi.mix(2, 1000, dst_row.bottom(20))
        p1200_multi.mix(2, 1000, dst_row.bottom(27))

        p1200_multi.drop_tip()

        print("Time for loop completion: %s" % (datetime.now() - loop_start_d))

    src_row_etoh += 1

    print("Time for loop completion: %s" % (datetime.now() - loop_start_a))
    robot.home()

    robot.pause()
    if i==0:
        check = input("Seal plate %s at location %s and centrifuge for 1 min at 1000 RPM. Place plate %s at location %s. Press enter when ready to continue. " % ((i+1), plate_slots[i], (i+2), plate_slots[i+1]))
    else:
        check = input("Seal plate %s at location %s and centrifuge for 1 min at 1000 RPM. Replace tip box at E1. Place plate %s at location %s. Press enter when ready to continue. " % ((i+1), plate_slots[i], (i-1), plate_slots[i-1]))
    robot.resume()

for i in range(2):
    
    p1200_multi.start_at_tip(racks[0].rows("1"))

    to_remove_vol = [980, 980, 980, 980, 980, 900]
    to_remove_height = [25,20, 15, 6, 1, -1]

    loop_start_b = datetime.now()

    #Just about 7.5 minutes per plate
    for row in plates[i].rows():
        
        p1200_multi.pick_up_tip()

        for j in range(len(to_remove_vol)):
            p1200_multi.transfer(to_remove_vol[j], 
                row.bottom(to_remove_height[j]), 
                liquid_trash[i],
                air_gap = 10, 
                new_tip='never'
            )
            p1200_multi.delay(0.5)
            p1200_multi.blow_out()

        p1200_multi.drop_tip()

    print("Time for loop completion: %s" % (datetime.now() - loop_start_b))

    robot.pause()
    check = input("Add 20 mL lysis buffer into column %s of 12-col divided plate and plate at A2. Press enter to continue " % (src_row_lysis))
    robot.resume()

    loop_start_c = datetime.now()

    #Just about 4 minutes
    for dst_row in plates[i].rows():
        p1200_multi.pick_up_tip()

        p1200_multi.transfer(300, 
            lysis_etoh.rows(str(src_row_lysis)),
            dst_row.bottom(),
            air_gap = 20,
            new_tip="never"
        )

        p1200_multi.mix(10, 200, dst_row.bottom())
        p1200_multi.blow_out()
        p1200_multi.drop_tip()

    print("Time for loop completion: %s" % (datetime.now() - loop_start_c))
    print("Time for loop completion: %s" % (datetime.now() - loop_start_a)) 
    
    if i==0:
        src_row_lysis += 1


    robot.pause()
    check = input("Remove plate %s at position %s and incubate for 10 minutes at 60C. Replace tip box at E1. Press enter to continue " % ((i+1), plate_slots[i]))
    robot.resume()

    robot.home()

print("Total time: %s" % (datetime.now()-start))
