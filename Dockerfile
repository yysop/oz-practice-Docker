# 0305

FROM python:3.13-slim
WORKDIR /app
# 현재 경로에 있는 모든 파일을 Container 안으로 모두 복사
COPY . .
# requirements.txt에 있는 것들 한 번에 설치 
RUN pip install -r requirements.txt 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]