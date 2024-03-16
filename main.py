import os

class Note():
  def __init__(self, fileName):
    self.contents = ""
    self.fileName = fileName

  def edit(self, contents):
    self.contents = contents

  def save(self):
    f = open(self.fileName, "w")
    f.write(self.contents)
    f.close()

  def saveAs(self, fileName):
    self.fileName = fileName
    self.save()

  def load(self):
    f = open(self.fileName, "r")
    self.contents = f.read()
    f.close()

class NoteManager:
  def __init__(self):
    configFile = ".notes"
    notes = []
    if os.path.isfile(configFile):
      f = open(configFile, "r")
      for line in f:
        line = line.strip('\n')
        note = Note(line)
        note.load()
        notes.append(note)
      f.close()
    else:
      f = open(configFile, "x")
      f.close()

    self.notes = notes
    self.configFile = configFile

  def addToConfig(self, note):
    f = open(self.configFile, "a")
    f.write(f'{note.fileName}\n')
    f.close()

  def newNote(self, fileName, contents):
    note = Note(fileName)
    note.edit(contents)
    note.save()
    self.notes.append(note)
    self.addToConfig(note)
    
  def editNote(self, fileName, newContents):
    note = next(filter(lambda note: note.fileName == fileName, self.notes))
    note.edit(newContents)
    note.save()

def main():
  manage = NoteManager()
  manage.newNote("note1.txt", "hi")

main()
