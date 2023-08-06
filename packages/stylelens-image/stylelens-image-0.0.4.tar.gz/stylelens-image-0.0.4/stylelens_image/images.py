from stylelens_image.database import DataBase

class Images(DataBase):
  def __init__(self):
    super().__init__()
    self.images = self.db.images

  def add_image(self, image):
    try:
      r = self.images.insert(image)
    except Exception as e:
      print(e)

    return str(r)

  def get_images(self, version_id=None, offset=0, limit=50):
    query = {}
    if version_id is None:
      query = {}
    else:
      query = {"version_id": version_id}

    try:
      r = self.images.find(query).skip(offset).limit(limit)
    except Exception as e:
      print(e)

    return list(r)

  def delete_images(self, version_id, except_version=True):
    query = {}
    if except_version is True:
      query = {"version_id": {"$ne": version_id}}
    else:
      query = {"version_id": version_id}

    try:
      r = self.images.delete_many(query)
    except Exception as e:
      print(e)

    return r.raw_result
