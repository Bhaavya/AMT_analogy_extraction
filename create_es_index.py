from elasticsearch import Elasticsearch
from elasticsearch import helpers
import io
import os
import json
import datetime 
import re

index =  "anlgy_paras"

def gendata(idx_tup):

    for i,(fulltext) in enumerate(idx_tup):
        yield {
            "_index": index,
            "_id": i,
            "_source": {"fulltext":fulltext},
        }


def crt_idx(paras):
    es = Elasticsearch()
    es.indices.delete(index=index, ignore=[400, 404])


    es.indices.create(
    index=index,

    body={
    "mappings": {

    "properties": {  

    
    "fulltext": {"type": "text","analyzer": "simple","fielddata":True}
   

    }
    }
    }
    )
    helpers.bulk(es, gendata(paras))