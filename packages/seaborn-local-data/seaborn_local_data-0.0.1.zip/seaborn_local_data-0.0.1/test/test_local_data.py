from seaborn.local_data import *

def smoke_test():
    path = '%s/local_data.json' % os.path.split(__file__)[0]
    if os.path.exists(path):
        os.remove(path)
    local_data = LocalData()
    local_data['username'] = 'hello'
    local_data.password = 'world'
    assert dict(username=local_data.username, password=local_data['password']) == json.load(open(path, 'r'))


if __name__ == '__main__':
    smoke_test()
