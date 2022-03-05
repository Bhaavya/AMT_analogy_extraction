import boto3
import urllib.request
from bs4 import BeautifulSoup
from bs4.element import Comment
import datetime 
ACCESS_ID = ACCESS_ID
SECRET_KEY = SECRET_KEY
MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

MTURK_PROD = 'https://mechanicalturk.amazonaws.com'

def PostHits():
  mturk = boto3.client('mturk',
   aws_access_key_id = ACCESS_ID,
   aws_secret_access_key = SECRET_KEY,
   region_name='us-east-1',
    endpoint_url = MTURK_SANDBOX
)
  # iam = boto3.resource('iam',aws_access_key_id = ACCESS_ID,
   # aws_secret_access_key = SECRET_KEY,)
  hitids = []
  num_hits = 15000
  print(mturk.get_account_balance()['AvailableBalance'])

  # print(iam.CurrentUser().arn.split(':')[4])
  # with open('../../data/hitids1.txt') as f:
  #   hids = f.readlines()
  # for hid in hids:
  '''
  for i in range(5):
     for item in mturk.list_hits()['HITs']:
       hid=item['HITId']
       # hid = hid.strip('\n')
       status=mturk.get_hit(HITId=hid)['HIT']['HITStatus']
       print('HITStatus:', status)

  #     # If HIT is active then set it to expire immediately
       if status=='Assignable':
           response = mturk.update_expiration_for_hit(
              HITId=hid,
               ExpireAt=60
           )        

  #     # Delete the HIT
       try:
           mturk.delete_hit(HITId=hid)
       except:
           print('Not deleted')
       else:
           print('Deleted')
    # 
  '''
  for i in range(num_hits):
    question = open('q.xml').read()

    new_hit = mturk.create_hit(
      Title = 'Analogies in webpages',
      Description = 'Identify whether a webpage contains any analogies or not. Highlight any analogies, if present.',
      Keywords = 'text, labeling, extraction, highlighting, analogy',
      Reward = '0.20',
      MaxAssignments = 6,
      LifetimeInSeconds = 17280000,
      AssignmentDurationInSeconds = 6000,
      AutoApprovalDelayInSeconds = 144000,
      Question = question
      , QualificationRequirements=[{'QualificationTypeId': '00000000000000000040',
    'Comparator': 'GreaterThan',
'IntegerValues':[500]},
    {'QualificationTypeId': '000000000000000000L0','Comparator': 'GreaterThan',
  'IntegerValues':[96]}]
  )
    print(i,"A new HIT has been created. You can preview it here:")
    print("https://workerssandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'])
  # print("HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)")
  # Remember to modify the URL above when you're publishing
  # HITs to the live marketplace.
  # Use: https://worker.mturk.com/mturk/preview?groupId=
    hitids.append(new_hit['HIT']['HITId'] )
  with open('../data/hitids_sndbx.txt','w') as f:
    for h in hitids:
      f.write(h+'\n')
    
if __name__ == '__main__':
  
  PostHits()
  # print(get_pg_text('https://www.upgrad.com/blog/gradient-descent-in-logistic-regression/'))
