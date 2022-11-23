# Online Store API

## Installation

#### Install Python 3:

- Please checkout https://realpython.com/installing-python/

#### Create virtual environment:

- Go to you project directory, then

```shell
> py -3 -m venv .venv
```

```shell
> .\.venv\Scripts\Activate.ps1
```

#### Install requirements:

```shell
> pip install -r requirements.txt
```

#### Loading fixtures:

```shell
> python manage.py loaddata additional_materials/fixtures/dump.json
```
- [Online Store API fixtures](https://github.com/YordanPetrovDS/OnlineStoreAPI/tree/main/additional_materials/fixtures)

## Running API Server

```shell
> python manage.py runserver
```

## Thunder Client Collection

![TC Collection](additional_materials/screenshots/TC_collection.JPG)

- [Online Store API Collection](https://github.com/YordanPetrovDS/OnlineStoreAPI/tree/main/additional_materials/thunder_client)

## Sample Screenshots

- POST | Product
  ![Create New Product](additional_materials/screenshots/thunder_client_POST_Product.JPG)
- PUT | Product
  ![Update Existing Product](additional_materials/screenshots/thunder_client_PUT_Product.JPG)
- GET | Product
  ![List | Product](additional_materials/screenshots/thunder_client_GET_Product.JPG)
- POST | Order
  ![Create New Order](additional_materials/screenshots/thunder_client_POST_Order.JPG)
- GET | Order
  ![List Product](additional_materials/screenshots/thunder_client_GET_Order.JPG)
- POST | Order Product
  ![Create New Product](additional_materials/screenshots/thunder_client_POST_Order_Product.JPG)
- GET | Stats
  ![Stats Admin](additional_materials/screenshots/thunder_client_GET_Stats.JPG)

## Admin Panel

- http://127.0.0.1:8000/admin

Basic CRUD operations can also be done from the admin interface of Django and Django Rest Framework.

![django-admin](additional_materials/screenshots/django_admin.JPG)

- http://127.0.0.1:8000/api/auth/accounts/register/
- http://127.0.0.1:8000/api/auth/accounts/login/
- http://127.0.0.1:8000/api/auth/accounts/logout/
- http://127.0.0.1:8000/api/product/
- http://127.0.0.1:8000/api/order/
- http://127.0.0.1:8000/api/order/stats/
- http://127.0.0.1:8000/api/order-product/

![drf-admin](additional_materials/screenshots/drf_admin.JPG)
