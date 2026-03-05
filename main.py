# 0305

from fastapi import FastAPI
from sqlalchemy import text

from database import SessionFactory

app = FastAPI()

@app.get("/users")
async def get_users_handler():
    with SessionFactory() as session:
        result = session.execute(
            text("SELECT * FROM user;")
        ).mappings().all()


    return {"result": result}