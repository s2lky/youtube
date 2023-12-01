import pandas as pd
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
from elasticsearch.exceptions import NotFoundError
import json


load_dotenv(verbose=True)

es_user = os.getenv('ES_USER')
es_password = os.getenv('ES_PASSWORD')
es_host = os.getenv('ES_HOST')
es_port = int(os.getenv('ES_PORT'))


def data_insert(json_data, index_name, es):
    for record in json_data.split('\n'):
        if record:
            es.index(index=index_name, body=json.loads(record))


def youtube_data(df):
    json_data = df.to_json(orient='records', lines=True)
    index_name = 'youtube'
    
    # Elasticsearch 클라이언트 생성
    es = Elasticsearch(hosts=[{'host': es_host, 'port': es_port, 'scheme': 'http'}], http_auth=(es_user, es_password))
    
    try:
    # 기존 인덱스 확인
        es.indices.get(index=index_name)
        index_exists = True
    except NotFoundError:
        index_exists = False

    if not index_exists:    
    # 인덱스 생성
        es.indices.create(index=index_name, body={
            "mappings": {
                "properties": {
                    "@timestamp": {"type": "date"},
                    "channel": {"type": "keyword"},
                    "describe": {"type": "text"},
                    "first_ad": {"type": "keyword"},
                    "second_ad": {"type": "keyword"},
                    "keyword": {"type": "keyword"},
                    "likes": {"type": "long"},
                    "persona": {"type": "keyword"},
                    "session": {"type": "long"},
                    "title": {"type": "text"},
                    "upload": {"type": "date", "format": "iso8601"},
                    "url": {"type": "keyword"},
                    "viewership": {"type": "long"}
                }
            }
        }, ignore=400)

    # JSON 데이터를 엘라스틱서치에 색인
    data_insert(json_data=json_data, index_name=index_name, es=es)
    # 클라이언트 종료
    es.transport.close()

    
def youtube_failed_log(df):
    json_data = df.to_json(orient='records', lines=True)
    index_name = 'logs'
    es = Elasticsearch(hosts=[{'host': es_host, 'port': es_port, 'scheme': 'http'}], http_auth=(es_user, es_password))
    
    try:
    # 기존 인덱스 확인
        es.indices.get(index=index_name)
        index_exists = True
    except NotFoundError:
        index_exists = False

    if not index_exists:
        es.indices.create(index=index_name, body={
            "mappings": {
                "properties": {
                    "@timestamp": {"type": "date"},
                    "ErrorMessage": {"type": "text"}
                }
            }
        }, ignore=400)
        
    data_insert(json_data=json_data, index_name=index_name, es=es)
    es.transport.close()
    
if __name__ == "__main__":
    print(type(es_port))
