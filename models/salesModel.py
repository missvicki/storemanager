"""structure models"""
class Sales:
    """sale model"""
    def __init__(self, user_id):
        self.user_id = user_id

class SalesHasProducts:
    """sales has products"""
    def __init__(self, sale_id, product_id, quantity, total):
        self.sale_id = sale_id
        self.product_id = product_id
        self.quantity =quantity
        self.total = total
        

