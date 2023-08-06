from stylelens_index.database import DataBase

class Indexes(DataBase):
  def __init__(self):
    super().__init__()
    self.images = self.db.images
    self.objects = self.db.objects

  def add_image(self, image):
    try:
      query = {"host_code": image['host_code'],
               "product_no": image['product_no'],
               "version_id": image['version_id']}
      r = self.images.update_one(query,
                                 {"$set":image},
                                 upsert=True)
    except Exception as e:
      print(e)

    return r.raw_result

  def add_object(self, object):
    try:
      query = {"name": object['name'],
               "version_id": object['version_id']}
      r = self.objects.update_one(query,
                                  {"$set":object},
                                  upsert=True)
    except Exception as e:
      print(e)

    return r.raw_result

  # def get_images_by_object(self, object_id, offset=0, limit=100):
  #   query = {'_id'}
  #
  #   try:
  #     r = self.objects.find({query}).skip(offset).limit(limit)
  #
  #   except Exception as e:
  #     print(e)
  #
  #   return list(r)
