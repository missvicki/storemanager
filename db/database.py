"""Database models"""

queries = (
    """
        CREATE TABLE IF NOT EXISTS products (
            product_id SERIAL PRIMARY KEY, 
            product_name VARCHAR(50) UNIQUE NOT NULL, 
            category VARCHAR(50) NOT NULL, 
            unit_price integer NOT NULL, 
            quantity integer NOT NULL, 
            measure VARCHAR(12) NOT NULL,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            delete_status BOOLEAN DEFAULT FALSE)
    """,
    """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY, 
            name VARCHAR(50) NOT NULL,
            user_name VARCHAR(12) NOT NULL UNIQUE, 
            password VARCHAR(12) UNIQUE NOT NULL, 
            role VARCHAR(15) NOT NULL,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            delete_status BOOLEAN DEFAULT FALSE)
    """,
    """
        CREATE TABLE IF NOT EXISTS sales (
            sale_id SERIAL PRIMARY KEY,  
            user_id integer NOT NULL,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            delete_status BOOLEAN DEFAULT FALSE,
            CONSTRAINT userid_foreign FOREIGN KEY (user_id) 
            REFERENCES users(user_id) 
             ON UPDATE CASCADE)
    """,
    """
        CREATE TABLE IF NOT EXISTS sales_has_products(
            sale_id integer NOT NULL,
            product_id integer NOT NULL,
            quantity integer NOT NULL,
            total integer NOT NULL,
            delete_status BOOLEAN DEFAULT FALSE,
            CONSTRAINT sale_idforeignkey FOREIGN KEY (sale_id)
            REFERENCES sales(sale_id)
                ON UPDATE CASCADE,
            CONSTRAINT prodidfk FOREIGN KEY (product_id)
            REFERENCES products(product_id)
                ON UPDATE CASCADE
            )
        """,
        """
            CREATE TABLE IF NOT EXISTS login(
                user_name VARCHAR(12) NOT NULL,
                password VARCHAR(12) NOT NULL,
                role VARCHAR(15) NOT NULL,
                date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        """
            INSERT INTO users(name, user_name, password, role)\
            VALUES('Vicki', 'vickib', 'vibel', 'admin')
        """
)
from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import datetime
from api.__init__ import app

class DatabaseConnection:
    """Connect to the database"""
    def __init__(self):
        try:
            self.conn = psycopg2.connect(host="ec2-54-83-27-162.compute-1.amazonaws.com", 
                                            database="dcojjie21dvmis", 
                                            user="sejawvmmzwabhv", 
                                            port = "5432",
                                            password="26c76331cf6695b3226de7db2d6405f757329228c9e84b858a29847e030d6044")
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.conn.autocommit = True
            for query in queries:
                self.cur.execute(query)
        except psycopg2.DatabaseError as anything:
            print (anything)
        
    def insert_data_products(self, data):
        """inserts values into table products"""

        try:
            self.cur.execute(
                """
                INSERT INTO products(product_name, category, unit_price, quantity, measure) \
                VALUES('{}', '{}', {}, {}, '{}')""".format(data.product_name, data.category, 
                data.unit_price, data.quantity, data.measure)
            )
            products = self.cur.execute.fetchall()
            return products
        except:
            return False

    def check_product_exists_name(self, product_name):
        """check if product exists"""

        try:
            self.cur.execute(
                "SELECT * FROM products WHERE product_name = '{}' AND delete_status = FALSE" .format(product_name)
            )
            return self.cur.fetchone()
        except:
            return False

    def getProducts(self):
        """get all products"""

        try:
            self.cur.execute(
                "SELECT * FROM products WHERE delete_status = FALSE"
            )
            _products = self.cur.fetchall()
            return _products

        except:
            return False

    def getoneProduct(self, _pid):
        """get one product"""

        try:
            self.cur.execute(
                "SELECT * FROM products WHERE product_id = %s AND delete_status = FALSE", [_pid]
            )
            _products = self.cur.fetchone()
            return _products

        except:
            return False

    def deloneProduct(self, _pid):
        """delete one product"""
        try:
            self.cur.execute(
                # "DELETE FROM products WHERE product_id = %s", [_pid]
                "UPDATE products SET delete_status=TRUE , date_modified =CURRENT_TIMESTAMP WHERE product_id = {}".format(_pid
                )
            )
        except:
            return False

    def check_product_exists_id(self, product_id):
        """check if product exists"""

        try:
            self.cur.execute(
                "SELECT * FROM products WHERE product_id = %s AND delete_status= FALSE", [product_id]) 
            return self.cur.fetchone()

        except:
            return False

    def modify_product(self, category, unit_price, quantity, measure,product_id):
        """modify product"""
        try:
            self.cur.execute(
                "UPDATE products SET category='{}', \
                unit_price={}, quantity={}, measure = '{}', date_modified=CURRENT_TIMESTAMP\
                WHERE product_id = {} AND delete_status = FALSE"
                .format(category, unit_price, quantity, measure, product_id)
            )

        except:
            return False
    
    def insert_table_users(self, record):
        """add data to table users"""

        try:
            self.cur.execute(
                """
                INSERT INTO users(name, user_name, password, role) \
                VALUES('{}', '{}', '{}', '{}')
                """.format(record.name, record.user_name, record.password, record.role)
            )
        
        except:
            return False

    def default_admin(self):
        """inserts default admin"""

        try:
            self.cur.execute(
                """
                INSERT INTO users(name, user_name, password, role)\
                VALUES('Vicki', 'vickib', 'vibel', 'admin');
                """
            )
        
        except:
            return False

    def insert_table_login(self, record):
        """add data to table login"""

        try:
            self.cur.execute(
                """
                INSERT INTO login(user_name, password, role) \
                VALUES('{}', '{}', '{}')
                """.format(record.user_name, record.password, record.role)
            )
        
        except:
            return False
    
    def getuserRole(self, role):
        try:
            self.cur.execute("SELECT * FROM users WHERE role=%s AND delete_status= FALSE", (role,))
            userrole = self.cur.fetchall()
            return userrole

        except:
            return False

    def getUsers(self):
        """get all users"""
        try:
            self.cur.execute(
                "SELECT * FROM users WHERE delete_status= FALSE"
            )
            _users = self.cur.fetchall()
            return _users

        except:
            return False

    def check_user_exists(self, user_name, password, role):
        """check if user exists"""

        try:
            self.cur.execute(
                "SELECT * FROM users WHERE user_name = '{}' AND password = '{}' AND role = '{}' AND delete_status= FALSE" .format(user_name, password, role)
            )
            return self.cur.fetchone()
        
        except:
            return False

    def getoneUser(self, _uid):
        """get one user"""

        try:
            self.cur.execute(
                "SELECT * FROM users WHERE user_id = %s AND delete_status = FALSE AND role = attendant", [_uid]
            )
            _users = self.cur.fetchone()
            return _users

        except:
            return False

    def deloneuser(self, _uid):
        """delete one user"""

        try:
            self.cur.execute(
                # "DELETE FROM users WHERE user_id = %s", [_uid]
                "UPDATE users SET delete_status=TRUE, date_modified= CURRENT_TIMESTAMP WHERE user_id = {}".format(_uid)
            )
        except:
            return False

    def check_user_exists_id(self, user_id):
        """check if user exists"""

        try:
            self.cur.execute(
                "SELECT * FROM users WHERE user_id = %s AND delete_status= FALSE", [user_id]) 
            return self.cur.fetchone()

        except:
            return False

    def insert_data_sales(self, data):
        """insert data into sales table"""

        try:
            self.cur.execute("INSERT INTO sales(user_id) VALUES({}) RETURNING sale_id".format(data.user_id)
            )
            return self.cur.fetchone()[0]
        
        except:
            return False

    def insert_data_sales_has_products(self, data):
        """insert data into salesproducts table"""

        try:
            self.cur.execute(
                "INSERT INTO sales_has_products(sale_id, product_id, quantity, total) \
                VALUES({}, {}, {}, {})\
                ".format(data.sale_id, data.product_id, data.quantity, data.total)
            )
        except:
            return False
        
    def getsales(self):
        """get one sale"""

        try:
            self.cur.execute(
                "SELECT * FROM sales WHERE delete_status = FALSE"
            )
            _sale = self.cur.fetchall()
            return _sale
        except:
            return False

    def getQuantity(self, id_):
        """get qty"""

        try:
            self.cur.execute(
                "SELECT quantity FROM products WHERE product_id = %s AND delete_status= FALSE", [id_]
            )
            return self.cur.fetchone()[0]
        
        except:
            return False

    def getPrice(self, id_):
        """get price"""

        try:
            self.cur.execute(
                "SELECT unit_price FROM products WHERE product_id = %s AND delete_status= FALSE", [id_]
            )
            return self.cur.fetchone()[0]
        
        except:
            return False

    def updateProductqty(self, qty, pdtid):
        """update pdt qty"""

        try:
            self.cur.execute(
                "UPDATE products SET quantity={}, date_modified=CURRENT_TIMESTAMP WHERE product_id = {} \
                AND delete_status=False".format(qty, pdtid)
            )
        
        except:
            return False
    
    def get_one_sale(self, user_id):
        try:
            self.cur.execute(
                "SELECT * FROM sales WHERE user_id = %s AND delete_status = FALSE", [user_id] 
            )
            _sale = self.cur.fetchall()
            return _sale
        except:
            return False
    
    def drop_tables(self):
        """drop tables if exist"""
        self.cur.execute(
            "DROP TABLE IF EXISTS products, users, sales, sales_has_products, login CASCADE"
        )
