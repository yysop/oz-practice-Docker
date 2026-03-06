# 0305

from fastapi import FastAPI
from sqlalchemy import text

from database import SessionFactory # api.database 로 자동 수정된 거 삭제해줌



app = FastAPI()

# root_handler 추가
@app.get("/")
async def root_handler():
    return {"ping": "pong247"}

@app.get("/users")
async def get_users_handler():
    with SessionFactory() as session:
        result = session.execute(
            text("SELECT * FROM user;")
        ).mappings().all()


    return {"result": result}