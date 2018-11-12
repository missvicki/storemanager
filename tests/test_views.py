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
        self.db.create_tables()
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
            "user_name":'vickib',
            "password":'vibel',
            "role":'admin'
        }
        self.user_attendant = {
            "user_name":'attendant',
            "password":'attendant',
            "role" : 'attendant'
        }
        self.user = {
            "name":"attendant",
            "user_name":'attendant',
            "password":'attendant',
            "role" : 'attendant'
        }

    def test_create_product_with_valid_fields(self):
        """create product with valid fields"""
        res = self.app.post("/api/v2/products",
                            data=json.dumps(self.product),
                            content_type='application/json')
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
                            content_type='application/json')
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
                            content_type='application/json')
        res_data = json.loads(res.data)
        expected_output = {
            "error": "unit price and quantity have to be integers"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)
    
    def test_post_products_valid_admin(self):
        """test_post_products(self)"""
        response= self.app.post('/api/v2/auth/login',
                                data=json.dumps(self.user_admin),
                                content_type='application/json')
        data = json.loads(response.data.decode())
        token = data.get('token')
        headers = {'Authorization': f'Bearer {token}'}
        response_product = self.app.post("/api/v2/products",
                                         data=json.dumps(self.product),
                                         content_type='application/json',
                                         headers=headers)
        self.assertEqual(response_product.status_code, 201) 

    def test_post_products_valid_attendant(self):
        """test_post_products(self)"""
        response = self.app.post('/api/v2/auth/login',
                                 data=json.dumps(self.user_attendant),
                                 content_type='application/json')
        data = json.loads(response.data.decode())
        token = data.get('token')
        headers = {'Authorization': f'Bearer {token}'}
        response_product = self.app.post("/api/v2/products",
                                         data=json.dumps(self.product),
                                         content_type='application/json',
                                         headers=headers)
        self.assertEqual(response_product.status_code, 201)

    def test_get_all_products(self):
        """Test getting all products user"""
        self.app.post("/api/v2/products",
                            data=json.dumps(self.product),
                            content_type='application/json')

        res = self.app.get("/api/v2/products",
                           content_type='application/json')
        self.assertEqual(res.status_code, 200)
    
    def test_get_one_product(self):
        """test__get_one_product(self)---"""
        self.app.post("/api/v2/products",
                            data=json.dumps(self.product),
                            content_type='application/json')

        res = self.app.get("/api/v2/products/1",
                           content_type='application/json')
        self.assertEqual(res.status_code, 200)
    
    def test_get_all_products_admin(self):
        """Test getting all products user"""
        response= self.app.post('/api/v2/auth/login',
                                data=json.dumps(self.user_admin),
                                content_type='application/json')
        data = json.loads(response.data.decode())
        token = data.get('token')
        headers = {'Authorization': f'Bearer {token}'}
        self.app.post("/api/v2/products",
                            data=json.dumps(self.product),
                            content_type='application/json',
                            headers=headers)

        res = self.app.get("/api/v2/products",
                           content_type='application/json',
                           headers=headers)
        self.assertEqual(res.status_code, 200)
    
    def test_get_one_product_attendant(self):
        """test__get_one_product(self)_attendant---"""
        response = self.app.post('/api/v2/auth/login',
                                 data=json.dumps(self.user_attendant),
                                 content_type='application/json')
        data = json.loads(response.data.decode())
        token = data.get('token')
        headers = {'Authorization': f'Bearer {token}'}
        self.app.post("/api/v2/products",
                            data=json.dumps(self.product),
                            content_type='application/json',
                            headers=headers)

        res = self.app.get("/api/v2/products/1",
                           content_type='application/json',
                           headers = headers)
        self.assertEqual(res.status_code, 200)
    
    def test_modifyproduct_admin(self):
        """test_modifyproduct_admin"""
        updateProduct = {
                'category':"Food",
                'unit_price':4200,
                'quantity':10,
                'measure':"Kgs"
                }
        response= self.app.post('/api/v2/auth/login',
                                data=json.dumps(self.user_admin),
                                content_type='application/json')
        data = json.loads(response.data.decode())
        token = data.get('token')
        headers = {'Authorization': f'Bearer {token}'}
        self.app.post("/api/v2/products",
                            data=json.dumps(self.product),
                            content_type='application/json',
                            headers=headers)
        res = self.app.put("/api/v2/products/1",
                            data=json.dumps(updateProduct),
                            content_type='application/json',
                            headers=headers)
        # self.assertEqual(res.status_code, 200)

    def test_delete_product_admin(self):
        """test delete a product"""        
        self.app.post("/api/v2/products",
                            data=json.dumps(self.product),
                            content_type='application/json')
        response= self.app.post('/api/v2/auth/login',
                                data=json.dumps(self.user_admin),
                                content_type='application/json')
        data = json.loads(response.data.decode())
        token = data.get('token')
        headers = {'Authorization': f'Bearer {token}'}
        res = self.app.delete("/api/v2/products/1",
                            content_type='application/json',
                            headers = headers)
        # self.assertEqual(res.status_code, 200)
    
    def test_signup(self):
        """
        Test registration with unathenticated user
        """
        response= self.app.post('/api/v2/auth/login',
                                data=json.dumps(self.user_admin),
                                content_type='application/json')
        data = json.loads(response.data.decode())
        token = data.get('token')
        headers = {'Authorization': f'Bearer {token}'}
        res = self.app.post("/api/v2/auth/signup",
                            content_type='application/json',
                            headers=headers,
                            data=json.dumps(self.user))
        res_data = json.loads(res.data)
        # self.assertEqual(res.status_code, 201)
    
    def test_login_unregistered(self):
        """Test login with valid data"""
        
        res = self.app.post('/api/v2/auth/login',
                            data=json.dumps(self.user_attendant),
                            content_type='application/json')
        self.assertEqual(res.status_code, 400)
    
    def test_make_sale(self):
        res = self.app.post('/api/v2/auth/login',
                                content_type='application/json',
                                data=json.dumps(self.user_attendant))
        data = json.loads(res.data)
        token = data.get('token')
        headers = {'Authorization': f'Bearer {token}'}

        self.app.post('/api/v2/products',
                      data=json.dumps(self.product),
                      content_type='application/json',
                      headers=headers)
        
        res2  = self.app.post('/api/v2/sales',
                              headers = headers,
                              content_type='application/json',
                              data = json.dumps(self.sale))
        # self.assertEqual(res.status_code, 201)

    def tearDown(self):
        """tearDown(self)---"""
        self.db = DatabaseConnection()
        self.db.drop_tables()

if __name__ == "__main__":
    unittest.main()
