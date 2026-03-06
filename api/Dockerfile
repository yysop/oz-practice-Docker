# 0305

# slim - 경량 버전
FROM python:3.13-slim 
WORKDIR /app
# 현재 경로에 있는 모든 파일을 Container 안으로 모두 복사
COPY . .
# requirements.txt에 있는 것들 한 번에 설치 
RUN pip install -r requirements.txt 
# --reload : 코드 변경될때마다 자동으로 재시작 # "--reload-dir", "/app" 감시할 폴더를 명확히 지정함
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app"]
