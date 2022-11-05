'''
import http.client

conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")

payload = "{}"

conn.request("GET", "/v0/topstories.json?print=pretty", payload)

res = conn.getresponse()
data = res.read()

d_data = data.decode("utf-8")

print(d_data[0])


import requests

url = "https://hacker-news.firebaseio.com/v0/showstories.json"

payload = "{}"
response = requests.request("GET", url, data=payload)

print(response.text)


https://hacker-news.firebaseio.com/v0/item/33405997.json?print=pretty
'''
from operator import itemgetter
import requests

#Make an API call and store the response
url='https://hacker-news.firebaseio.com/v0/showstories.json'
r=requests.get(url)
print(f"Status Code:{r.status_code}")

#Process the information about each submission
submission_ids=r.json()
submission_dicts= {}
i = 0
for submission_id in submission_ids[:30]:
    #Make a seperate api call for each id
    url1=f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json?print=pretty"
    r1=requests.get(url1)
    response_dict=r1.json()
    print(response_dict['title'])
    
    
    submission_dict[i]={
            'title':response_dict['title'],
            'hn_link':f"http://news.ycombinator.com/item?id={submission_id}",
            'comments':response_dict['descendants']
        }
    i += 1

print(submission_dict)



'''
    submission_dicts.append(submission_dict)
submission_dicts=sorted(submission_dicts,key=itemgetter('comments'),reverse=True)
for submission_dict in submission_dicts:
    print(f"\nTitle: {submission_dicts.get('title')}")
    print(f"\nDiscuission link: {submission_dicts.get('hn_link')}")

'''
