import os
import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio

class Note():
  def __init__(self, filePath):
    self.contents = ""
    self.filePath = filePath

  def edit(self, contents):
    self.contents = contents

  def save(self):
    f = open(self.filePath, "w")
    f.write(self.contents)
    f.close()

  def saveAs(self, filePath):
    self.filePath = filePath
    self.save()

  def load(self):
    f = open(self.filePath, "r")
    self.contents = f.read()
    f.close()


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

    # Save file button
    self.save_dialog = Gtk.FileDialog.new()
    self.save_dialog.set_title("Select a File") 
    self.button = Gtk.Button(label="Save As")
    self.button.connect('clicked', self.show_save_dialog)
    self.header.pack_start(self.button)

    # Main box layout
    self.box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    self.box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    self.set_child(self.box1)
    self.box1.append(self.box2)  
    self.box1.append(self.box3)

    # Text Box
    self.text = Gtk.TextView.new()
    self.text.set_hexpand(True)
    self.text.set_vexpand(True)

    self.textbuffer = self.text.get_buffer()
    self.textbuffer.set_text("Hi")

    self.box3.append(self.text)

  def get_current_buffer(self):
    bounds = self.textbuffer.get_bounds()
    return self.textbuffer.get_text(bounds.start, bounds.end, False)

  def show_open_dialog(self, button):
    self.open_dialog.open(self, None, self.load_selected_file)

  def show_save_dialog(self, button):
    self.save_dialog.set_initial_file(Gio.File.new_for_path(self.currentNote.filePath))
    self.save_dialog.save(self, None, self.save_selected_file)

  def load_selected_file(self, dialog, result):
    try:
      file = dialog.open_finish(result)
      if file is not None:
        print(f"File path is {file.get_path()}")
        self.currentNote = Note(file.get_path())
        self.currentNote.load()
        self.textbuffer.set_text(self.currentNote.contents)
    except GLib.Error as error:
      print(f"Error opening file: {error.message}")

  def save_selected_file(self, dialog, result):
    try:
      file = dialog.save_finish(result)
      if file is not None:
        print(f"File path is {file.get_path()}")
        self.currentNote.edit(self.get_current_buffer())
        self.currentNote.saveAs(file.get_path())
    except GLib.Error as error:
      print(f"Error opening file: {error.message}")


class NoteAppWindow(Adw.Application):
  def __init__(self):
    super().__init__()
    self.connect('activate', self.on_activate) 

  def on_activate(self, app):
    self.win = NoteWindow(application=app)
    self.win.present()

def main():
  app = NoteAppWindow()
  app.run(sys.argv)

main()
