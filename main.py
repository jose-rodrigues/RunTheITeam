import math
import parser
import operations

from warehouse import Warehouse

nb_octet = 0
instructions = []
data = parser.get_data()
nb_order = data['orders']['number']
nb_warehouse = data['warehouses']['number']

class Drone:
    def __init__(self, id):
        self.id = id
        self.item_list = {}
        self.at_warehouse = True
        self.position_id = 0
        self.payload = 0
        self.tick = 0

    def go_to_delivery(self, order_id):
        if len(self.item_list) > 0:
            if self.at_warehouse:
                for item_id, nb_item in self.item_list.iteritems():
                    self.tick = self.tick + 1
                    if self.tick < data['turns']:
                        instructions.append('{} L {} {} {}'.format(self.id, self.position_id, item_id, nb_item))
                self.at_warehouse = False
                self.tick += warehouse_distance_mat[order_id][self.position_id]
                self.position_id = order_id
            for item_id, nb_item in self.item_list.iteritems():
                self.tick = self.tick + 1
                if self.tick < data['turns']:
                    instructions.append('{} D {} {} {}'.format(self.id, self.position_id, item_id, nb_item))
            self.item_list = {}

    def load_item(self, warehouse_id, item_id):
        if not self.at_warehouse:
            self.tick += warehouse_distance_mat[self.position_id][warehouse_id]
            self.at_warehouse = True
            self.position_id = warehouse_id
        elif self.position_id != warehouse_id:
            if self.position_id > warehouse_id:
                self.tick += w_to_w_mat[self.position_id][warehouse_id]
            else:
                self.tick += w_to_w_mat[warehouse_id][self.position_id]
        if not item_id in self.item_list:
            self.item_list[item_id] =  1
        else:
            self.item_list[item_id] = self.item_list[item_id] + 1
        self.payload += data['products']['weights'][item_id]

    def can_fit(self, item_id):
        return self.payload + data['products']['weights'][item_id] <= data['max_payload']

    def get_tick_val_to_warehouse(self, warehouse_id):
        if self.at_warehouse and self.position_id == warehouse_id:
            return self.tick
        elif self.at_warehouse:
            if self.position_id > warehouse_id:
                return self.tick + w_to_w_mat[self.position_id][warehouse_id]
            else:
                return self.tick + w_to_w_mat[warehouse_id][self.position_id]
        else:
            return self.tick + warehouse_distance_mat[self.position_id][warehouse_id]


def get_order_distance_mat():
    order_distance_mat = [[-1 for i in range(nb_order)] for j in range(nb_order)]
    for i in range(0, nb_order):
        for j in range(i + 1, nb_order):
            x1 = data['orders']['informations'][i]['location']['x']
            x2 = data['orders']['informations'][j]['location']['x']
            y1 = data['orders']['informations'][i]['location']['y']
            y2 = data['orders']['informations'][j]['location']['y']
            order_distance_mat[i][j] = int(math.ceil(math.sqrt((x2 - x1)**2 + (y2 - y1)**2)))
    return order_distance_mat

def get_warehouse_distance_mat():
    warehouse_distance_mat = [[-1 for i in range(nb_warehouse)] for j in range(nb_order)]
    for i in range(0, nb_order):
        for j in range(0, nb_warehouse):
            x1 = data['orders']['informations'][i]['location']['x']
            x2 = data['warehouses']['informations'][j]['location']['x']
            y1 = data['orders']['informations'][i]['location']['y']
            y2 = data['warehouses']['informations'][j]['location']['y']
            warehouse_distance_mat[i][j] = int(math.ceil(math.sqrt((x2 - x1)**2 + (y2 - y1)**2)))
    return warehouse_distance_mat

def get_warehouse_to_warehouse_mat():
    order_distance_mat = [[-1 for i in range(nb_warehouse)] for j in range(nb_warehouse)]
    for i in range(0, nb_warehouse):
        for j in range(i + 1, nb_warehouse):
            x1 = data['warehouses']['informations'][i]['location']['x']
            x2 = data['warehouses']['informations'][j]['location']['x']
            y1 = data['warehouses']['informations'][i]['location']['y']
            y2 = data['warehouses']['informations'][j]['location']['y']
            order_distance_mat[i][j] = int(math.ceil(math.sqrt((x2 - x1)**2 + (y2 - y1)**2)))
    return order_distance_mat

def get_next_drone(warehouse_id):
    min_drone_id = 0
    min_drone_tick = data['turns']
    for drone in drones:
        if drone.get_tick_val_to_warehouse(warehouse_id) < min_drone_tick:
            min_drone_id = drone.id
            min_drone_tick = drone.get_tick_val_to_warehouse(warehouse_id)
    return min_drone_id

def deliver():
    current_drone_id = 0
    for current_warehouse_id in range(nb_warehouse):
        closest_orders = sorted(range(nb_order), key=lambda k: warehouse_distance_mat[k][current_warehouse_id])
        for order in closest_orders:
            for item in data['orders']['informations'][order]['items']['products']:
                if item != -1 and warehouses[current_warehouse_id].has_items(item):
                    if drones[current_drone_id].can_fit(item):
                        idx = data['orders']['informations'][order]['items']['products'].index(item)
                        data['orders']['informations'][order]['items']['products'][idx] = -1
                        warehouses[current_warehouse_id].load_item(item)
                        drones[current_drone_id].load_item(current_warehouse_id, item)
                    else:
                        drones[current_drone_id].go_to_delivery(order)

                        current_drone_id = get_next_drone(current_warehouse_id)
                        warehouses[current_warehouse_id].load_item(item)

                        idx = data['orders']['informations'][order]['items']['products'].index(item)
                        data['orders']['informations'][order]['items']['products'][idx] = -1
                        drones[current_drone_id].load_item(current_warehouse_id, item)
            drones[current_drone_id].go_to_delivery(order)
            current_drone_id = get_next_drone(current_warehouse_id)

warehouse_distance_mat = get_warehouse_distance_mat()
w_to_w_mat = get_warehouse_to_warehouse_mat()
drones = [Drone(i) for i in range(data['drones'])]
warehouses = [Warehouse(i, data) for i in range(nb_warehouse)]
deliver()


print len(instructions)
# print 'nb drone:', data['drones']
# print 'turns: ', data['turns']
# print 'max: ', data['drones'] * data['turns']
print '\n'.join(instructions)
