# 📦 Warehouse CRUD API

A RESTful API built with **FastAPI** for managing a warehouse. It supports full **CRUD** operations on **Products** and **Orders**, product search with filters, order placement with stock validation, and product statistics — all backed by a **PostgreSQL** database via **psycopg2**.

---

## ✨ Features

- ✅ Full CRUD for **Products** (create, read, update, delete)
- ✅ Full CRUD for **Orders** (place, update, delete)
- ✅ **Product search** with multiple optional filters (name, price range, quantity range)
- ✅ **Stock validation** when placing or updating orders
- ✅ **Product statistics** (totals, averages, sorted lists)
- ✅ Automatic **Swagger UI** and **ReDoc** documentation
- ✅ Layered architecture: `controller` → `services` → `repository` → `domain`
- ✅ Data validation with **Pydantic**

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.11+** | Language |
| **FastAPI** | Web framework |
| **Pydantic** | Data validation / schemas |
| **psycopg2** | PostgreSQL driver |
| **PostgreSQL** | Database |
| **Uvicorn** | ASGI server |

---

## 📁 Project Structure

```
APIproject/
├── controller/
│   ├── main_controller.py        # FastAPI app + router registration
│   ├── product_controller.py     # /products endpoints
│   └── orders_controller.py      # /orders endpoints
├── services/
│   ├── product_services.py       # Business logic for products
│   └── order_services.py         # Business logic for orders
├── repository/
│   └── database.py               # All SQL queries (psycopg2)
├── domain/
│   ├── product.py                # Product Pydantic model
│   ├── order.py                  # Order + OrderItem Pydantic models
│   └── search_products.py        # SearchProducts Pydantic model
├── APIuvicorn.txt
├── database_dbeaver.txt
└── README.md
```

---

## 🗄️ Database Schema

The API expects a PostgreSQL database with the following tables:

**`products`**

| Column | Type | Notes |
|--------|------|-------|
| `product_id` | SERIAL / INT | Primary key |
| `product_name` | VARCHAR | |
| `product_description` | VARCHAR | |
| `product_price` | NUMERIC | |
| `product_availability` | INT | Stock quantity |

**`orders`**

| Column | Type | Notes |
|--------|------|-------|
| `order_id` | SERIAL / INT | Primary key |
| `customer_name` | VARCHAR | |

**`order_items`**

| Column | Type | Notes |
|--------|------|-------|
| `order_item_id` | SERIAL / INT | Primary key |
| `order_id` | INT | FK → `orders.order_id` |
| `product_id` | INT | FK → `products.product_id` |
| `quantity` | INT | |

> ⚠️ The database connection is currently configured in `repository/database.py` inside `connect_db()`. Default values: `dbname=students`, `user=postgres`, `password=pass123`, `host=localhost`, `port=5432`. Change them to match your environment.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Alex-Vlandos/CRUD_Warehouse_System.git
cd CRUD_Warehouse_System

```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn psycopg2-binary pydantic
```

### 4. Set up the database

Create the PostgreSQL database and the three tables (`products`, `orders`, `order_items`) as shown in the schema section above.

### 5. Run the server

From the **inner** `APIproject` folder (the one that contains the `controller/` package):

```bash
uvicorn controller.main_controller:app --reload
```

The API will be available at: **http://127.0.0.1:8000**

---

## 📚 API Documentation

Once the server is running:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## 🔗 Endpoints

### 🛒 Products — `/products`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/create-products` | Create one or more products |
| `GET` | `/read-products` | List all products |
| `PATCH` | `/update-product/{product_id}` | Update a product's fields |
| `DELETE` | `/delete-product/{product_id}` | Delete a product |
| `POST` | `/search-products` | Search products with filters |

**POST `/create-products` — Request body (list of products):**

```json
[
  {
    "name": "Laptop",
    "desc": "Dell XPS 15",
    "price": 1499.99,
    "quantity": 10
  },
  {
    "name": "Mouse",
    "desc": "Logitech MX",
    "price": 99.99,
    "quantity": 50
  }
]
```

**Response:**

```json
{
  "message": "2 products created!",
  "products": [
    { "name": "Laptop", "desc": "Dell XPS 15", "price": 1499.99, "quantity": 10 },
    { "name": "Mouse", "desc": "Logitech MX", "price": 99.99, "quantity": 50 }
  ]
}
```

---

**GET `/read-products` — Response:**

```json
{
  "Available products list": [
    {
      "product id": 1,
      "product name": "Laptop",
      "product description": "Dell XPS 15",
      "product price": 1499.99,
      "product quantity": 10
    }
  ]
}
```

