from fastapi import FastAPI

from app.api.routers import receipt, store, customer

app = FastAPI()

app.include_router(
    receipt.router,
    prefix='/api/receipt',
    tags=['receipt']
)
app.include_router(
    store.router,
    prefix='/api/store',
    tags=['store']
)
app.include_router(
    customer.router,
    prefix='/api/customer',
    tags=['customer']
)
