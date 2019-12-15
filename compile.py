try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
import pygubu
from PIL import ImageTk
import tkMessageBox
import bpcs

imgfile = list()
txtfile = list()
val_alpha = list()

class Application:
    
    def __init__(self, master):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('main.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('mainwindow', master)
        self.imgepath = builder.get_object('img_path')
        self.filepath = builder.get_object('file_path')
        self.txt_alpha = builder.get_object('txt_alpha')
        
        # Configure callbacks
        callbacks = {
          'on_process_clicked': on_process_clicked,
          'on_clear_clicked': on_clear_clicked,
        }

        builder.connect_callbacks(callbacks)
        builder.connect_callbacks(self)
        
        # Configure image lable
        self.img_label = builder.get_object('lbl_image', master)
        self.img_label.new_image = ImageTk.PhotoImage(file='noImage.gif')
        self.img_label.config(image=self.img_label.new_image)
        
    def on_image_change(self, event=None):
        path = self.imgepath.cget('path')
        # print(self.txt_alpha.get())
        imgfile.append(path)
        val_alpha.append(float(self.txt_alpha.get()))
        self.img_label.new_image = ImageTk.PhotoImage(file=path)
        self.img_label.config(image=self.img_label.new_image)
        tkMessageBox.showinfo('You choosed:', path)
    
    def on_file_change(self, event=None):
        path = self.filepath.cget('path')
        txtfile.append(path)
        tkMessageBox.showinfo('You choosed:', path)

# define btn_process action
def on_process_clicked():
  init_bpcs()
  tkMessageBox.showinfo('Message', 'Job done!')

def on_clear_clicked():
  imgfile = []
  txtfile = []
  val_alpha = []

def init_bpcs():
  from datetime import datetime
  now = datetime.now()
  current_time = now.strftime("%dd%M%Y%H%M%S")
  # print('alpha value = '+val_alpha[0])
  # print('image file = '+imgfile[0])
  # print('txt path = '+txtfile[0])
  
  alpha = val_alpha[0]
  vslfile = imgfile[0]
  msgfile = txtfile[0]
  encfile = 'outputfile/encoded_' + current_time + '_.png'
  msgfile_decoded = 'outputfile/msg_decoded_' + current_time + '_tmp.txt'

  bpcs.capacity(vslfile, 'alpha', alpha) # check max size of message you can embed in vslfile
  bpcs.encode(vslfile, msgfile, encfile, alpha) # embed msgfile in vslfile, write to encfile
  bpcs.decode(encfile, msgfile_decoded, alpha) # recover message from encfile

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()