
from BeautifulSoup import BeautifulSoup as bs
import urlparse
from urllib import urlretrieve
import urllib2
import os
import sys
import gzip
from StringIO import StringIO

def main(url, out_folder="/test/"):
    """Downloads all the images at 'url' to /test/"""
    request = urllib2.Request(url)
    request.add_header('Accept-encoding','gzip')
    response = urllib2.urlopen(request)
    contentAll = response
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        contentAll = f.read()
    soup = bs(contentAll,fromEncoding="gb18030")
    #print soup.originalEncoding
    #print soup.prettify()
    parsed = list(urlparse.urlparse(url))

    for image in soup.findAll("img"):
        print "Image:%(src)s" % image
        image_url = urlparse.urljoin(url, image['src'])
        filename = image["src"].split("/")[-1]
        outpath = os.path.join(out_folder,filename)
        urlretrieve(image_url,outpath)

def _usage():
    print "usage: python dumpimages.py http://example.com [outpath]"

if __name__ == "__main__":
    url = sys.argv[-1]
    out_folder = "/test/"
    if not url.lower().startswith("http"):
        out_folder = sys.argv[-1]
        url = sys.argv[-2]
        if not url.lower().startswith("http"):
            _usage()
            sys.exit(-1)
    main(url, out_folder)
