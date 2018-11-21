"""!Flask web api for Store Manager"""
from flask import Flask, jsonify, request
from flask.views import MethodView
import datetime
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt)
from db.database import DatabaseConnection
from models.productsModel import Products
from models.salesModel import Sales
from models.usersModel import Users, Blacklist
from api.__init__ import app, jwt
from api.validations.validations import (validate_product, validate_product_modify, validate_user_signup, validate_user_login, validate_sales)

# what happens when you start the app
database = DatabaseConnection()
database.default_admin()

#storage engine to save revoked tokens
_db_ = DatabaseConnection()
blacklisted = _db_.fetch_blacklist_all()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklisted

#error handlers
@app.errorhandler(404)
def not_found(self, error):
    """ not_found(error) -returns error not found"""
    return jsonify({'error': 'NOT FOUND'}), 404

@app.errorhandler(400)
def bad_request(self, error):
    """ bad_request(error) -returns error bad request"""
    return jsonify({'error': 'BAD REQUEST'}), 400

@app.errorhandler(401)
def unauthorized(self, error):
    """ unauthorized(error) -returns error unauthorized"""
    return jsonify({'error': "NOT AUTHORIZED"}), 401

class ProductsView(MethodView):
    """class to do http methods eg get post put on products"""
    def get(self, product_id=None):
        """returns products"""
        if product_id:
            # get single product
            _product_ = database.getoneProduct(product_id)
            if not _product_:
                return jsonify({'message': "product has not been found"}), 404
            return jsonify({'product': _product_}), 200

        # get all products
        productget = database.getProducts()
        if not productget:
             return jsonify({'message': "There are no products"}), 404
        return jsonify({'products': productget}), 200  

    def post(self):
        """admins and attendants add products"""        
        data = request.get_json()
        prod_name = data.get('product_name')
        prod_cat = data.get('category')
        prod_price = data.get('unit_price')
        prod_qty = data.get('quantity')
        prod_meas = data.get('measure')
                
        valprod = validate_product(product_name=prod_name, 
                                   category=prod_cat, 
                                   unit_price=prod_price, 
                                   quantity=prod_qty, 
                                   measure=prod_meas)
        if valprod:
            return valprod

        obj_products = Products(prod_name, prod_cat, prod_price, prod_qty, prod_meas)
        database.insert_data_products(obj_products)
        return jsonify({"Success": "you have added a product"}), 201
    
    @jwt_required
    def put(self, product_id):
        """modifies a product"""
        #get the user who is currently logged in
        current_user = get_jwt_identity()
        jti = get_raw_jwt()['jti']
        revoked = database.fetch_blacklist(jti)

        if revoked:
            return jsonify({'msg': 'token already revoked'}), 401

        if not current_user == 'admin':
            return jsonify({"message": "You are not authorized"}), 401

        # check if product exists
        prod = database.check_product_exists_id(product_id)
        if not prod:
            return jsonify({"error": "product you are trying to modify does not exist"}), 404

        data = data = request.get_json()
        prod_cat = data.get('category')
        prod_price = data.get('unit_price')
        prod_qty = data.get('quantity')
        prod_meas = data.get('measure')

        valprod = validate_product_modify(category=prod_cat, 
                                          unit_price=prod_price, 
                                          quantity=prod_qty, 
                                          measure=prod_meas)
        if valprod:
            return valprod
        
        database.modify_product(prod_cat, prod_price, prod_qty, prod_meas, product_id)
        return jsonify({"Success": "product has been modified"}), 200
    
    @jwt_required
    def delete(self, product_id):
        # get the user who is currently logged in
        current_user = get_jwt_identity()
        jti = get_raw_jwt()['jti']
        revoked = database.fetch_blacklist(jti)

        if revoked:
            return jsonify({'msg': 'token already revoked'}), 401

        if not current_user == 'admin':
            return jsonify({"message": "You are not authorized"}), 401

        # check if product exists
        prod = database.check_product_exists_id(product_id)
        if not prod:
            return jsonify({"error": "product you are trying to modify does not exist"}), 404
        
        #deleting product
        database.deloneProduct(product_id)
        return jsonify({"message": "Product has been deleted successfully"}), 200
        
class UsersView(MethodView):
    """class to deal with html methods on users"""
    @jwt_required
    def get(self, role=None):
        """returns users"""
        current_user = get_jwt_identity()
        jti = get_raw_jwt()['jti']
        revoked = database.fetch_blacklist(jti)

        if revoked:
            return jsonify({'msg': 'token already revoked'}), 401

        if not current_user == 'admin':
            return jsonify({"message": "You are not authorized"}), 401
        if role:
            # get user with role
            _user_ = database.getuserRole(role)
            if not _user_:
                return jsonify({'message': "no users were found with that role"}), 404
            return jsonify({'users': _user_}), 200

        # get all users
        userget = database.getUsers()
        if not userget:
             return jsonify({'message': "There are no users"}), 404
        return jsonify({'users': userget}), 200    

