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

