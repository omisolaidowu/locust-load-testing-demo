from fastapi import FastAPI, APIRouter

app = FastAPI(title="Locust Server Example")

# Item router
item_router = APIRouter(prefix="/items", tags=["items"])
# User router
user_router = APIRouter(prefix="/users", tags=["users"])


# Sample endpoints for items
@item_router.get("/")
async def get_items():
    return [{"id": 1, "name": "Item A"}, {"id": 2, "name": "Item B"}]


@item_router.get("/{item_id}")
async def get_item(item_id: int):
    return {"id": item_id, "name": f"Item {item_id}"}


# Sample endpoints for users
@user_router.get("/")
async def get_users():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]


@user_router.get("/{user_id}")
async def get_user(user_id: int):
    return {"id": user_id, "name": f"User {user_id}"}


# Include routers in the main app
app.include_router(user_router)
app.include_router(item_router)


# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Locust Server Example"}
