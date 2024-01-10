import pandas as pd
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
from elasticsearch.exceptions import NotFoundError
import json
import traceback
from datetime import datetime


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
    index_name = 'youtube_with_nori'
    
    # Elasticsearch 클라이언트 생성
    es = Elasticsearch(hosts=[{'host': es_host, 'port': es_port, 'scheme': 'http'}], basic_auth=(es_user, es_password))

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
                    "first_ad": {"type": "keyword"},
                    "first_ad_name": {"type": "keyword"},
                    "second_ad": {"type": "keyword"},
                    "second_ad_name": {"type": "keyword"},
                    "first_break_ad": {"type": "keyword"},
                    "first_break_ad_name": {"type": "keyword"},
                    "second_break_ad": {"type": "keyword"},
                    "second_break_ad_name": {"type": "keyword"},
                    "keyword": {"type": "keyword"},
                    "likes": {"type": "long"},
                    "persona": {"type": "keyword"},
                    "session": {"type": "long"},
                    "describe": {"type": "text",
                                 "analyzer": "nori_analyzer",
                                 "fielddata": True},
                                #  "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}},
                    "title": {"type": "text",
                              "analyzer": "nori_analyzer",
                              "fielddata": True},
                            #   "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
                    "upload": {"type": "date"},
                    "url": {"type": "keyword"},
                    "viewership": {"type": "long"}
                }
            },
            "settings": {
                "analysis": {
                    "filter": {
                        "nori_posfilter": {
                            "type": "nori_part_of_speech",
                            "stoptags": [
                            "E",
                            "IC",
                            "J",
                            "MAG",
                            "MAJ",
                            "MM",
                            "NA",
                            "SC",
                            "SE",
                            "SF",
                            "SN",
                            "SP",
                            "SSC",
                            "SSO",
                            "SY",
                            "UNA",
                            "VSV",
                            "XPN",
                            "XSA",
                            "XSN",
                            "XSV"
                            ]
                        }
                        # "exclude_single_char": {
                    #     "type": "length",
                    #     "min": 5,
                    #     "max": 20
                    #     }
                    },
                    "tokenizer": {
                        "nori_tokenizer": {
                            "type": "nori_tokenizer"
                            # "decompound_mode": "mixed"
                        }
                    },
                    "analyzer": {
                        "nori_analyzer": {
                            "type": "nori",
                            "tokenizer": "nori_tokenizer",
                            "filter": ["nori_posfilter"]
                            }
                        }
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
    es = Elasticsearch(hosts=[{'host': es_host, 'port': es_port, 'scheme': 'http'}], basic_auth=(es_user, es_password))

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
