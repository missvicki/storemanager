"""structure models"""
class Sales:
    """sale model"""
    def __init__(self, user_id, product_id, quantity, total):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity =quantity
        self.total = total
