def load_item(drone, warehouse, product, number):
    print '{} L {} {} {}'.format(drone, warehouse, product, number)

def unload_item(drone, warehouse, product, number):
    print '{} U {} {} {}'.format(drone, warehouse, product, number)

def deliver_item(drone, customer, product, number):
    print '{} D {} {} {}'.format(drone, warehouse, product, number)

def wait(drone, time):
    print '{} W {} {} {}'.format(drone, time)
