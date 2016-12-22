```
$ python --version
Python 2.7.12
```

# Setup/run
```bash
git clone https://gist.github.com/ab633fb149d7b02e3916c370d57becd2.git ./django-repo
cd ./django-repo
# mkvirtualenv django-repo
pip install django==1.9.4 https://github.com/DataDog/dd-trace-py/archive/v0.5.2.tar.gz
python manage.py runserver
```

# Producing the error
Open http://127.0.0.1:8000/

Will receive the following error:

```
error sending spans
Traceback (most recent call last):
  File "/Users/brettlangdon/.env/django-test/lib/python2.7/site-packages/ddtrace/writer.py", line 127, in _target
    self.api.send_services(services)
  File "/Users/brettlangdon/.env/django-test/lib/python2.7/site-packages/ddtrace/api.py", line 65, in send_services
    response = self._put(self._services, data)
  File "/Users/brettlangdon/.env/django-test/lib/python2.7/site-packages/ddtrace/api.py", line 78, in _put
    conn.request("PUT", endpoint, data, self._headers)
  File "/usr/local/Cellar/python/2.7.12_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/httplib.py", line 1057, in request
    self._send_request(method, url, body, headers)
  File "/usr/local/Cellar/python/2.7.12_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/httplib.py", line 1097, in _send_request
    self.endheaders(body)
  File "/usr/local/Cellar/python/2.7.12_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/httplib.py", line 1053, in endheaders
    self._send_output(message_body)
  File "/usr/local/Cellar/python/2.7.12_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/httplib.py", line 897, in _send_output
    self.send(msg)
  File "/usr/local/Cellar/python/2.7.12_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/httplib.py", line 859, in send
    self.connect()
  File "/usr/local/Cellar/python/2.7.12_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/httplib.py", line 836, in connect
    self.timeout, self.source_address)
  File "/usr/local/Cellar/python/2.7.12_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/socket.py", line 557, in create_connection
    for res in getaddrinfo(host, port, 0, SOCK_STREAM):
error: getaddrinfo() argument 2 must be integer or string
```

# Reproducing via Python repl

```
$ python
Python 2.7.12 (default, Oct 11 2016, 15:46:18)
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.38)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from socket import *
>>> getaddrinfo('127.0.0.1', u'7777', 0, SOCK_STREAM)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
socket.error: getaddrinfo() argument 2 must be integer or string
>>> getaddrinfo('127.0.0.1', '7777', 0, SOCK_STREAM)
[(2, 1, 6, '', ('127.0.0.1', 7777))]
>>> getaddrinfo('127.0.0.1', 7777, 0, SOCK_STREAM)
[(2, 1, 6, '', ('127.0.0.1', 7777))]
>>>
```

`getaddrinfo` only allows `str` or `int` for the port number and errors on `unicode`. This is not an issue for Python 3.

# Fixing the problem

```python
DATADOG_TRACE = {
    'AGENT_PORT': 7777,
}
```
