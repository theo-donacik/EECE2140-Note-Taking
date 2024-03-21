import os
import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib

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

class NoteWindow(Gtk.ApplicationWindow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.set_default_size(800, 600)
    self.set_title("Notes")

    # Header Bar
    self.header = Gtk.HeaderBar()
    self.set_titlebar(self.header)

    # Open file button
    self.open_dialog = Gtk.FileDialog.new()
    self.open_dialog.set_title("Select a File")
    self.open_button = Gtk.Button(label="Open")
    self.header.pack_start(self.open_button)
    self.open_button.connect('clicked', self.show_open_dialog)

    # Main box layout
    self.box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    self.box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    self.set_child(self.box1)
    self.box1.append(self.box2)  
    self.box1.append(self.box3)

    self.button = Gtk.Button(label="Hello")
    self.button.connect('clicked', self.hello)
    self.box2.append(self.button)

    # Text Box
    self.text = Gtk.TextView.new()
    self.text.set_hexpand(True)
    self.text.set_vexpand(True)

    self.textbuffer = self.text.get_buffer()
    self.textbuffer.set_text("Hi")

    self.box3.append(self.text)
    

  def hello(self, button):
    print(self.textbuffer.get_text(self.textbuffer.get_bounds().start, self.textbuffer.get_bounds().end, False))

  def show_open_dialog(self, button):
    self.open_dialog.open(self, None, self.open_dialog_open_callback)
        
  def open_dialog_open_callback(self, dialog, result):
      try:
          file = dialog.open_finish(result)
          if file is not None:
              print(f"File path is {file.get_path()}")
              # Handle loading file from here
      except GLib.Error as error:
          print(f"Error opening file: {error.message}")

class NoteAppWindow(Adw.Application):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.connect('activate', self.on_activate)

    self.manage = NoteManager()

  def on_activate(self, app):
    self.win = NoteWindow(application=app)
    self.win.present()

def main():
  app = NoteAppWindow(application_id="com.theo.NoteApp")
  app.run(sys.argv)

main()
