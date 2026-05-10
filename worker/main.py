# Llama 추론 프로그램 -> CPU 작업, 답변 생성기
import json
import redis
from llama_cpp import Llama
# 비동기 프로그래밍을 적용해야 할까요?
# Yes or No

# I/O 작업에 효과적 -> "대기시간에 다른거 하자"

# redis = (비유) 엄청 빠른 초소형 데이터베이스(key: value)
redis_client = redis.from_url("redis://redis:6379", decode_responses=True)

llm = Llama(
    model_path="./models/Llama-3.2-1B-Instruct-04_K_M.gguf",
    n_ctx=4096,
    n_threads=2,
    verbose=False,
    chat_format="llama-3",
)

SYSTEM_PROMPT = (
    "You are a concise assistant. "
    "Always reply in the same language as the user's input. "
    "Do not change the language. "
    "Do not mix languages."
)


def create_response(question: str):
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        max_tokens=256,
        temperature=0.7,
    )
    return response["choices"][0]["message"]["content"]


def run():
    while True:
        # [1] Job을 deque
        # brpop: 작업이 들어올 때까지 기다렸다가 받고 종료
        _, job_data = redis_client.brpop("inference_queue")
        job: dict = json.loads(job_data)

        # [2] 추론
        answer = create_response(question=job["question"])

        # [3] 결과를 API 
        channel = f"result:{job["id"]}"
        redis_client.publish(channel, answer)


# python main.py를 직접 실행되었을 때만, run()을 호출
if __name__ == "__main__":
    run()
