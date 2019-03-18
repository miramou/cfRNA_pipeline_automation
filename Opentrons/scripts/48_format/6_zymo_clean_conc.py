##SCRIPT TO ZYMO CLEAN AND CONCENTRATE
##TIME TO RUN: ~1 hour (with centrifugation) for 12 rows
##TOTAL TIPS USED: 17 rows

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
start = datetime.now()
print("Step 6: Zymo Clean and Concentrate")
print("%s" % (start))

binding_etoh_src_row = 1 #binding and etoh
wash_src_row = 1 #prep and wash buffers 

start_row = int(sys.argv[1])
last_row = int(sys.argv[2])+1
max_vol = 1000
disposal_vol = 50

volumes = [226, 339, 400, 700, 400] #Binding, EtOH, RNA Prep, Wash, Wash
what_to_add = ["27 mL binding buffer", "50 mL EtOH", "48 mL RNA prep", "84 mL wash buffer","48 mL wash buffer"]


for i in range(5):   
    loop_start = datetime.now()

    if i < 2:
        robot.pause()
        check = input("Place sample plate at C1. Add %s to column %s at D1 reservoir. Press enter to continue. " % (what_to_add[i], binding_etoh_src_row))
        robot.resume()

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

        # if i == 1:
        #     robot.pause()
        #     check = input("Place filter plate at B1. Make sure there is a seal on both plates. You will peel this back sequentially. ")
        #     robot.resume()

        #     for row_i in range(start_row, last_row): 
        #         #loop_start_inner = datetime.now()

        #         robot.pause()
        #         check = input("Peel back seal from %s " % (row_i))
        #         robot.resume()

        #         p1200_multi.pick_up_tip()
        #         p1200_multi.mix(3, 500, sample_plate.rows(str(row_i)).bottom())
        #         p1200_multi.aspirate(900, sample_plate.rows(str(row_i)).bottom())
        #         p1200_multi.delay(0.5)
        #         p1200_multi.aspirate(100, sample_plate.rows(str(row_i)).top())
        #         p1200_multi.dispense(1000, filter_plate.rows(str(row_i)).bottom(10))
        #         p1200_multi.aspirate(200, filter_plate.rows(str(row_i)).bottom(20)) #air gap
        #         p1200_multi.drop_tip()

        #         #print("Loop completion time: %s" % (datetime.now() - loop_start_inner))

        #         if row_i == 10:
        #             p1200_multi.start_at_tip(racks[0].rows("1"))
        #             robot.pause()
        #             check = input("Change tip rack at E1. Press enter to continue. ")
        #             robot.resume()

        binding_etoh_src_row += 1

    else:
        robot.pause()
        check = input("Place filter plate at B1. Add %s to column %s at A1 reservoir. Press enter to continue. " % (what_to_add[i], wash_src_row))
        robot.resume()

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
    

    if i > 0:
        print("Centrifuge for 5 min at 3000-5000*g. ")
    
    print("Loop completion time: %s" % (datetime.now()-loop_start))

print("Total time: %s" % (datetime.now()-start))
robot.home()