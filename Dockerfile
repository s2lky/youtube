# 기반이 되는 이미지
FROM selenium/standalone-chrome:119.0-20231102

RUN sudo chmod 777 usr/src

# 작업 디렉토리 설정
WORKDIR /usr/src

# 필요한 파일을 복사
COPY . .

RUN sudo apt update

RUN sudo apt install vim -y

RUN sudo apt install pip -y

RUN sudo apt install tor -y

# 파이썬 라이브러리 설치
RUN pip install -r requirements.txt

CMD ["bash", "-c", "./start_tor.sh && python3 app.py"]
