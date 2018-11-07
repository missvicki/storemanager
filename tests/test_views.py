"""test authentication"""
import unittest
import json
import psycopg2
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from ..api.views import app
from ..db.database import DatabaseConnection

class TestStoreManagerApi(unittest.TestCase):
    """TestStoreManagerApi(unittest.TestCase)--holds all tests we shall perform"""
    def setUp(self):
        """setUp(self)---"""
        self.db = DatabaseConnection()
        self.app = app.test_client()
        self.product = {
            "product_id":1,
            "product_name": "Sugar",
            "category":"Food",
            "unit-price":4100,
            "quantity": 20,
            "measure":"Kgs"
        }
        self.invalidproduct = {
            "product_id":1,
            "product_name": "",
            "category":"Food",
            "unit-price":"4100",
            "quantity": 20,
            "measure":"Kgs"
        }
        self.sale = {
            "user_id":1,
            "product_id": 1,
            "quantity":6
        }
        self.user_admin = {
            "username":'admin',
            "password":'admin',
            "role":'admin'
        }
        self.user_attendant = {
            "username":'attendant',
            "password":'attendant',
            "role" : 'attendant'
        }

    def test_get_all_products(self):
        """test_get_all_products(self)---"""

        res = self.app.post(
                '/api/v1/auth/login',
                data=json.dumps(self.user_attendant),
                content_type='application/json'
            )
        data = json.loads(res.data)
        token=data.get('message')
        headers = {'Authorization': f'Bearer {token}'}

        response_products = self.app.get("/api/v1/products")
        data_products = json.loads(response_products.data.decode('utf8'))
        self.assertEqual(response_products.status_code, 200, msg="Found Products")

    def test_get_all_sales(self):
        """test_get_all_sales(self)---"""
        res = self.app.post(
                '/api/v1/auth/login',
                data=json.dumps(self.user_admin),
                content_type='application/json'
            )
        data = json.loads(res.data)
        token=data.get('message')
        headers = {'Authorization': f'Bearer {token}'}

        response_sales = self.app.get("/api/v1/sales")
        data_sales = json.loads(response_sales.data.decode('utf8'))
        self.assertEqual(response_sales.status_code, 200, msg="Found Sales")

    def test_get_one_product(self):
        """test__get_one_product(self)---"""

        res = self.app.post(
                '/api/v1/auth/login',
                data=json.dumps(self.user_admin),
                content_type='application/json'
            )
        data = json.loads(res.data)
        token=data.get('message')
        headers = {'Authorization': f'Bearer {token}'}

        productid = self.db.getProducts()[0]["product_id"]
        response_product = self.app.get("/api/v1/products/"+int(productid))
        data_products = json.loads(response_product.data())
        self.assertEqual(response_product.status_code, 200, msg="Found Product")

    def test_product_not_exist(self):
        """test_product_not_exist(self) --"""
        res = self.app.post(
                '/api/v1/auth/login',
                data=json.dumps(self.user_admin),
                content_type='application/json'
            )
        data = json.loads(res.data)
        token=data.get('message')
        headers = {'Authorization': f'Bearer {token}'}

        response_product = self.app.get("/api/v1/products/2")
        self.assertEqual(response_product.status_code, 404, msg="Didn't find product")
    
    def test_post_products_valid_admin(self):
        """test_post_products(self)"""
        res = self.app.post(
                '/api/v1/auth/login',
                data=json.dumps(self.user_admin),
                content_type='application/json'
            )
        data = json.loads(res.data)
        token=data.get('message')
        headers = {'Authorization': f'Bearer {token}'}
        response_product = self.app.post("/api/v1/products",
                                      data=json.dumps(self.product),
                                      content_type='application/json',
                                      headers=headers)
        self.assertIn(b'Product successfully added', response_product.data) 

    def test_post_products_valid_attendant(self):
        """test_post_products(self)"""
        res = self.app.post(
                '/api/v1/auth/login',
                data=json.dumps(self.user_attendant),
                content_type='application/json'
            )
        data = json.loads(res.data)
        token=data.get('message')
        headers = {'Authorization': f'Bearer {token}'}
        response_product = self.app.post("/api/v1/products",
                                      data=json.dumps(self.product),
                                      content_type='application/json',
                                      headers=headers)
        self.assertIn(b'Product successfully added', response_product.data)      

    def test_post_products_invaliddata(self):
        """test_post_products(self)"""
        res = self.app.post(
                '/api/v1/auth/login',
                data=json.dumps(self.user_admin),
                content_type='application/json'
            )
        data = json.loads(res.data)
        token=data.get('message')
        headers = {'Authorization': f'Bearer {token}'}
        response_product = self.app.post("/api/v1/products",
                                      data=json.dumps(self.invalidproduct),
                                      content_type='application/json',
                                      headers=headers)
        self.assertIn(b'Product name, measure and category are strings, quantity and unit price are integers', response_product.data)      

    # def test_edit_product(self):


    def test_delete_product(self):
        res = self.app.post(
                '/api/v1/auth/login',
                data=json.dumps(self.user_admin),
                content_type='application/json'
            )
        data = json.loads(res.data)
        token=data.get('message')
        headers = {'Authorization': f'Bearer {token}'}

        response = self.app.delete("/api/v1/products/1")
        response_product = self.app.post("/api/v1/products",
                                      data=json.dumps(self.product),
                                      content_type='application/json',
                                      headers=headers)
        self.assertEqual(response_product.status_code, 200, msg="Product has been deleted")
        response_product = self.app.post("/api/v1/products",
                                      data=json.dumps(self.invalidproduct),
                                      content_type='application/json',
                                      headers=headers)
        response = self.app.delete("/api/v1/products/20")
        self.assertEqual(response_product.status_code, 404, msg="Product has not been deleted")

    def test_sale_not_exist(self):
        """test_sale_not_exist(self) --"""
        res = self.app.post(
                '/api/v1/auth/login',
                data=json.dumps(self.user_admin),
                content_type='application/json'
            )
        data = json.loads(res.data)
        token=data.get('message')
        headers = {'Authorization': f'Bearer {token}'}
        response_sale = self.app.get("/api/v1/sales/20")
        self.assertEqual(response_sale.status_code, 404, "Didn't find sale")
    
    def test_post_sales(self):
        """test_post_sales(self)"""
        
        res = self.app.post(
                '/api/v1/auth/login',
                data=json.dumps(self.user_attendant),
                content_type='application/json'
            )
        data = json.loads(res.data)
        token=data.get('message')
        headers = {'Authorization': f'Bearer {token}'}

        sale = {"sale_id": 4, "product_id": 6,
                "quantity": 1}
        response_sale = self.app.post("/api/v1/sales/1",
                                      data=json.dumps(sale),
                                      content_type='application/json')
        self.assertEqual(response_sale.status_code, 201, msg="sale added")
        data = json.loads(response_sale.get_data())
        print(data)

    def tearDown(self):
        """tearDown(self)---"""
        self.db.drop_tables()


if __name__ == "__main__":
    unittest.main()
