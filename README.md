# Vendor Management System

This project is a Vendor Management System developed using Django and Django REST Framework.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/vivekrathod5/vendor-management-system.git
cd vendor-management-system
```

### 2. Set Up Virtual Environment

```bash
# Install virtualenv if you haven't already
pip install virtualenv

# Create a virtual environment
virtualenv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Make sure to configure your database settings in `vendor-management-system/settings.py`. Then, run the following commands:

```bash
python manage.py makemigrations
python manage.py migrate
```


### 5. Run the Management Cammand
```bash
# To create a sytem user
python manage.py seed --mode=refresh

# To clear/delete a sytem user
python manage.py seed --mode=clear
```


### 5. Run the Development Server

```bash
python manage.py runserver
```

You should now be able to access the API at `http://127.0.0.1:8000/`.





## Swagger API Documentation
  - `http://127.0.0.1:8000/swagger/`: All endpoints



## Authentication

This API uses token-based authentication. You need to obtain an authentication token by sending a POST request to `/login` with your system email and password. Use this token in the Authorization header (`Bearer token`) for accessing protected endpoints.



## API Endpoints

- **Admin**
  - `POST /login`: Admin login
  - `GET /logout`: Admin logout


- **Vendors**
  - `GET /api/vendors`: List all vendors
  - `POST /api/vendors`: Create a new vendor
  - `GET /api/vendors/{vendor_id}`: Retrieve a specific vendor
  - `PUT /api/vendors/{vendor_id}`: Update a vendor
  - `DELETE /api/vendors/{vendor_id}`: Delete a vendor

- **Purchase Orders**
  - `GET /api/purchase_orders`: List all purchase orders
  - `POST /api/purchase_orders`: Create a new purchase order
  - `GET /api/purchase_orders/{po_id}`: Retrieve a specific purchase order
  - `PUT /api/purchase_orders/{po_id}`: Update a purchase order
  - `DELETE /api/purchase_orders/{po_id}`: Delete a purchase order

- **Performance Metrics**
  - `GET /api/vendors/{vendor_id}/performance`: Vendor Performance


