import json
import uuid

import redis import asyncio as aredis
from fastapi import FastAPI, Body, Query, Path


# 답변 생성을 요청하면, 대기 발생
# 대기하는 동안, 다른 일(HTTP 요청) 처리

# responses
redis_client = aredis.from_url("redis://redis:6379", decode_responses=True)


app = FastAPI()

# [ 쿼리 파라미터(QueryParameter) ]
# GET google.com/search?q=python -> 새로운 데이터를 만들어내거나, 데이터 변경 X

# GET -> 새로운 데이터를 만들어내거나, 데이터 변경 X
# POST -> 새로운 데이터를 생성

# [1] 클라이언트에서 질문(question)을 요청한다.
@app.post("/chats")
async def chat_handler(
    # RequestBody
    # 3-1) 
    # UserSignUpRequest = Body(...)
    # 3-2)
    question: str = Body(..., embed=True),
    
    # Query
    # question: str = Query(...),

    # Path
    # question: str = Path(...),
):
    # [2] 결과 채널을 구독
    job_id = str(uuid.uuid4())  # 작업을 식별할 수 있는 랜덤 식별자 발급
    channel = f"result:{job_id}"

    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel)

    # [3] 답변 생성 작업 Enqueue
    job = {"id": job_id, "question": question}
    await redis_client.lpush("inference_queue", json.dumps(job))

    # [4] 답변 생성 결과를 돌려받기
    result = None
    async for message in pubsub.listen():
        if message["type"] == "message":
            result = message["data"]
            break
        
    return {"result": result}
