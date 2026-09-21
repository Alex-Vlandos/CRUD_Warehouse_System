# 📦 Warehouse CRUD API

Ένα RESTful API για διαχείριση αποθήκης, φτιαγμένο με **FastAPI**. Υποστηρίζει πλήρεις λειτουργίες **CRUD** (Create, Read, Update, Delete) για **Products** και **Orders**, με χρήση Docker και Postman.

---

## 🚀 Features

- ✅ Πλήρες CRUD για **Products** (δημιουργία, ανάκτηση, ενημέρωση, διαγραφή)
- ✅ Πλήρες CRUD για **Orders** (δημιουργία, ανάκτηση, ενημέρωση, διαγραφή)
- ✅ Data validation με **Pydantic**
- ✅ Async endpoints με **FastAPI**
- ✅ Βάση δεδομένων **PostgreSQL**
- ✅ Docker
- ✅ Συλλογή **Postman** για δοκιμή όλων των endpoints
- ✅ Δομημένη αρχιτεκτονική (controllers / repository / domain / services)

---

## 🛠️ Tech Stack

| Τεχνολογία | Χρήση |
|------------|-------|
| **Python 3.11+** | Γλώσσα |
| **FastAPI** | Web framework |
| **Pydantic** | Data validation |
| **PostgreSQL** | Βάση δεδομένων |
| **Docker** | Containerization |
| **Uvicorn** | ASGI server |
| **Postman** | API testing |

---

## 📁 Δομή Project

```
APIproject/
├── controller/
│   ├── main_controller.py
│   ├── product_controller.py
│   └── orders_controller.py
├── domain/
│   ├── search_products.py
│   ├── product.py
│   └── order.py
├── services/
│   ├── product_services.py
│   └── order_services.py
├── repository/
│   └── database.py
├── .venv
├── .gitignore
├── APIuvicorn.txt
├── database_dbeaver.txt
└── README.md
```

---

## ⚙️ Εγκατάσταση & Εκτέλεση

### 🔹 Τοπική εκτέλεση (χωρίς Docker)

**1. Clone το repository:**

```bash
git clone https://github.com/[το-username-σας]/[όνομα-repo].git
cd [όνομα-repo]
```

**2. Δημιουργία virtual environment:**

```bash
python -m venv .venv
```

Ενεργοποίηση:

- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

**3. Εγκατάσταση dependencies:**

```bash
pip install -r requirements.txt
```

**4. Ρύθμιση μεταβλητών περιβάλλοντος:**

Αντιγράψτε το `.env.example` σε `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/warehouse
```

**5. Εκκίνηση του server:**

```bash
uvicorn controller.main_controller:app --reload
```

Το API είναι διαθέσιμο στο: **http://127.0.0.1:8000**

---

### 🐳 Εκτέλεση με Docker

```bash
docker-compose up --build
```

Ή μεμονωμένα:

```bash
docker build -t warehouse-api .
docker run -p 8000:8000 --env-file .env warehouse-api
```

Για τερματισμό:

```bash
docker-compose down
```

---

## 📚 API Documentation

Μετά την εκκίνηση του server:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## 🔗 Endpoints

### 🛒 Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/products` | Λίστα όλων των προϊόντων |
| `GET` | `/products/{id}` | Ανάκτηση προϊόντος με ID |
| `POST` | `/products` | Δημιουργία νέου προϊόντος |
| `PUT` | `/products/{id}` | Ενημέρωση προϊόντος |
| `DELETE` | `/products/{id}` | Διαγραφή προϊόντος |

**POST /products — Request body:**

```json
{
  "name": "Laptop",
  "description": "Dell XPS 15",
  "price": 1499.99,
  "quantity": 10
}
```

**Response:**

```json
{
  "id": 1,
  "name": "Laptop",
  "description": "Dell XPS 15",
  "price": 1499.99,
  "quantity": 10,
  "created_at": "2026-01-15T10:30:00"
}
```

### 📋 Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/orders` | Λίστα όλων των παραγγελιών |
| `GET` | `/orders/{id}` | Ανάκτηση παραγγελίας με ID |
| `POST` | `/orders` | Δημιουργία νέας παραγγελίας |
| `PUT` | `/orders/{id}` | Ενημέρωση παραγγελίας |
| `DELETE` | `/orders/{id}` | Διαγραφή παραγγελίας |

**POST /orders — Request body:**

```json
{
  "product_id": 1,
  "quantity": 2,
  "customer_name": "Alex Papadopoulos"
}
```

**Response:**

```json
{
  "id": 1,
  "product_id": 1,
  "quantity": 2,
  "customer_name": "Alex Papadopoulos",
  "status": "pending",
  "created_at": "2026-01-15T10:35:00"
}
```

---

## 🧪 Δοκιμή με Postman

Στο repository υπάρχει το `postman_collection.json`.

1. Ανοίξτε το **Postman**
2. **Import** → επιλέξτε το `postman_collection.json`
3. Ρυθμίστε τη μεταβλητή `base_url` σε `http://localhost:8000`
4. Εκτελέστε τα requests

---

## 🐳 Docker Compose

```yaml
version: "3.9"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: warehouse
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 📌 Παράδειγμα με curl

```bash
# Δημιουργία προϊόντος
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 1499.99, "quantity": 10}'

# Λίστα προϊόντων
curl http://localhost:8000/products

# Δημιουργία παραγγελίας
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2, "customer_name": "Alex"}'
```

---

## 🤝 Συνεισφορά

Pull requests είναι ευπρόσδεκτα. Για μεγάλες αλλαγές, ανοίξτε πρώτα ένα issue για να συζητήσουμε τι θα θέλατε να αλλάξετε.


---

## 👤 Author

**[Το όνομά σας]**
- GitHub: [@το-username-σας](https://github.com/Alex-Vlandos)
- Email: [alexvla@windowslive.com]

---

## ⭐ Αν σας φάνηκε χρήσιμο

Αφήστε ένα ⭐ στο repository!
