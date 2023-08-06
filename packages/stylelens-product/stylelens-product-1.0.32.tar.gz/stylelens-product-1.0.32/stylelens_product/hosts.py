from bson.objectid import ObjectId
from stylelens_product.database import DataBase

class Hosts(DataBase):
  def __init__(self):
    super(Hosts, self).__init__()
    self.hosts = self.db.hosts

  def add_host(self, host):
    id = None
    query = {"host_code": host['host_code']}
    try:
      r = self.hosts.update_one(query,
                               {"$set": host},
                               upsert=True)
    except Exception as e:
      print(e)

    if 'upserted' in r.raw_result:
      id = str(r.raw_result['upserted'])

    return id

  def get_hosts(self, offset=0, limit=100):
    try:
      r = self.hosts.find({}).skip(offset).limit(limit)
    except Exception as e:
      print(e)

    return list(r)

