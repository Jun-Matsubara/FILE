from tinydb import TinyDB,where
import uuid, time, os

BASE_DIR = os.path.dirname(__file__)
FILES_DIR = BASE_DIR + '/files'
DATA_FILE = BASE_DIR + '/data/data.json'

def save_file(upfile,meta):
    id = 'FS_' + uuid.uuid4().hex
    #file_path=FILES_DIR + '/' + id + '.jpg'
    file_path=FILES_DIR + '/' + upfile.name
    with open(file_path, 'wb+') as destination: 
        for chunk in upfile.chunks():
            destination.write(chunk) 
    db = TinyDB(DATA_FILE)
    meta['id'] = id
    term = meta['limit'] * 60 * 60 * 24
    meta['time_limit']= time.time() + term
    db.insert(meta)
    print('OK4')
    return id

def get_data(id):
    db= TinyDB(DATA_FILE)
    f = db.get(where('id') == id)
    if f is not None:
        path= FILES_DIR + '/' + id + '.jpg'
        db.update({'path':path},where('id')== id)
    print('OK7')
    return f

def set_data(id,meta):
    db= TinyDB(DATA_FILE)
    db.update({'count':meta['count']}, where('id')== id)
    print('OK11')