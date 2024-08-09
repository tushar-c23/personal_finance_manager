from fastapi import FastAPI
from personal_finance_manager.routes import auth, user, transaction, category
from personal_finance_manager.database import Base, engine

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return "Hello World"


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}



# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(transaction.router)
app.include_router(category.router)