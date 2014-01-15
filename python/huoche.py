#encoding:utf-8
import urllib2,urllib,httplib
import json

request = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2014-02-09&leftTicketDTO.from_station=ZEK&leftTicketDTO.to_station=SHH&purpose_codes=0X00"
r = urllib.urlopen(request)
rlt = json.loads(r.read())
result = rlt['data']
if result:
	if isinstance(result,list):
		for l in result:
			if l['queryLeftNewDTO']['canWebBuy'] == 'Y':
				print l['queryLeftNewDTO']['station_train_code']