class LoginView(MethodView):
    """class where user can login"""
    def post(self):
        """user can login"""
        data = request.get_json()
        user_name = data.get('user_name')
        password = data.get('password')
        role = data.get('role')

        loguserval = validate_user_login(user_name = user_name, password=password, role = role)

        if loguserval:
            return loguserval

        access_token = create_access_token(identity=role)
        return jsonify(access_token="{}".format(access_token)), 200

class LogoutView(MethodView):
    @jwt_required
    def delete(self):
        """logout a user"""
        jti = get_raw_jwt()['jti']
        revoked = database.fetch_blacklist(jti)

        if revoked:
            return jsonify({'msg': 'token already revoked'}), 401
        
        jti = get_raw_jwt()['jti']
        obj_blacklist = Blacklist(jti)
        database.insert_blacklist(obj_blacklist)
        return jsonify({"msg": "Successfully logged out"}), 200

class SignupView(MethodView):
    """class where admin can create new users"""
    @jwt_required
    def post(self):
        """create a new user"""
        current_user = get_jwt_identity()
        jti = get_raw_jwt()['jti']
        revoked = database.fetch_blacklist(jti)

        if revoked:
            return jsonify({'msg': 'token already revoked'}), 401

        if not current_user == 'admin':
            return jsonify({"message": "You are not authorized"}), 401
        
        data = request.get_json()
        name = data.get('name')
        user_name = data.get('user_name')
        password = data.get('password')
        role = data.get('role')

        valuser = validate_user_signup(name=name, user_name = user_name, password=password, role = role)

        if valuser:
            return valuser

        obj_users = Users(name, user_name, password, role)
        database.insert_table_users(obj_users)
        return jsonify({"Success": "user has been added"}), 201

class SalesView(MethodView):
    """class to make sale orders"""
    @jwt_required
    def post(self):
        """make a sale order"""
        current_user = get_jwt_identity()
        jti = get_raw_jwt()['jti']
        revoked = database.fetch_blacklist(jti)

        if revoked:
            return jsonify({'msg': 'token already revoked'}), 401

        if not current_user == 'attendant':
            return jsonify({"message": "You are not authorized"}), 401
        
        data = request.get_json()
        user_id = int(data.get('user_id'))
        quantity = int(data.get('quantity'))
        product_id = int(data.get('product_id'))

        # check empty fields
        valsale=validate_sales(user_id=user_id, product_id=product_id, quantity=quantity)

        if valsale:
            return valsale
                
        # get quantity
        getQty = int(database.getQuantity(product_id))

        # get price
        getPrice = int(database.getPrice(product_id))

        #check if quantity is more than quantity in products table
        if quantity > database.getoneProduct(product_id)["quantity"]:
            return jsonify({"message": "this products quantity is less than the quantity you are purchasing"}), 400
                     
        # calculate total
        total = quantity * getPrice

        # new qty
        newqty = getQty - quantity

        # insert into sales table
        obj_sales = Sales(user_id, product_id, quantity, total)
        database.insert_data_sales(obj_sales)

        #update products table
        database.updateProductqty(newqty, product_id)             
        return jsonify({"Success": "sale has been added"}), 201

    @jwt_required
    def get(self, user_id = None):
        """get sale orders"""
        current_user = get_jwt_identity()
        jti = get_raw_jwt()['jti']
        revoked = database.fetch_blacklist(jti)

        if revoked:
            return jsonify({'msg': 'token already revoked'}), 401

        if current_user == 'admin' or current_user == 'attendant':
            if user_id:
                saleorder = database.get_one_sale(user_id)
                if not saleorder:
                    return jsonify({'message': "sale has not been found"}), 404
                return jsonify({'sale': saleorder}), 200
        
        if current_user == 'admin':
            if not user_id:
                saleget = database.getsales()
                if not saleget:
                    return jsonify({'message': "There are no sales"}), 404
                return jsonify({'sales': saleget}), 200

#mapping urls to view classes
app.add_url_rule('/api/v2/products',
                 view_func=ProductsView.as_view('products_view'),
                 methods=["GET", "POST"])
app.add_url_rule('/api/v2/products/<product_id>',
                 view_func=ProductsView.as_view('product_view'),
                 methods=["GET", "PUT", "DELETE"])
app.add_url_rule('/api/v2/sales',
                 view_func=SalesView.as_view('sales_view'),
                 methods=["GET", "POST"])
app.add_url_rule('/api/v2/sales/<user_id>',
                 view_func=SalesView.as_view('sale_view'),
                 methods=["GET"])
app.add_url_rule('/api/v2/users',
                 view_func=UsersView.as_view('users_view'),
                 methods=["GET"])
app.add_url_rule('/api/v2/users/<role>',
                 view_func=UsersView.as_view('user_view'),
                 methods=["GET"])
app.add_url_rule('/api/v2/auth/login',
                 view_func=LoginView.as_view('login_view'),
                 methods=["POST"])
app.add_url_rule('/api/v2/auth/logout',
                 view_func=LogoutView.as_view('logout_view'),
                 methods=["DELETE"])
app.add_url_rule('/api/v2/auth/signup',
                 view_func=SignupView.as_view('signup_view'),
                 methods=["POST"])
