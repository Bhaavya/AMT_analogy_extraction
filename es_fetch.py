from elasticsearch import Elasticsearch, helpers
terms = ["analogy","analogous","is like","are like","similar","similarly","imagine"]

def fetch():
	es = Elasticsearch(timeout=120)
	# query = {'query':{'match_phrase':{"fulltext":"juvenile delinquency"}}}
	query = {'query': {
"bool": { 
		"should": []
	,
	
	 "minimum_should_match" : 1,
	}},"highlight": {
    "fields": {
      "fulltext": {}
    },
   
 
    "fragment_size":0
  }}
 # "order": "score",
	for t in terms:
		query['query']['bool']['should'].append({'match_phrase':{'fulltext':t}})

	ids = []
	res = es.search(index='anlgy_paras',body=query)#Searching
	# print(res)
	if len(res['hits']['hits'])>0:

		return res['hits']['hits'][0]["highlight"]["fulltext"]
	else:
		return None
		


