# 기반이 되는 이미지
FROM selenium/standalone-chrome:119.0-20231102

# 작업 디렉토리 설정
WORKDIR /usr/src

# 필요한 파일을 복사
COPY . .

RUN sudo apt update

RUN sudo apt install vim -y

RUN sudo apt install pip -y

# 파이썬 라이브러리 설치
RUN pip install -r requirements.txt

CMD ["python3", "app.py"]

