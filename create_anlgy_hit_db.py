import sqlite3
import json 
import json 
import urllib.request as req
from bs4 import BeautifulSoup
from bs4 import Comment
from create_es_index import *
from es_fetch import *
import time 
from nltk.tokenize.punkt import PunktSentenceTokenizer
import re
import html
import string
db_name = 'ANLGY'



def main(hitid_path,wbpages_path,done_urls_path):
	wbpgs = json.load(open(wbpages_path,'r'))
	hitids = []

	
	done_urls =set()
	with open(hitid_path,'r') as f:
		hitids = f.readlines()
	cnt = 0

	for idx,(k,v) in enumerate(wbpgs.items()):

		if cnt<len(hitids)-1:
			crt_idx([v['body']])
			time.sleep(3)
			snippet = fetch()

			if snippet is None:
				snippet = [' '.join(v['body'].split(' ')[:50])]
			
			snippet_cxt = []
			sents = list(PunktSentenceTokenizer().span_tokenize(html.unescape(v['body'])))
			for snip in snippet:
				# print('+'*20,idx,snip)
				f = False
				
				snip = html.unescape(snip.strip().replace('<em>','').replace('</em>',''))
				if snip!='':
					# print(re.escape(snip).replace('\ ','(\s|'+'|'.join([re.escape(p) for p in string.punctuation])+')+'))	
					m = re.compile(re.escape(snip).replace('\ ','(\s|'+'|'.join([re.escape(p) for p in string.punctuation])+')+')).search(html.unescape(v['body']),pos=0)
					if m is not None:	
						sidx = m.start()
						eidx = m.end()
						sntidxs = []
						for sntidx,(start, end) in enumerate(sents):
							length = end - start
							if sidx in range(start,end+1) or eidx in range(start,end+1):
						
								sntidxs.append(sntidx)
						cxt = ''
						
						snippet_cxt.append('INSNIPRTR'.join([str(sntidx) for sntidx in sntidxs ]))	
						
					else:
						print("ERROR",snip,v['body'])


				
			snippet_cxt = 'SNIPSEPARATOR'.join(snippet_cxt)
			ssents = []
			for start,end in sents:
				ssents.append('INSNIPRTR'.join([str(start),str(end)]))
			ssents = 'SNIPSEPARATOR'.join(ssents)
			snippet = 'SNIPSEPARATOR'.join(snippet)

			if v['body']!=None:
				con = sqlite3.connect(db_name)
				cur = con.cursor()
				cur.execute("INSERT into CLSFY VALUES (?,?,?,?,?,?,?,?)",[k,hitids[idx].strip('\n'),v['title'],snippet,snippet_cxt,ssents,v['query'],v['body']])
				con.commit()
				con.close()
				done_urls.add(k)
				cnt +=1
		else:
			break
	# with open(done_urls_path,'w') as f:
	# 	for du in done_urls:
	# 		f.write(du+'\n')


if __name__ == '__main__':
	hitid_path = '../data/hitids.txt'
	wbpages_path = '../data/webpgs.json'
	done_urls_path = '../data/added_hits.txt'
	con = sqlite3.connect(db_name)
	cur = con.cursor()

	# # # # # # Create table
	cur.execute('''CREATE TABLE IF NOT EXISTS  'CLSFY' ( URL text, HITID text,TITLE text, SNIPPET text, SNIPPET_CXT text, SENTS text, QUERY text, BODY text)''')
	# cur.execute('''SELECT * from CLSFY''')
	# print(cur.fetchall())
	con.commit()
	con.close()
	# print(get_pg_text('https://www.kdnuggets.com/2018/06/intuitive-introduction-gradient-descent.html'))
	main(hitid_path,wbpages_path,done_urls_path)
