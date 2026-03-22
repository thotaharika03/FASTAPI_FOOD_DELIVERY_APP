from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# ---------------- DATA ----------------

menu = [
    {"id": 1, "name": "Margherita Pizza", "price": 199, "category": "Pizza", "available": True},
    {"id": 2, "name": "Veg Burger", "price": 99, "category": "Burger", "available": True},
    {"id": 3, "name": "Pasta Alfredo", "price": 249, "category": "Pasta", "available": False},
    {"id": 4, "name": "French Fries", "price": 79, "category": "Snacks", "available": True}
]

cart = []
orders = []

# ---------------- HELPERS ----------------

def find_item(item_id):
    for item in menu:
        if item["id"] == item_id:
            return item
    return None

def get_cart_total():
    total = 0
    for item in cart:
        total += item["subtotal"]
    return total

# ---------------- MODELS ----------------

class MenuItem(BaseModel):
    name: str = Field(..., min_length=3)
    price: int = Field(..., gt=0)
    category: str
    available: bool

class Order(BaseModel):
    customer_name: str = Field(..., min_length=3)
    address: str = Field(..., min_length=10)

# ---------------- DAY 1 ----------------

@app.get("/")
def home():
    return {"message": "Welcome to Food Delivery API "}

@app.get("/menu")
def get_menu():
    return {"items": menu, "total": len(menu)}

@app.get("/menu/available")
def available_items():
    result = [item for item in menu if item["available"]]
    return {"items": result, "count": len(result)}

@app.get("/menu/summary")
def summary():
    total = len(menu)
    available = len([i for i in menu if i["available"]])
    return {
        "total_items": total,
        "available": available,
        "unavailable": total - available
    }

# ---------------- FILTER ----------------

@app.get("/menu/filter")
def filter_menu(category: Optional[str] = None, available: Optional[bool] = None):
    result = menu

    if category is not None:
        result = [i for i in result if i["category"].lower() == category.lower()]

    if available is not None:
        result = [i for i in result if i["available"] == available]

    return {"items": result, "count": len(result)}

# ---------------- CRUD ----------------

@app.post("/menu", status_code=201)
def add_item(item: MenuItem):
    for i in menu:
        if i["name"].lower() == item.name.lower():
            raise HTTPException(status_code=400, detail="Item already exists")

    new_item = item.dict()
    new_item["id"] = len(menu) + 1
    menu.append(new_item)

    return {"message": "Item added", "item": new_item}

@app.put("/menu/{item_id}")
def update_item(item_id: int, name: Optional[str] = None, price: Optional[int] = None):
    item = find_item(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if name is not None:
        item["name"] = name

    if price is not None:
        item["price"] = price

    return {"message": "Item updated", "item": item}

@app.delete("/menu/{item_id}")
def delete_item(item_id: int):
    item = find_item(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item["available"]:
        raise HTTPException(status_code=400, detail="Cannot delete available item")

    menu.remove(item)
    return {"message": "Item deleted"}

# ---------------- CART WORKFLOW ----------------

@app.post("/cart/add")
def add_to_cart(item_id: int, quantity: int = 1):
    item = find_item(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if not item["available"]:
        raise HTTPException(status_code=400, detail="Item out of stock")

    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            c["subtotal"] = c["quantity"] * c["price"]
            return {"message": "Cart updated", "item": c}

    new_item = {
        "item_id": item_id,
        "name": item["name"],
        "price": item["price"],
        "quantity": quantity,
        "subtotal": item["price"] * quantity
    }

    cart.append(new_item)
    return {"message": "Added to cart", "item": new_item}

@app.get("/cart")
def view_cart():
    if not cart:
        return {"message": "Cart is empty"}

    return {
        "items": cart,
        "grand_total": get_cart_total()
    }

@app.delete("/cart/{item_id}")
def remove_from_cart(item_id: int):
    for c in cart:
        if c["item_id"] == item_id:
            cart.remove(c)
            return {"message": "Item removed from cart"}

    raise HTTPException(status_code=404, detail="Item not in cart")

@app.post("/cart/checkout")
def checkout(order: Order):
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    for c in cart:
        orders.append({
            "order_id": len(orders) + 1,
            "customer": order.customer_name,
            "product": c["name"],
            "quantity": c["quantity"],
            "total": c["subtotal"]
        })

    cart.clear()
    return {"message": "Order placed", "orders": orders}

@app.get("/orders")
def get_orders():
    return {"orders": orders, "total_orders": len(orders)}

# ---------------- SEARCH ----------------

@app.get("/menu/search")
def search(keyword: str):
    result = [i for i in menu if keyword.lower() in i["name"].lower()]

    if not result:
        return {"message": f"No items found for: {keyword}"}

    return {"items": result, "total_found": len(result)}

# ---------------- SORT ----------------

@app.get("/menu/sort")
def sort(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name"]:
        raise HTTPException(status_code=400, detail="sort_by must be 'price' or 'name'")

    reverse = True if order == "desc" else False
    sorted_items = sorted(menu, key=lambda x: x[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "items": sorted_items
    }

# ---------------- PAGINATION ----------------

@app.get("/menu/page")
def paginate(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    end = start + limit

    total_pages = (len(menu) + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "items": menu[start:end]
    }

# ---------------- COMBINED ----------------

@app.get("/menu/browse")
def browse(
    keyword: Optional[str] = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = menu

    if keyword:
        result = [i for i in result if keyword.lower() in i["name"].lower()]

    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    start = (page - 1) * limit
    end = start + limit

    total_pages = (len(result) + limit - 1) // limit

    return {
        "total_found": len(result),
        "page": page,
        "total_pages": total_pages,
        "items": result[start:end]
    }

# ---------------- LAST ROUTE ----------------

@app.get("/menu/{item_id}")
def get_item(item_id: int):
    item = find_item(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item
