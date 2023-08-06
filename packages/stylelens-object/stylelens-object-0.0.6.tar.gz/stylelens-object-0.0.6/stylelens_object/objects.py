from stylelens_object.database import DataBase

class Objects(DataBase):
  def __init__(self):
    super().__init__()
    self.objects = self.db.objects

  def get_objects_with_null_index(self, offset=0, limit=50):
    try:
      r = self.objects.find({"index":None}).skip(offset).limit(limit)
    except Exception as e:
      print(e)

    return list(r)

  def add_object(self, object):
    try:
      r = self.objects.update_one({"name": object['name']},
                                  {"$set": object},
                                  upsert=True)
    except Exception as e:
      print(e)

    return r.raw_result

  def update_object(self, object):
    try:
      r = self.objects.update_one({"name": object['name']},
                                  {"$set": object})
    except Exception as e:
      print(e)
      return None

    return r.raw_result