---

**PATCH `/update-product/{product_id}` — Request body:**

```json
{
  "name": "Laptop Pro",
  "price": 1699.99
}
```

Only the fields you send will be updated. Fields left as `null` are ignored.

**Response:**

```json
{
  "message": {
    "Product with id : 1 changed, new name : Laptop Pro,new desc : None,new price : 1699.99,new quantity": null
  }
}
```

---

**DELETE `/delete-product/{product_id}` — Response:**

```json
{
  "message": "Product with id : 1 has been deleted successfully!"
}
```

---

**POST `/search-products` — Request body:**

```json
{
  "name": "Lap",
  "min_price": 100,
  "max_price": 2000,
  "min_quantity": 1,
  "max_quantity": 100
}
```

All fields are optional. Only the ones provided are used as filters.

**Response:** same structure as `/read-products`.

---

### 📋 Orders — `/orders`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/place-order` | Place a new order |
| `POST` | `/update-order/{order_id}` | Update an existing order |
| `DELETE` | `/delete-order/{order_id}` | Delete an order |
| `GET` | `/products-statistics` | Get product statistics |

**POST `/place-order` — Request body:**

```json
{
  "customer_name": "Alex Papadopoulos",
  "products_details": [
    { "product_id": 1, "quantity": 2 },
    { "product_id": 2, "quantity": 1 }
  ]
}
```

**Response (success):**

```json
{
  "products ": ["product with id : 1", "quantity ordered : 2", "product with id : 2", "quantity ordered : 1"],
  "Order details, order id ": 5
}
```

**Response (validation error):**

```json
{
  "Error ": "Order could not be placed",
  "Reasons ": "['You chose product with id : 1 but you chose quantity = 100,whereas product availability is 10!']"
}
```

**Validation rules applied by the service:**
- Customer name is required.
- Product list must not be empty.
- Each item must have a `product_id` and `quantity`.
- The same product cannot appear twice in one order.
- Quantity must be > 0 and ≤ product availability.

---

**POST `/update-order/{order_id}` — Request body:**

```json
{
  "customer_name": "Alex P.",
  "products_details": [
    { "product_id": 1, "quantity": 3 }
  ]
}
```

- If the `product_id` already exists in the order → the line is updated.
- If it doesn't exist → a new item is inserted via `place_order`.

---

**DELETE `/delete-order/{order_id}` — Response:**

```json
{ "message": "Order with id 5 deleted successfully!" }
```

Or, if the order does not exist:

```json
{ "error": "There is no such order with id 5 anymore!" }
```

---

**GET `/products-statistics` — Response:**

```json
{
  "total_amount_of_different_products": 3,
  "total_stock": 60,
  "average_total_price": 899.99,
  "products_descending_price": [ ... ],
  "products_ascending_price": [ ... ]
}
```

---

## 🧪 Testing with Postman

1. Open Postman.
2. Create a new collection called **Warehouse API**.
3. Set a collection variable `base_url = http://localhost:8000`.
4. Add requests using the endpoints above (e.g. `{{base_url}}/create-products`).
5. Make sure the PostgreSQL database and tables exist before sending requests.

---

## 📌 Example with curl

```bash
# Create products
curl -X POST http://localhost:8000/create-products \
  -H "Content-Type: application/json" \
  -d '[{"name":"Laptop","desc":"Dell XPS 15","price":1499.99,"quantity":10}]'

# Read products
curl http://localhost:8000/read-products

# Search products
curl -X POST http://localhost:8000/search-products \
  -H "Content-Type: application/json" \
  -d '{"min_price": 100, "max_price": 2000}'

# Place an order
curl -X POST http://localhost:8000/place-order \
  -H "Content-Type: application/json" \
  -d '{"customer_name":"Alex","products_details":[{"product_id":1,"quantity":2}]}'

# Delete an order
curl -X DELETE http://localhost:8000/delete-order/5
```

---

## ⚠️ Notes

- All database queries are done with **raw SQL** via `psycopg2` — there is no ORM.
- The connection settings are hardcoded inside `repository/database.py`. For production, move them to environment variables.
- The API uses `PATCH` for product updates (partial update) and `POST` for order updates (because the order update may insert new items).

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

Distributed under the **MIT** License.

---

## 👤 Author

**[Alexandros Vlandos]**
- GitHub: [@your-username](https://github.com/Alex-Vlandos)
- Email: [alexvla@windowslive.com]
