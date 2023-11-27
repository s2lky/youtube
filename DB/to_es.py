import pandas as pd
from elasticsearch import Elasticsearch
# CSV 파일 경로
csv_file_path = '/content/youtube_bot_log.csv'

# CSV 파일을 데이터프레임으로 불러오기
df = pd.read_csv(csv_file_path, encoding='utf-8')

# 데이터프레임을 JSON 파일로 저장
json_file_path = 'data.json'
df.to_json(json_file_path, orient='records', lines=True)

# Elasticsearch 연결
es = Elasticsearch([{'host': '34.127.105.217', 'port': 9200, 'scheme': 'http'}])

# # 인덱스 생성
index_name = 'youtube'
es.indices.create(index=index_name)

# 인덱스 삭제 (존재하는 경우에만)
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# 인덱스 생성
es.indices.create(index=index_name)


# 데이터 삽입
with open(json_file_path, 'r') as data_file:
    bulk_data = data_file.readlines()
    for doc in bulk_data:
        es.index(index=index_name, body=doc)


# 인덱스 리프레시
es.indices.refresh(index=index_name)
