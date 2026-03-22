🍕 FastAPI Food Delivery Backend
A backend application built using FastAPI that simulates a real-world food delivery system. This project was developed as part of my FastAPI internship to demonstrate API design, backend logic, and workflow handling.

🚀 Project Overview
This application provides REST APIs to manage food items, handle cart operations, process orders, and perform advanced operations like search, sorting, and pagination.

All endpoints are tested and verified using Swagger UI.

✨ Features
📋 Menu Management
View all menu items
Get item details by ID
Add new items with validation
Update existing items
Delete items with business rules
🛒 Cart & Order Workflow
Add items to cart
View cart details
Calculate total price
Checkout and place orders
Store and retrieve order history
🔍 Advanced Functionality
Search items (case-insensitive)
Sort items by price or name
Pagination for large data
Combined endpoint (search + sort + pagination)
🛠️ Tech Stack
🐍 Python
⚡ FastAPI
📦 Pydantic
🚀 Uvicorn
▶️ How to Run
1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Run the Server
uvicorn main:app --reload

3️⃣ Open Swagger UI
http://127.0.0.1:8000/docs

📸 API Testing
All endpoints are tested using Swagger UI.
Screenshots of all API responses are included in the screenshots/ folder.

📌 Key Highlights
Clean API structure
Proper input validation using Pydantic
Full CRUD implementation
Multi-step workflow (Cart → Checkout → Orders)
Advanced APIs with search, sorting, and pagination
⚠️ Notes
Data is stored in-memory (resets when server restarts)
This project focuses on backend logic and API design
📎 Repository Structure
fastapi-food-delivery-app/ │ ├── main.py ├── README.md ├── requirements.txt └── screenshots/

🎯 Conclusion
This project demonstrates practical backend development using FastAPI, covering all essential concepts from basic APIs to advanced data handling.

