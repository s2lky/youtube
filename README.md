# 유튜브 알고리즘 리버스 엔지니어링

---

**프로젝트 기간:** 2023.11.05 ~ 2023.12.15 (6주)

**프로젝트 도구:** AWS EC2, Selenium, Tor, Docker, PostgreSQL, Elastic Search, Kibana, Github

**사용 언어:** Python, SQL

---

### ****프로젝트 개요****

- 유튜브의 알고리즘을 리버스 엔지니어링을 통해서 분석해보는 프로젝트

### 프로젝트 배경

- 스타트업 연계 프로젝트에서 기업이 요청한 주제에 맞춰서 진행한 프로젝트

### 프로젝트 아키텍쳐
![Architecture](https://github.com/s2lky/youtube/assets/132236456/a619bb9b-d175-41a4-b658-f1f87e0834de)

### 프로젝트 기술 스택

- **DevOps**
    
    ![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
    
- **Database**
    
    ![PostgreSQL](https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
    ![ElasticSearch](https://img.shields.io/badge/elasticsearch-005571?style=for-the-badge&logo=elasticsearch&logoColor=white)

- **Dashboard**

    ![Kibana](https://img.shields.io/badge/kibana-005571?style=for-the-badge&logo=kibana&logoColor=white)
  
**ElasticSearch/Kibana 선택 이유**

- ElasticSearch의 기본적인 형태소 분석기를 통해 간단하게 페르소나와 관련된 키워드 생성이 가능할 것이라 판단
- 수집한 데이터를 많은 추가적인 과정 필요없이 클릭 몇 번 만으로도, 대시보드 기능을 통해 시각화 가능
- 형태소 분석과 대시보드로 어느 정도의 분석이 가능하지 않을까?라는 생각을 가지고 선택하게 되었음

### 개발 인원

| 이름   | 담당 업무                                                                                                                                                                                                 |
|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 김동호 | - DB 설계, Docker를 통한 크롤러 관리 |
| 이혜원 | - 페르소나별 키워드 생성, 데이터 분석 |
| 정윤재 | - 유튜브 크롤러 봇 개발 및 데이터 적재 |
| 서은경 | - Elastic Search 및 Kibana 설정, Kibana 대시보드 생성 |

### 프로젝트 진행 과정

1. 유튜브 봇 개발
2. DB 적재
3. 대시보드 생성

### 프로젝트 구현 내용

1. 유튜브 봇 개발
![crawler](https://github.com/s2lky/youtube/assets/132236456/c8952b48-3dd9-44b5-9ae8-f0114b180b4a)

2. Elastic Search 적재
![es1](https://github.com/s2lky/youtube/assets/132236456/eb5b2198-4655-4829-b85b-4b0c3fd29c4e)
![es2](https://github.com/s2lky/youtube/assets/132236456/96fe9778-975e-42a4-ae95-8057fdef73e1)

3. 대시보드 생성
![kibana](https://github.com/s2lky/youtube/assets/132236456/faa0951c-fae0-4e9b-857c-3c563f51875e)

   
### 프로젝트 한계 및 개선 방안

**한계**

- selenium과 Tor의 높은 리소스 점유율으로 인한 적은 컨테이너 수
- 컨테이너를 올리기 위해 하나씩 직접 입력한 후 docker compose up 명령어를 통해서 컨테이너를 올림. 컨테이너가 많아지면 귀찮아지게 됨.

**개선 방안**

- docker swarm이나 k8s를 통해서 컨테이너를 yml파일에 하나씩 입력해서 컨테이너를 생성할 필요없이 한 번의 작업으로 끝나도록 개선
