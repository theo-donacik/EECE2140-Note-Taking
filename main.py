class Note():
  def __init__(self):
    self.contents = ""
    self.fileName = ""

  def edit(self, contents):
    self.contents = contents

  def save(self):
    f = open(self.fileName, "w")
    f.write(self.contents)
    f.close()

  def saveAs(self, fileName):
    self.fileName = fileName
    self.save()

def main():
  return

main()
