# """test authentication"""
# import unittest
# import json
# import psycopg2
# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)
# import sys
# sys.path.append('../')
# from api.__init__ import app
# from db.database import DatabaseConnection


# class TestStoreManagerApi(unittest.TestCase):
#     """TestStoreManagerApi(unittest.TestCase)--holds all tests we shall perform"""
#     def setUp(self):
#         """setUp(self)---"""
#         self.db = DatabaseConnection()
#         self.app = app.test_client()
#         self.db.create_tables()
#         self.db.default_admin()
#         self.product = {
#             "product_name": "Sugar",
#             "category":"Food",
#             "unit_price":4100,
#             "quantity": 20,
#             "measure":"Kgs"
#         }
#         self.invalidproduct = {
#             "product_id":1,
#             "product_name": "",
#             "category":"",
#             "unit_price":"",
#             "quantity": 20,
#             "measure":""
#         }
#         self.badpriceandquantity = {
#             "product_id":1,
#             "product_name": "Sugar",
#             "category":"Food",
#             "unit_price":"4100",
#             "quantity": "20",
#             "measure":"Kgs"
#         }
#         self.sale = {
#             "user_id":2,
#             "product_id": 1,
#             "quantity":6
#         }
#         self.user_admin = {
#             "user_name":'vickib',
#             "password":'vibel',
#             "role":'admin'
#         }
#         self.user_attendant = {
#             "user_name":'attendant',
#             "password":'attendant',
#             "role" : 'attendant'
#         }
#         self.user = {
#             "name":"attendant",
#             "user_name":'attendant',
#             "password":'attendant',
#             "role" : 'attendant'
#         }

#     def test_create_product_with_valid_fields(self):
#         """create product with valid fields"""
#         res = self.app.post("/api/v2/products",
#                             data=json.dumps(self.product),
#                             content_type='application/json')
#         res_data = json.loads(res.data)
#         expected_output = {
#             "Success": "you have added a product"
#         }
#         self.assertEqual(res.status_code, 201)
#         self.assertEqual(res_data, expected_output)

#     def test_create_product_with_empty_fields(self):
#         """create product with invalid fields"""
        
#         res = self.app.post("/api/v2/products",
#                             data=json.dumps(self.invalidproduct),
#                             content_type='application/json')
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "fields should not be empty"
#         }
#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(res_data, expected_output)
    
#     def test_create_product_with_string_price_quantity(self):
#         """create product with string price and quantity fields"""
        
#         res = self.app.post("/api/v2/products",
#                             data=json.dumps(self.badpriceandquantity),
#                             content_type='application/json')
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "unit price and quantity have to be integers"
#         }
#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(res_data, expected_output)
    
