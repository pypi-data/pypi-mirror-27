
from bson.objectid import ObjectId
from stylelens_object.database import DataBase

class Objects(DataBase):
  def __init__(self):
    super(Objects, self).__init__()
    self.objects = self.db.objects

  def get_object(self, object_id):
    try:
      r = self.objects.find_one({"_id": ObjectId(object_id)})
    except Exception as e:
      print(e)

    return r

  def get_objects_with_null_index(self, version_id=None, offset=0, limit=50):
    query = {}

    if version_id is None:
      query = {"index":None, "feature": {"$ne":None}, "version_id": {"$ne":None}}
    else:
      query = {"index":None, "feature": {"$ne":None}, "version_id":version_id}

    try:
      r = self.objects.find(query).skip(offset).limit(limit)
    except Exception as e:
      print(e)

    return list(r)

  def add_object(self, object):
    object_id = None
    try:
      r = self.objects.update_one({"name": object['name']},
                                  {"$set": object},
                                  upsert=True)
    except Exception as e:
      print(e)

    if 'upserted' in r.raw_result:
      object_id = str(r.raw_result['upserted'])

    return object_id

  def update_object(self, object):
    try:
      r = self.objects.update_one({"name": object['name']},
                                  {"$set": object})
    except Exception as e:
      print(e)
      return None

    return r.raw_result

  def update_objects(self, objects):
    try:
      bulk = self.objects.initialize_unordered_bulk_op()
      for i in range(0, len(objects)):
        bulk.find({'name': objects[i]['name']}).update({'$set': objects[i]})
      r = bulk.execute()
      print(r)
    except Exception as e:
      print(e)

  def reset_index(self, version_id=None):
    query = {}
    obj = {"index": None}

    if version_id is None:
      query = {"index":{"$ne":None}, "version_id": {"$ne":None}}
    else:
      query = {"index":{"$ne":None}, "version_id":version_id}
    try:
      r = self.objects.update_many(query, {"$set":obj})
      print(r)
    except Exception as e:
      print(e)
