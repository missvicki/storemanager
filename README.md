## Store Manager [![Build Status](https://travis-ci.org/missvicki/storemanager.svg?branch=feature)](https://travis-ci.org/missvicki/storemanager) [![Coverage Status](https://coveralls.io/repos/github/missvicki/storemanager/badge.svg?branch=feature)](https://coveralls.io/github/missvicki/storemanager?branch=feature) [![Maintainability](https://api.codeclimate.com/v1/badges/5ede6e059132e2e43860/maintainability)](https://codeclimate.com/github/missvicki/storemanager/maintainability)

Store Manager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store.    

## Getting Started

For installation of this project:  `$ git clone 'https://github.com/missvicki/storemanager.git`

## Prerequisites

* Create a Virtual Environment e.g.: `$ virtualenv storemanager`
* Activate the environment: 
    * For Windows: `$c:/ .\storemanager\Scripts\activate`
    * For Linux and Mac: `$ source storemanager/bin/activate`
* Install project dependencies e.g. flask: `$ pip install -r requirements.txt`

## Features

* Admin: 
    * can create a product
    * can get all products
    * can get a specific product 
    * can delete a product
    * can modify a single product

    * can get all sale orders
    * can get a single sale made by attendant

    * can create new users
    * can login
    * can view all users
    * can view users under a role


* Attendant:
    * can login

    * can create a sale order of a product
    * can get a sales they made

    * can get all products 
    * can get a specific product
    * can create a product

## gh-pages link 
    
    `$ https://missvicki.github.io/storemanager/UI/templates`

## Login Credentials

| User Role | Username | Password |
| ----------- | -------- | --------- |
| Store Owner | admin | admin |
| Store Attendant | attendant | attendant |

## Heroku Endpoints

| REQUEST | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- |
| POST | /api/v2/auth/signup |Create a New User|
| POST | /api/v2/auth/login |Login a User|
| POST | /api/v2/products | Adds a new product |
| POST | /api/v2/sales | Creates a sales order |
| GET | /api/v2/products | Returns all products|
| GET | /api/v2/products/product_id | Fetches a single product |
| GET | /api/v2/sales | Fetches all sales |
| GET | /api/v2/users | Fetches all users |
| GET | /api/v2/sales/user_id | Fetches a single sale made by a user |
| GET | /api/v2/users/role | Fetches all users belonging to a role |
| DELETE | /api/v2/products/product_id | Deletes a product |
| PUT | /api/v2/products/product_id | Modifies a single product |

## Testing the app

`$nosetests --with-cov --cov  tests/`
  
## Language

**Python**: 3.6.5

## Run the app

`$ python run.py`

## Authors

* **Victor Nomwesigwa**

## Acknowledgments

* Andela
