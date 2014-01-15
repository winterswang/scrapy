from curl import Curl
import json

url = 'http://localhost:6800/listprojects.json'
curl = Curl(url)
res = curl.get()
rlt = json.loads(res)

if len(rlt['projects']) ==0:
    print 'adding the project\n'
    url = 'http://localhost:6800/addversion.json'
    curl.set_url(url)
    dic = {'project':'soufun_s1','version':'r23','egg':'@soufun_s1/soufun_s1.egg'}
    res = curl.post(dic)
    print res

for r in rlt['projects']:
    print r
