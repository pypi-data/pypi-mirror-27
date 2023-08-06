from stylelens_index.database import DataBase

class Indexes(DataBase):
  def __init__(self):
    super().__init__()
    self.indexes = self.db.indexes

  def add_image(self, image):
    try:
      query = {"host_code": image['host_code'],
               "product_no": image['product_no'],
               "version_id": image['version_id']}
      r = self.indexes.update_one(query,
                                 {"$set":image},
                                 upsert=True)
    except Exception as e:
      print(e)

    return r.raw_result

  def add_object(self, object):
    try:
      query = {"name": object['name'],
               "version_id": object['version_id']}
      r = self.indexes.update_one(query,
                                  {"$set":object},
                                  upsert=True)
    except Exception as e:
      print(e)

    return r.raw_result
