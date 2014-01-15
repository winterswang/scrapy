import urllib
import pycurl
import StringIO

class Curl:
    def __init__(self,url='http://127.0.0.1:6800/'):
        self.url = url
    def get(self):
 
        crl = pycurl.Curl()
        crl.setopt(pycurl.VERBOSE,1)
        crl.setopt(pycurl.FOLLOWLOCATION, 1)
        crl.setopt(pycurl.MAXREDIRS, 5)
        crl.fp = StringIO.StringIO()
        crl.setopt(pycurl.URL, self.url)
        crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
   
        try:
            crl.perform()
        except pycurl.error, error:
            errno, errstr = error
            print 'an error occured:',errstr

        res = crl.fp.getvalue()
        crl.close()
        return res

    def post(self,post_data_dic):
        
        crl = pycurl.Curl()
        crl.setopt(pycurl.VERBOSE,1)
        crl.setopt(pycurl.FOLLOWLOCATION, 1)
        crl.setopt(pycurl.MAXREDIRS, 5)
        #crl.setopt(pycurl.AUTOREFERER,1)
 
        crl.setopt(pycurl.CONNECTTIMEOUT, 60)
        crl.setopt(pycurl.TIMEOUT, 300)
        #crl.setopt(pycurl.PROXY,proxy)
        crl.setopt(pycurl.HTTPPROXYTUNNEL,1)
        #crl.setopt(pycurl.NOSIGNAL, 1)
        crl.fp = StringIO.StringIO()
        crl.setopt(pycurl.USERAGENT, "dhgu hoho")
 
        # Option -d/--data <data>   HTTP POST data
        crl.setopt(crl.POSTFIELDS,  urllib.urlencode(post_data_dic))
 
        crl.setopt(pycurl.URL, self.url)
        crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
        crl.perform()
 
        res = crl.fp.getvalue()
        crl.close()
        return res
