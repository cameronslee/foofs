import os
import tempfile
import hashlib
import shutil


# Master Server #
def master(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    key = env['PATH_INFO']
    return [b"Master out"]


# Volume Server #
class Cache(object):
    def __init__(self, basedir):
        self.basedir = os.path.realpath(basedir)
        self.tmpdir = os.path.join(self.basedir, "tmp")
        os.makedirs(self.tmpdir, exist_ok=True)
        print(self.basedir)
        print(self.tmpdir)

        # clear temp dir
        for f in os.listdir(self.tmpdir):
            os.unlink(os.path.join(self.tmpdir, f))

        print("cache: ", basedir)

    def hashKey(self, key, mkdir_ok=False):
        key = hashlib.md5(key.encode('utf-8')).hexdigest()

        path = self.basedir+"/"+key[0:2]+"/"+key[0:4]
        if not os.path.isdir(path) and mkdir_ok:

            os.makedirs(path, exist_ok=True)

        return os.path.join(path, key)

    def exists(self, key):
        return os.path.isfile(self.hashKey(key))

    def get(self, key):
        try:
            return open(self.hashKey(key), "rb")
        except FileNotFoundError:
            return None

    def put(self, key, stream):
        with tempfile.NamedTemporaryFile(dir=self.tmpdir, delete=False) as f:
            shutil.copyfileobj(stream, f)

        os.rename(f.name, self.hashKey(key, True))

    def delete(self, key):
        try:
            os.unlink(self.hashKey(key))
            return True
        except FileNotFoundError:
            pass
        return False


# Volume Server Running
if os.environ['TYPE'] == "volume":
    c = Cache(os.environ['VOLUME'])


def volume(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    key = env['PATH_INFO']

    req_method = env['REQUEST_METHOD']

    val_len = int(env.get('CONTENT_LENGTH', 0))

    if req_method == 'PUT':
        print('PUT: Content Len: ', val_len)
        if val_len > 0:
            i = env['wsgi.input']

            c.put(key, i)
        else:
            return [b"key length must be greater than 0"]

    if req_method == 'GET':
        if c.exists(key):
            return c.get(key)
        else:
            return [b"not found"]

    if req_method == 'DELETE':
        if c.delete(key):
            return [b"deleted"]
        else:
            return [b"not found"]

    return [b"Volume out"]
