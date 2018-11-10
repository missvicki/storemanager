"""test authentication"""
import unittest
import json
import psycopg2
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import sys
sys.path.append('../')
from api.__init__ import app
from db.database import DatabaseConnection


class TestStoreManagerApi(unittest.TestCase):
    """TestStoreManagerApi(unittest.TestCase)--holds all tests we shall perform"""
    def setUp(self):
        """setUp(self)---"""
        self.db = DatabaseConnection()
        self.app = app.test_client()
        self.product = {
            "product_name": "Sugar",
            "category":"Food",
            "unit_price":4100,
            "quantity": 20,
            "measure":"Kgs"
        }
        self.invalidproduct = {
            "product_id":1,
            "product_name": "",
            "category":"",
            "unit_price":"",
            "quantity": 20,
            "measure":""
        }
        self.badpriceandquantity = {
            "product_id":1,
            "product_name": "Sugar",
            "category":"Food",
            "unit_price":"4100",
            "quantity": "20",
            "measure":"Kgs"
        }
        self.sale = {
            "user_id":1,
            "product_id": 1,
            "quantity":6
        }
        self.user_admin = {
            "username":'vickib',
            "password":'vibel',
            "role":'admin'
        }
        self.user_attendant = {
            "username":'attendant',
            "password":'attendant',
            "role" : 'attendant'
        }
        
        response = self.app.post("/api/v2/auth/login",
                                  content_type='application/json',
                                  data=json.dumps(self.user_admin))
        self.data = json.loads(response.data.decode())
        self.token = self.data.get('token')
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def tearDown(self):
        """tearDown(self)---"""
        self.db = DatabaseConnection()
        self.db.drop_tables()

    def test_create_product_with_valid_fields(self):
        """create product with valid fields"""
        res = self.app.post("/api/v2/products",
                            data=json.dumps(self.product),
                            content_type='application/json',
                            headers=self.headers)
        res_data = json.loads(res.data)
        expected_output = {
            "Success": "you have added a product"
        }
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res_data, expected_output)

    def test_create_product_with_empty_fields(self):
        """create product with invalid fields"""
        
        res = self.app.post("/api/v2/products",
                            data=json.dumps(self.invalidproduct),
                            content_type='application/json',
                            headers=self.headers)
        res_data = json.loads(res.data)
        expected_output = {
            "error": "fields should not be empty"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)
    
    def test_create_product_with_string_price_quantity(self):
        """create product with string price and quantity fields"""
        
        res = self.app.post("/api/v2/products",
                            data=json.dumps(self.badpriceandquantity),
                            content_type='application/json',
                            headers=self.headers)
        res_data = json.loads(res.data)
        expected_output = {
            "error": "unit price and quantity have to be integers"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)
    
    def test_post_products_valid_admin(self):
        """test_post_products(self)"""
        res = self.app.post(
                '/api/v2/auth/login',
                data=json.dumps(self.user_admin),
                content_type='application/json'
            )
        data = json.loads(res.data)
        token=data.get('message')
        headers = {'Authorization': f'Bearer {token}'}
        response_product = self.app.post("/api/v2/products",
                                      data=json.dumps(self.product),
                                      content_type='application/json',
                                      headers=headers)
        self.assertEqual(response_product.status_code, 201) 

    def test_post_products_valid_attendant(self):
        """test_post_products(self)"""
        res = self.app.post(
                '/api/v2/auth/login',
                data=json.dumps(self.user_attendant),
                content_type='application/json'
            )
        data = json.loads(res.data)
        token=data.get('message')
        headers = {'Authorization': f'Bearer {token}'}
        response_product = self.app.post("/api/v2/products",
                                      data=json.dumps(self.product),
                                      content_type='application/json',
                                      headers=headers)
        self.assertEqual(response_product.status_code, 201)

    def test_get_all_products(self):
        """Test getting all products user"""

        res = self.app.get("/api/v2/products",
                           content_type='application/json',
                           headers=self.headers)
        res_data_ = json.loads(res.data)
        exepected_output = {
            "message": "There are no products"
        }
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data_, exepected_output)
    
    def test_get_one_product(self):
        """test__get_one_product(self)---"""
        product_id=1
        res = self.app.get("/api/v2/products/{}".format(product_id),
                           content_type='application/json',
                           headers=self.headers)
        res_data_ = json.loads(res.data)
        exepected_output = {
            'message': "product has not been found"
        }
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data_, exepected_output)


if __name__ == "__main__":
    unittest.main()
