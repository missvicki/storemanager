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
            "product_name": "Sugar",
            "category":"Food",
            "unit_price":4100,
            "quantity": 20,
            "measure":"Kgs"
        }
        self.invalidproduct = {
            "product_id":1,
            "product_name": "",
            "category":"Food",
            "unit_price":"4100",
            "quantity": 20,
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
        
        response = self.app.post("/api/v1/auth/login",
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
        res = self.app.post("/api/v1/products",
                            data=json.dumps(self.product),
                            content_type='application/json',
                            headers=self.headers)
        res_data = json.loads(res.data)
        expected_output = {
            "Success": "you have added a product"
        }
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res_data, expected_output)

    def test_create_product_with_invalid_fields(self):
        """create product with invalid fields"""
        
        res = self.app.post("/api/v1/products",
                            data=json.dumps(self.invalidproduct),
                            content_type='application/json',
                            headers=self.headers)
        res_data = json.loads(res.data)
        expected_output = {
            "error": "fields should not be empty"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    def test_get_all_products(self):
        """Test getting all products user"""
        res2 = self.app.get("/api/v1/products",
                           content_type='application/json',
                           headers=self.headers)
        res_data = json.loads(res2.data)
        exepected_output = {
            "message": "There are no products"
        }
        self.assertEqual(res2.status_code, 404)
        self.assertEqual(res_data, exepected_output)

    # def test_get_all_sales(self):
    #     """Test getting all sales user"""
    #     res2 = self.app.get("/api/v1/sales",
    #                        content_type='application/json',
    #                        headers=self.headers)
    #     res_data = json.loads(res2.data)
    #     exepected_output = {
    #         "message": "There are no sales"
    #     }
    #     self.assertEqual(res2.status_code, 404)
    #     self.assertEqual(res_data, exepected_output)
    
    # def test_create_sale_with_valid_fields(self):
    #     """create sale with valid fields"""
    #     res = self.app.post("/api/v1/sales",
    #                         data=json.dumps(self.sale),
    #                         content_type='application/json',
    #                         headers=self.headers)
    #     res_data = json.loads(res.data)
    #     expected_output = {
    #         "Success": "you have added a sale"
    #     }
    #     self.assertEqual(res.status_code, 201)
    #     self.assertEqual(res_data, expected_output)

if __name__ == "__main__":
    unittest.main()
