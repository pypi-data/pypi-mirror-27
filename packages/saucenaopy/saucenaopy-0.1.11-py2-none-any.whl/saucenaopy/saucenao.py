import sys
import json
import requests
from limiter import ShortLimiter, LongLimiter

class SauceNAO:

  def __init__(self, api_key, output_type=2, testmode=0, dbmask=None, dbmaski=None, db=999, numres=6, shortlimit=20, longlimit=300):
    params = dict()
    params['api_key'] = api_key
    params['output_type'] = output_type
    params['testmode'] = testmode
    params['dbmask'] = dbmask
    params['dbmaski'] = dbmaski
    params['db'] = db
    params['numres'] = numres
    self.params = params

    self.shortlimiter = ShortLimiter(shortlimit)
    self.longlimiter = LongLimiter(longlimit)

  def get_sauce(self, url):
    sthread = self.shortlimiter.acquire()
    lthread = self.longlimiter.acquire()
    threads = (sthread, lthread)

    self.params['url'] = url
    result = requests.get('https://saucenao.com/search.php', params=self.params)

    if self.verify_http_status(result, threads):
      data = self.load_json(result)
      if data is not None and self.verify_header_status(data, threads):
        return result.text

  def verify_http_status(self, result, threads):
    if result.status_code != 200:
      for thread in threads:
        thread.cancel()
      print 'HTTP Status', str(result.status_code)
      return False
    else:
      return True

  def verify_header_status(self, data, threads):
    header = data['header']
    if header['status'] != 0:
      for thread in threads:
        thread.cancel()
      print 'Header Status', str(header['status'])
      return False
    else:
      return True

  def load_json(self, result):
    try:
      data = json.loads(result.text)
      return data
    except ValueError:
      print 'Specified file does not seem to be an image.'

