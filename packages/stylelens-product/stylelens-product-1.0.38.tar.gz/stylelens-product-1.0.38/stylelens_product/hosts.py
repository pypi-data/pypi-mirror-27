from bson.objectid import ObjectId
from stylelens_product.database import DataBase

HOST_STATUS_TODO = 'todo'
HOST_STATUS_DOING = 'doing'
HOST_STATUS_DONE = 'done'

class Hosts(DataBase):
  def __init__(self):
    super(Hosts, self).__init__()
    self.hosts = self.db.hosts

  def add_host(self, host):
    id = None
    query = {}
    query['host_code'] = host['host_code']
    host['crawl_status'] = HOST_STATUS_TODO

    try:
      r = self.hosts.update_one(query,
                               {"$set": host},
                               upsert=True)
    except Exception as e:
      print(e)

    if 'upserted' in r.raw_result:
      id = str(r.raw_result['upserted'])

    return id

  def get_hosts(self, version_id=None, crawl_status=HOST_STATUS_TODO, offset=0, limit=100):
    query = {}

    if version_id is not None:
      query['version_id'] = version_id

    if crawl_status is HOST_STATUS_TODO:
      query['$or'] = [{'crawl_status':HOST_STATUS_TODO}, {'crawl_status':None}]
    else:
      query['crawl_status'] = crawl_status

    try:
      r = self.hosts.find(query).skip(offset).limit(limit)
    except Exception as e:
      print(e)

    return list(r)

  def update_host(self, host):
    query = {"host_code": host['host_code']}
    try:
      r = self.hosts.update_one(query,
                                {"$set": host},
                                upsert=True)
    except Exception as e:
      print(e)

    return r.raw_result
