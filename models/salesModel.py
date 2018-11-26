"""structure models"""
class Sales:
    """sale model"""
    def __init__(self, user_name, product_id, quantity, total):
        self.user_name = user_name
        self.product_id = product_id
        self.quantity =quantity
        self.total = total
