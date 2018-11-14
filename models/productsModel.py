"""structure models"""
class Products:
    """product model"""
    def __init__(self, product_name, category, unit_price, quantity, measure):
        self.product_name = product_name
        self.category = category
        self.unit_price = unit_price
        self.quantity = quantity
        self.measure = measure