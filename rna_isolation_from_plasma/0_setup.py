#fix from https://github.com/OpenTrons/opentrons/issues/314
def create_container_instance(name, grid, spacing, diameter, depth,
                              volume=0, slot=None, label=None):
    from opentrons import robot
    from opentrons.containers.placeable import Container, Well
    
    if slot is None:
        raise RuntimeError('"slot" argument is required.')
    if label is None:
        label = name
    columns, rows = grid
    col_spacing, row_spacing = spacing
    custom_container = Container()
    well_properties = {
        'type': 'custom',
        'diameter': diameter,
        'height': depth,
        'total-liquid-volume': volume
    }

    for r in range(rows):
        for c in range(columns):
            well = Well(properties=well_properties)
            well_name = chr(c + ord('A')) + str(1 + r)
            coordinates = (c * col_spacing, r * row_spacing, 0)
            custom_container.add(well, well_name, coordinates)

    # if a container is added to Deck AFTER a Pipette, the Pipette's
    # Calibrator must update to include all children of Deck
    for _, instr in robot.get_instruments():
        if hasattr(instr, 'update_calibrator'):
            instr.update_calibrator()
            
    custom_container.properties['type'] = name
    custom_container.get_name = lambda: label

    # add to robot deck
    robot.deck[slot].add(custom_container, label)

    return custom_container

#HELPER FUNCTIONS

#For step 2
def get_source_idx(dest_well):
    src_rack_idx = 0
    src_well = dest_well

    if (dest_well > 23):
        src_well = dest_well - 24
        src_rack_idx = 1

    return (src_rack_idx, src_well)


# create_container_instance(
#     '48-well-7mL-EK-2043',
#     grid =(8,6), #cols,rows
#     spacing=(9,18), #mm spacing between each col,row
#     diameter=8.5,
#     depth=65, #depth mm of each well 
#     slot=slot_i
# )

# create_container_instance(
#     '96-well-1mL-Axygen',
#     grid =(8,12), #cols,rows
#     spacing=(8,8), #mm spacing between each col,row
#     diameter=8,
#     depth=15, #depth mm of each well 
#     slot=slot_i
# )

# create_container_instance(
#     '96-well-300mL-EK-2035-S',
#     grid =(8,12), #cols,rows
#     spacing=(8,8), #mm spacing between each col,row
#     diameter=8,
#     depth=15, #depth mm of each well 
#     slot=slot_i
# )

# create_container_instance(
#     'rainin-tiprack-1200ul',
#     grid =(8,12), #cols,rows
#     spacing=(9.1,8.8), #mm spacing between each col,row
#     diameter=8,
#     depth=110, #depth mm of each well 
#     slot=slot_i
# )
