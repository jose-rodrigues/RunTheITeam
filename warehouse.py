class Warehouse:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        self.items = self.data['warehouses']['informations'][id]['products']
        self.position = self.data['warehouses']['informations'][id]['location']

    def load_item(self, item_id):
        self.items[item_id] -= 1

    def has_items(self, item_id):
        return item_id < len(self.items) and self.items[item_id] > 0