#     def test_post_products_valid_admin(self):
#         """test_post_products(self)"""
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         response_product = self.app.post("/api/v2/products",
#                                          data=json.dumps(self.product),
#                                          content_type='application/json',
#                                          headers=headers)
#         self.assertEqual(response_product.status_code, 201) 

#     def test_post_products_valid_attendant(self):
#         """test_post_products(self)"""
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         #create attendant
#         self.app.post("/api/v2/auth/signup",
#                             content_type='application/json',
#                             headers=headers,
#                             data=json.dumps(self.user))
#         #login attendant
#         res = self.app.post('/api/v2/auth/login',
#                                 content_type='application/json',
#                                 data=json.dumps(self.user_attendant))
#         datat = json.loads(res.data)
#         tokent = datat.get('access_token')
#         headerst = {'Authorization': f'Bearer {tokent}'}
#         response_product = self.app.post("/api/v2/products",
#                                          data=json.dumps(self.product),
#                                          content_type='application/json',
#                                          headers=headerst)
#         self.assertEqual(response_product.status_code, 201)

#     def test_get_all_products(self):
#         """Test getting all products user"""
#         self.app.post("/api/v2/products",
#                             data=json.dumps(self.product),
#                             content_type='application/json')

#         res = self.app.get("/api/v2/products",
#                            content_type='application/json')
#         self.assertEqual(res.status_code, 200)
    
#     def test_get_one_product(self):
#         """test__get_one_product(self)---"""
#         self.app.post("/api/v2/products",
#                             data=json.dumps(self.product),
#                             content_type='application/json')

#         res = self.app.get("/api/v2/products/1",
#                            content_type='application/json')
#         self.assertEqual(res.status_code, 200)
    
#     def test_get_one_product_not_exist(self):
#         """test_get_one_product_not_exist(self)---"""
#         self.app.post("/api/v2/products",
#                             data=json.dumps(self.product),
#                             content_type='application/json')

#         res = self.app.get("/api/v2/products/3",
#                            content_type='application/json')
#         self.assertEqual(res.status_code, 404)
    
#     def test_get_all_products_admin(self):
#         """Test getting all products user"""
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         self.app.post("/api/v2/products",
#                             data=json.dumps(self.product),
#                             content_type='application/json',
#                             headers=headers)

#         res = self.app.get("/api/v2/products",
#                            content_type='application/json',
#                            headers=headers)
#         self.assertEqual(res.status_code, 200)
    
#     def test_get_one_product_attendant(self):
#         """test__get_one_product(self)_attendant---"""
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         #create attendant
#         self.app.post("/api/v2/auth/signup",
#                             content_type='application/json',
#                             headers=headers,
#                             data=json.dumps(self.user))
#         #login attendant
#         res = self.app.post('/api/v2/auth/login',
#                                 content_type='application/json',
#                                 data=json.dumps(self.user_attendant))
#         datat = json.loads(res.data)
#         tokent = datat.get('access_token')
#         headerst = {'Authorization': f'Bearer {tokent}'}
#         self.app.post("/api/v2/products",
#                             data=json.dumps(self.product),
#                             content_type='application/json',
#                             headers=headerst)

#         res = self.app.get("/api/v2/products/1",
#                            content_type='application/json',
#                            headers = headerst)
#         self.assertEqual(res.status_code, 200)
    
#     def test_modifyproduct_admin(self):
#         """test_modifyproduct_admin"""
#         updateProduct = {
#                 'category':"Food",
#                 'unit_price':4200,
#                 'quantity':10,
#                 'measure':"Kgs"
#                 }
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         self.app.post("/api/v2/products",
#                             data=json.dumps(self.product),
#                             content_type='application/json',
#                             headers=headers)
#         res = self.app.put("/api/v2/products/1",
#                             data=json.dumps(updateProduct),
#                             content_type='application/json',
#                             headers=headers)
#         self.assertEqual(res.status_code, 200)
    
#     def test_modifyproduct_attendant(self):
#         """test_modifyproduct_attendant"""
#         updateProduct = {
#                 'category':"Food",
#                 'unit_price':4200,
#                 'quantity':10,
#                 'measure':"Kgs"
#                 }
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         #create attendant
#         self.app.post("/api/v2/auth/signup",
#                             content_type='application/json',
#                             headers=headers,
#                             data=json.dumps(self.user))
#         #login attendant
#         res = self.app.post('/api/v2/auth/login',
#                                 content_type='application/json',
#                                 data=json.dumps(self.user_attendant))
#         datat = json.loads(res.data)
#         tokent = datat.get('access_token')
#         headerst = {'Authorization': f'Bearer {tokent}'}
#         self.app.post("/api/v2/products",
#                             data=json.dumps(self.product),
#                             content_type='application/json',
#                             headers=headerst)
#         res = self.app.put("/api/v2/products/1",
#                             data=json.dumps(updateProduct),
#                             content_type='application/json',
#                             headers=headerst)
#         self.assertEqual(res.status_code, 401)

#     def test_modifyproduct_not_exist(self):
#         """test_modifyproduct_not_exist"""
#         updateProduct = {
#                 'category':"Food",
#                 'unit_price':4200,
#                 'quantity':10,
#                 'measure':"Kgs"
#                 }
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         self.app.post("/api/v2/products",
#                             data=json.dumps(self.product),
#                             content_type='application/json',
#                             headers=headers)
#         res = self.app.put("/api/v2/products/3",
#                             data=json.dumps(updateProduct),
#                             content_type='application/json',
#                             headers=headers)
#         self.assertEqual(res.status_code, 404)

#     def test_delete_product_admin(self):
#         """test delete a product"""        
#         self.app.post("/api/v2/products",
#                             data=json.dumps(self.product),
#                             content_type='application/json')
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         res = self.app.delete("/api/v2/products/1",
#                             content_type='application/json',
#                             headers = headers)
#         self.assertEqual(res.status_code, 200)
    
#     def test_delete_product_admin_not_exist(self):
#         """test delete a product"""        
#         self.app.post("/api/v2/products",
#                             data=json.dumps(self.product),
#                             content_type='application/json')
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         res = self.app.delete("/api/v2/products/2",
#                             content_type='application/json',
#                             headers = headers)
#         self.assertEqual(res.status_code, 404)
    
#     def test_delete_product_attendant(self):
#         """test delete a product"""        
#         self.app.post("/api/v2/products",
#                             data=json.dumps(self.product),
#                             content_type='application/json')
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         #create attendant
#         self.app.post("/api/v2/auth/signup",
#                             content_type='application/json',
#                             headers=headers,
#                             data=json.dumps(self.user))
#         #login attendant
#         res = self.app.post('/api/v2/auth/login',
#                                 content_type='application/json',
#                                 data=json.dumps(self.user_attendant))
#         datat = json.loads(res.data)
#         tokent = datat.get('access_token')
#         headerst = {'Authorization': f'Bearer {tokent}'}
#         res = self.app.delete("/api/v2/products/1",
#                             content_type='application/json',
#                             headers = headerst)
#         self.assertEqual(res.status_code, 401)
    
#     def test_signup(self):
#         """
#         Test registration with unathenticated user
#         """
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         res = self.app.post("/api/v2/auth/signup",
#                             content_type='application/json',
#                             headers=headers,
#                             data=json.dumps(self.user))
#         res_data = json.loads(res.data)
#         self.assertEqual(res.status_code, 201)
    
#     def test_login_unregistered(self):
#         """Test login with invalid data"""
        
#         res = self.app.post('/api/v2/auth/login',
#                             data=json.dumps(self.user_attendant),
#                             content_type='application/json')
#         self.assertEqual(res.status_code, 404)
    
#     def test_login_registered_admin(self):
#         """Test login with valid data"""
        
#         res = self.app.post('/api/v2/auth/login',
#                             data=json.dumps(self.user_admin),
#                             content_type='application/json')
#         self.assertEqual(res.status_code, 200)
    
#     def test_login_registered_attendant(self):
#         """Test login with valid data"""
        
#         #login admin
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         #create attendant
#         self.app.post("/api/v2/auth/signup",
#                             content_type='application/json',
#                             headers=headers,
#                             data=json.dumps(self.user))
#         #login attendant
#         res = self.app.post('/api/v2/auth/login',
#                                 content_type='application/json',
#                                 data=json.dumps(self.user_attendant))
#         self.assertEqual(res.status_code, 200)
    
#     def test_make_sale(self):
#         #login admin
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         #create attendant
#         self.app.post("/api/v2/auth/signup",
#                             content_type='application/json',
#                             headers=headers,
#                             data=json.dumps(self.user))
#         #login attendant
#         res = self.app.post('/api/v2/auth/login',
#                                 content_type='application/json',
#                                 data=json.dumps(self.user_attendant))
#         datat = json.loads(res.data)
#         tokent = datat.get('access_token')
#         headerst = {'Authorization': f'Bearer {tokent}'}
#         #post products
#         self.app.post('/api/v2/products',
#                       data=json.dumps(self.product),
#                       content_type='application/json',
#                       headers=headerst)
#         #make sale
#         res2  = self.app.post('/api/v2/sales',
#                               headers = headerst,
#                               content_type='application/json',
#                               data = json.dumps(self.sale))
#         self.assertEqual(res2.status_code, 201)
    
#     def test_get_sales_admin(self):
#         #login admin
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         #create attendant
#         self.app.post("/api/v2/auth/signup",
#                             content_type='application/json',
#                             headers=headers,
#                             data=json.dumps(self.user))
#         #login attendant
#         res = self.app.post('/api/v2/auth/login',
#                                 content_type='application/json',
#                                 data=json.dumps(self.user_attendant))
#         datat = json.loads(res.data)
#         tokent = datat.get('access_token')
#         headerst = {'Authorization': f'Bearer {tokent}'}
#         #post products
#         self.app.post('/api/v2/products',
#                       data=json.dumps(self.product),
#                       content_type='application/json',
#                       headers=headerst)
#         #make sale
#         self.app.post('/api/v2/sales',
#                               headers = headerst,
#                               content_type='application/json',
#                               data = json.dumps(self.sale))
        
#         #login as admin
#         response2= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data2 = json.loads(response2.data.decode())
#         token2 = data2.get('access_token')
#         headers2 = {'Authorization': f'Bearer {token2}'}

#         #get sale
#         res3= self.app.get('/api/v2/sales',
#                       content_type='application/json',
#                       headers=headers2)
#         self.assertEqual(res3.status_code, 200)
    
#     def test_get_attendant_sale_admin(self):
#         #login admin
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         #create attendant
#         self.app.post("/api/v2/auth/signup",
#                             content_type='application/json',
#                             headers=headers,
#                             data=json.dumps(self.user))
#         #login attendant
#         res = self.app.post('/api/v2/auth/login',
#                                 content_type='application/json',
#                                 data=json.dumps(self.user_attendant))
#         datat = json.loads(res.data)
#         tokent = datat.get('access_token')
#         headerst = {'Authorization': f'Bearer {tokent}'}
#         #post products
#         self.app.post('/api/v2/products',
#                       data=json.dumps(self.product),
#                       content_type='application/json',
#                       headers=headerst)
#         #make sale
#         self.app.post('/api/v2/sales',
#                               headers = headerst,
#                               content_type='application/json',
#                               data = json.dumps(self.sale))
        
#         #login as admin
#         response2= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data2 = json.loads(response2.data.decode())
#         token2 = data2.get('access_token')
#         headers2 = {'Authorization': f'Bearer {token2}'}

#         #get sale
#         res3= self.app.get('/api/v2/sales/2',
#                       content_type='application/json',
#                       headers=headers2)
#         self.assertEqual(res3.status_code, 200)
    
#     def test_get_attendant_sale_admin_not_exists(self):
#         #login admin
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         #create attendant
#         self.app.post("/api/v2/auth/signup",
#                             content_type='application/json',
#                             headers=headers,
#                             data=json.dumps(self.user))
#         #login attendant
#         res = self.app.post('/api/v2/auth/login',
#                                 content_type='application/json',
#                                 data=json.dumps(self.user_attendant))
#         datat = json.loads(res.data)
#         tokent = datat.get('access_token')
#         headerst = {'Authorization': f'Bearer {tokent}'}
#         #post products
#         self.app.post('/api/v2/products',
#                       data=json.dumps(self.product),
#                       content_type='application/json',
#                       headers=headerst)
#         #make sale
#         self.app.post('/api/v2/sales',
#                               headers = headerst,
#                               content_type='application/json',
#                               data = json.dumps(self.sale))
        
#         #login as admin
#         response2= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data2 = json.loads(response2.data.decode())
#         token2 = data2.get('access_token')
#         headers2 = {'Authorization': f'Bearer {token2}'}

#         #get sale
#         res3= self.app.get('/api/v2/sales/1',
#                       content_type='application/json',
#                       headers=headers2)
#         self.assertEqual(res3.status_code, 404)
    
#     def test_get_attendant_sale_attendant(self):
#         #login admin
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         #create attendant
#         self.app.post("/api/v2/auth/signup",
#                             content_type='application/json',
#                             headers=headers,
#                             data=json.dumps(self.user))
#         #login attendant
#         res = self.app.post('/api/v2/auth/login',
#                                 content_type='application/json',
#                                 data=json.dumps(self.user_attendant))
#         datat = json.loads(res.data)
#         tokent = datat.get('access_token')
#         headerst = {'Authorization': f'Bearer {tokent}'}
#         #post products
#         self.app.post('/api/v2/products',
#                       data=json.dumps(self.product),
#                       content_type='application/json',
#                       headers=headerst)
#         #make sale
#         self.app.post('/api/v2/sales',
#                               headers = headerst,
#                               content_type='application/json',
#                               data = json.dumps(self.sale))

#         #get sale
#         res3= self.app.get('/api/v2/sales/2',
#                       content_type='application/json',
#                       headers=headerst)
#         self.assertEqual(res3.status_code, 200)
    
#     def test_get_attendant_sale_attendant_not_exist(self):
#         #login admin
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         #create attendant
#         self.app.post("/api/v2/auth/signup",
#                             content_type='application/json',
#                             headers=headers,
#                             data=json.dumps(self.user))
#         #login attendant
#         res = self.app.post('/api/v2/auth/login',
#                                 content_type='application/json',
#                                 data=json.dumps(self.user_attendant))
#         datat = json.loads(res.data)
#         tokent = datat.get('access_token')
#         headerst = {'Authorization': f'Bearer {tokent}'}
#         #post products
#         self.app.post('/api/v2/products',
#                       data=json.dumps(self.product),
#                       content_type='application/json',
#                       headers=headerst)
#         #make sale
#         self.app.post('/api/v2/sales',
#                               headers = headerst,
#                               content_type='application/json',
#                               data = json.dumps(self.sale))

#         #get sale
#         res3= self.app.get('/api/v2/sales/1',
#                       content_type='application/json',
#                       headers=headerst)
#         self.assertEqual(res3.status_code, 404)
    
#     def test_getusers_admin(self):
#         #login as admin
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}

#         #get users
#         res= self.app.get('/api/v2/users',
#                       content_type='application/json',
#                       headers=headers)
#         self.assertEqual(res.status_code, 200)
    
#     def test_getadminusers_admin(self):
#         #login as admin
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}

#         #get users
#         res= self.app.get('/api/v2/users/admin',
#                       content_type='application/json',
#                       headers=headers)
#         self.assertEqual(res.status_code, 200)
    
#     def test_getusers_attendant(self):
#         #login admin
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         #create attendant
#         self.app.post("/api/v2/auth/signup",
#                             content_type='application/json',
#                             headers=headers,
#                             data=json.dumps(self.user))
#         #login attendant
#         res = self.app.post('/api/v2/auth/login',
#                                 content_type='application/json',
#                                 data=json.dumps(self.user_attendant))
#         datat = json.loads(res.data)
#         tokent = datat.get('access_token')
#         headerst = {'Authorization': f'Bearer {tokent}'}
#         #get users
#         res= self.app.get('/api/v2/users',
#                       content_type='application/json',
#                       headers=headerst)
#         self.assertEqual(res.status_code, 401)
    
#     def test_getattendantusers_admin(self):
#         #login admin
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         #create attendant
#         self.app.post("/api/v2/auth/signup",
#                             content_type='application/json',
#                             headers=headers,
#                             data=json.dumps(self.user))
#         #get users
#         res= self.app.get('/api/v2/users/attendant',
#                       content_type='application/json',
#                       headers=headers)
#         self.assertEqual(res.status_code, 200)

#     def test_logout_admin(self):
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}

#         res = self.app.delete('/api/v2/auth/logout',
#                               content_type='application/json',
#                               headers=headers)
#         self.assertEquals(res.status_code, 200)
    
#     def test_logout_attendant(self):
#         response= self.app.post('/api/v2/auth/login',
#                                 data=json.dumps(self.user_admin),
#                                 content_type='application/json')
#         data = json.loads(response.data.decode())
#         token = data.get('access_token')
#         headers = {'Authorization': f'Bearer {token}'}
#         #create attendant
#         self.app.post("/api/v2/auth/signup",
#                             content_type='application/json',
#                             headers=headers,
#                             data=json.dumps(self.user))
#         #login attendant
#         res = self.app.post('/api/v2/auth/login',
#                                 content_type='application/json',
#                                 data=json.dumps(self.user_attendant))
#         datat = json.loads(res.data)
#         tokent = datat.get('access_token')
#         headerst = {'Authorization': f'Bearer {tokent}'}

#         res2 = self.app.delete('/api/v2/auth/logout',
#                               content_type='application/json',
#                               headers=headers)
#         self.assertEquals(res2.status_code, 200)

#     def tearDown(self):
#         """tearDown(self)---"""
#         self.db = DatabaseConnection()
#         self.db.drop_tables()

# if __name__ == "__main__":
#     unittest.main()
