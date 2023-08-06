from stylelens_object.database import DataBase

class Objects(DataBase):
  def __init__(self):
    super().__init__()
    self.objects = self.db.objects

  def add_object(self, object):
    try:
      r = self.objects.insert(object)
    except Exception as e:
      print(e)

    return str(r)

