class Warehouse:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        self.items = self.data['warehouses']['informations'][id]['products']
        self.position = self.data['warehouses']['position']

    def load_item(self, item_id):
        idx = self.items.index(item_id)
        self.items.pop(idx)

    def has_items(self, item_id):
        return self.items.index(item_id) >= 0
