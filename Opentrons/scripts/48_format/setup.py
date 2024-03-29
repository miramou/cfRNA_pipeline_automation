
from opentrons import robot, containers, instruments
from opentrons.util import environment

robot.connect(robot.get_serial_ports_list()[0])
robot.is_connected()
robot.home()

environment.refresh()   # point python to your App's calibration file
print(environment.get_path('CALIBRATIONS_FILE'))   # should print the location of file

#Increase robot head speed - https://support.opentrons.com/ot-one/ot-one-defaults/ot-one-motor-speeds
## Default speed: {"x": 12000, "y": 12000, "z": 3000, "a": 700, "b": 700}
## Max speed: {"x": 20000,  "y": 20000,  "z": 6000, "a": 1200, "b": 1200}

robot.head_speed(x=18000, y=18000, z=3500, a=700, b=700) 


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
    src_well = dest_well

    if (dest_well > 23):
        src_well = dest_well - 24

    return src_well