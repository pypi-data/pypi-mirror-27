from bson.objectid import ObjectId
from stylelens_product.database import DataBase

class Products(DataBase):
  def __init__(self):
    super(Products, self).__init__()
    self.products = self.db.products

  def add_product(self, product):
    object_id = None
    query = {"host_code": product['host_code'], "product_no": product["product_no"]}
    try:
      r = self.products.update_one(query,
                                  {"$set": product},
                                  upsert=True)
    except Exception as e:
      print(e)

    if 'upserted' in r.raw_result:
      product_id = str(r.raw_result['upserted'])

    return product_id

  def get_products_by_host_code_and_version_id(self,
                                              host_code, version_id,
                                              offset=0, limit=100):
    try:
      r = self.products.find({"host_code": host_code,
                              "version_id": version_id})\
                            .skip(offset).limit(limit)
    except Exception as e:
      print(e)

    return list(r)

  def update_product_by_id(self, product_id, product):
    try:
      r = self.products.update_one({"_id": ObjectId(product_id)},
                                  {"$set": product})
    except Exception as e:
      print(e)

    return r.modified_count

  def update_product_by_hostcode_and_productno(self, product):
    query = {"host_code": product['host_code'], "product_no": product['product_no']}
    try:
      r = self.products.update_one(query,
                                  {"$set": product},
                                  upsert=True)
    except Exception as e:
      print(e)

    return r.raw_result
