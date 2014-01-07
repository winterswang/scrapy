from curl import Curl

url = 'http://localhost:6800/schedule.json'
curl =Curl(url)
dic = {'project':'soufun_s1','spider':'soufun_agent'}
res = curl.post(dic)
print res
