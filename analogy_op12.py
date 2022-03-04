# coding=utf8
import sys
import os
import json 
sys.path.insert(0, os.path.dirname(__file__))
from flask import Flask,jsonify
from flask import make_response, request, current_app
from flask import render_template, flash,redirect 
from flask import Flask,jsonify,url_for
from flask import make_response, request, current_app
from flask import render_template
from flask_session import Session
from flask import session
import sqlite3
import pprint
import requests
import string
import re
# import regex
import html



app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)
# html = HTMLParser.HTMLParser()


db_name = 'ANLGY'

def read_sql_assn(q_hitid,wid):
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cmd = "SELECT * from  ASSN where HITID=(?) and WID=(?)"
        cur.execute(cmd,(q_hitid,wid))
        results = {}
        desc = cur.description

        column_names = [col[0] for col in desc]
        for idx,c in enumerate(cur.fetchone()):   

            results[column_names[idx]] = c
        # print(results,q_hitid)
        con.commit()
        con.close()
        return results

def read_sql_bal(q_hitid):
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cmd = "SELECT * from  BAL where HITID=(?)"
        cur.execute(cmd,(q_hitid,))
        results = {}
        desc = cur.description

        column_names = [col[0] for col in desc]
        for idx,c in enumerate(cur.fetchone()):   

            results[column_names[idx]] = c
        # print(results,q_hitid)
        con.commit()
        con.close()
        return results

def insert_sql_bal(q_hitid):
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute("INSERT into BAL VALUES (?,?)",[q_hitid,0])
        con.commit()
        con.close()

def insert_sql_assn(q_hitid,wid,url):
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute("INSERT into ASSN VALUES (?,?,?)",[q_hitid,wid,url])
        con.commit()
        con.close()



def update_sql(q_hitid,flg):
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute("UPDATE BAL set FLAG = (?) where HITID = (?)",[flg,q_hitid])
        con.commit()
        con.close()

def read_sql(q_hitid):
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cmd = "SELECT * from CLSFY where HITID=(?)"
        cur.execute(cmd,(q_hitid,))
        results = {}
        desc = cur.description

        column_names = [col[0] for col in desc]
        for idx,c in enumerate(cur.fetchone()):   

            results[column_names[idx]] = c
        # print(results,q_hitid)
        con.commit()
        con.close()
        return results

def get_fmt_txt_handler(snippet,st_bdy,add_a=False):
   # print(snippet,st_bdy)
    for snip in snippet:
        # snip = snip.strip()
        snip = html.unescape(snip.strip().replace('<em>','').replace('</em>',''))
        if snip!='':
            f = 0
            mf = ''
            # print(snip)
            # print('(?e)('+regex.escape(snip).replace('\ ','(\s+|'+regex.escape(string.punctuation)+'+)')+'){e<=3}')
            # for idx,m in enumerate(list(regex.finditer('(?e)('+regex.escape(snip).replace('\ ','(\s+|'+regex.escape(string.punctuation)+'+)')+'){e<=3}',st_bdy))):
            beg = 0
            while(beg<len(st_bdy)):
                # print(re.escape(snip).replace('\ ','(\s|'+'|'.join(list(re.escape(string.punctuation)))+')+'))
                # print(st_bdy)
                m = re.compile(re.escape(snip).replace('\ ','(\s|'+'|'.join([re.escape(p) for p in string.punctuation])+')+')).search(st_bdy,pos=beg)
                
                # print(m)
                if m is None:
                    break
                print(m)
                f =1 
                # if idx>0:
                #     break 

                sidx = m.start()
                eidx = m.end()
                mf = m
            # ifs f:
                if add_a and beg==0:
                    st_bdy = st_bdy[:sidx]+'ATTRIB_TAG_IMHERE'+'STARTANLGYSNIP'+st_bdy[sidx:eidx] + 'ENDANLGYSNIP' + st_bdy[eidx:]
                else:
                    st_bdy = st_bdy[:sidx]+'STARTANLGYSNIP'+st_bdy[sidx:eidx] + 'ENDANLGYSNIP' + st_bdy[eidx:]
            
                beg = eidx+1+len('STARTANLGYSNIP')+len('ENDANLGYSNIP')
    if add_a:
        span_tag = '<span style="background:yellow;text-transform:inherit;font-weight:inherit;font-size:inherit;white-space:inherit;position:inherit;top:0em;display:inline">'
    else:
        span_tag = '<span style="background:yellow">'
    ftxt=html.escape(st_bdy).replace('\n','<br><br>').replace('STARTANLGYSNIP',span_tag).replace('ENDANLGYSNIP','</span>').replace('ATTRIB_TAG_IMHERE','<a id="imhere"></a>')
    return ftxt

@app.route('/submit', methods=['POST'])
def submit():
    json_data = request.get_json()
    wid = json_data['wid']
    hid = json_data['hid']
    with open('submit.txt','a') as f:
        f.write(wid+'\t'+hid+'\n')
   
    return jsonify({'msg':'success'})

@app.route('/get_snip', methods=['POST'])
def get_fmt_txt():
    json_data = request.get_json()
    snippet = [s[:-4] for s in json_data['snippet']]

    txt = json_data['txt']
    wid = json_data['wid']
    try:
        add_a = json_data['add_a']
    except:
        add_a = False
    
    ftxt = get_fmt_txt_handler(snippet,txt,add_a)
    with open('click.txt','a') as f:
        f.write(wid+'###############'+' '.join(snippet).replace('\n',' ')+'###############'+txt.replace('\n',' ')+'\n')
    return jsonify(ftxt=ftxt)

