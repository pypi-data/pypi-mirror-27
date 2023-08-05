**crawl_requests**
==================

*Usage:*
--------
>>>import requests

>>>from true_encoding.encode_bug import encode_bug

>>>res = requests.get('https://python.org')

>>>res.encoding = encode_bug(res)

>>>content = res.text
