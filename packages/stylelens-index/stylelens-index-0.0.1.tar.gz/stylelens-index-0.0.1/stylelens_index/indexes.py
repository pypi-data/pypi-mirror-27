from stylelens_index.database import DataBase

class Indexes(DataBase):
  def __init__(self):
    super().__init__()
    self.indexes = self.db.indexes

  def add_index(self, index):
    try:
      r = self.indexes.insert(index)
    except Exception as e:
      print(e)

    return str(r)