@app.route('/', methods=['GET','POST'])
def ann():
    try:
        query = request.args.get('hitId')
        wid = request.args.get('workerId')
        results = read_sql(query)
    except Exception as e:
        print(e,query,flush=True)
        return render_template('error.html')
    # query = 't123'
    # results = read_sql(query)

    try:
        results_assn = read_sql_assn(query,wid)
        condition = results_assn['COND']

    except Exception as e:
        print(e)
        try:
            results_bal = read_sql_bal(query)
            flg = int(results_bal['FLAG'])
        except Exception as e:
            print(e,flush=True)
            if wid is not None:
                insert_sql_bal(query)
      
            flg = 0 
        if flg == 0:
            if wid is not None:
                update_sql(query,1)
            condition = 0            
        else:
            if wid is not None:
                update_sql(query,0)
            condition = 1
        insert_sql_assn(query,wid,condition)

    print(wid,condition)


#     results = {'URL':'https://www.kdnuggets.com/2018/06/intuitive-introduction-gradient-descent.html','TITLE':'An Intuitive Introduction to Gradient Descent','SNIPPET':'''Minimizing the cost function is <b>analogous</b> to trying to reach lower altitudes. You are blind folded, since we don't have the luxury of evaluating (seeing) the ...''','BODY':'''Analogy (from Greek ἀναλογία, analogia, "proportion", from ana- "upon, according to" [also "against", "anew"] + logos "ratio" [also "word, speech, reckoning"][1][2]) is a cognitive process of transferring information or meaning from a particular subject (the analog, or source) to another (the target), or a linguistic expression corresponding to such a process. In a narrower sense, analogy is an inference or an argument from one particular to another particular, as opposed to deduction, induction, and abduction, in which at least one of the premises, or the conclusion, is general rather than particular in nature. The term analogy can also refer to the relation between the source and the target themselves, which is often (though not always) a similarity, as in the biological notion of analogy.orem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

# Why do we use it?
# It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).


# Where does it come from?
# # Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Lati''','SNIPPET':'In a narrower sense, analogy is an inference or an argument from one particular to another particular, as opposed to deduction, induction, and abduction, in which at least one of the premises, or the conclusion, is general rather than particular in nature.','SNIPPET_CXT':'1','SENTS':'0INSNIPRTR362SNIPSEPARATOR363INSNIPRTR619SNIPSEPARATOR620INSNIPRTR801'}
    # print(results)
    # results['SNIPPET']
    # ,
    # print(results['BODY'])
    # st_bdy = results['BODY'].translate(str.maketrans('', '', string.punctuation)).replace('\n',' ')
    st_bdy = results['BODY']



    # snippet = html.unescape(results['SNIPPET'])
    # print(snippet,st_bdy)
    # words = [' analogy ',' comparable ',' analogous ',' compare ',' comparing ',' is like a ']
    # for snip in snippet.split('...'):
    # for word in words:
    snippet = results['SNIPPET'].split('SNIPSEPARATOR')
    st_bdy = get_fmt_txt_handler(snippet,st_bdy)
   

                # print(f,sidx,eidx,mf)
    snippet_cxt = []
    for s in results['SNIPPET_CXT'].split('SNIPSEPARATOR'):
        cxt = []
        for s1 in s.split('INSNIPRTR'):

            cxt.append(int(s1))
        snippet_cxt.append(cxt)

    sents = []

    for s in results['SENTS'].split('SNIPSEPARATOR'):
        sent = []
        for s1 in s.split('INSNIPRTR'):

            sent.append(int(s1))
        sents.append(sent)


    return render_template('label.html',url=results['URL'],title=results['TITLE'],snippet=[html.escape(s.replace('<em>','').replace('</em>',''))+'... ' for s in snippet],hid=query,snippet_cxt = snippet_cxt,sents=sents,sent_bdy=html.unescape(results['BODY']),snip_cnt=list(range(len(snippet_cxt))),body=st_bdy,wid=wid,condition=condition)


if __name__ == '__main__':
    
    con = sqlite3.connect(db_name)
    # cur = con.cursor()

    # # # # # # # Create table
    # # cur.execute('''CREATE TABLE 'CLSFY' ( URL text, HITID text,TITLE text, SNIPPET text,  QUERY text, BODY text)''')
   
    # # cur.execute("INSERT into CLSFY VALUES (?,?,?,?,?)",['https://en.wikipedia.org/wiki/Analogy','t123','Wiki','Analogy (from Greek ἀναλογία, analogia, "proportion", from ana- "upon, according to" [also "against", "anew"] + logos "ratio" [also "word, speech, reckoning"][1][2]) is a cognitive process of transferring information or meaning from a particular subject (the analog, or source) to another (the target), or a linguistic expression corresponding to such a process. In a narrower sense, analogy is an inference or an argument from one particular to another particular, as opposed to deduction, induction, and abduction, in which at least one of the premises, or the conclusion, is general rather than particular in nature. The term analogy can also refer to the relation between the source and the target themselves, which is often (though not always) a similarity, as in the biological notion of analogy.','analogy',''])
    # cur.execute('''DROP TABLE 'BAL' ''')
    # cur.execute('''DROP TABLE 'ASSN' ''')
    # cur.execute('''CREATE TABLE 'BAL' ( HITID text, FLAG text)''')
    # cur.execute('''CREATE TABLE 'ASSN' ( HITID text, WID text, COND text)''')
    # con.commit()
    # con.close()
    app.run(host='localhost',port=6005, debug=False)





