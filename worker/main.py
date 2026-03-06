# Llama 추론 프로그램 -> CPU 작업

# 비동기 프로그래밍을 적용해야 할까? No
# -> I/O 작업에 효과적 -> "대기시간에 다른 거 하자"
import redis 

redis_client = redis.from_url("redis://redis:6379", decode_response=True)
# redis = 엄청 빠른 초소형 데이터베이스 (dict()처럼 키-값으로 저장)

def run():
    # While True:
    pass

# if문 - 무한 루프 도는 걸 방지! - 컴퓨터 터질 수 있음...
# python main.py로 실행되었을 때만, run()호출
if __name__ == "__main__":
    run()