import sys
import os

try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
import pygubu
from PIL import ImageTk, Image
import tkMessageBox
import bpcs
import subprocess as cmd
from datetime import datetime
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_psnr, compare_mse
import cv2
import __builtin__
# from sewar.full_ref import mse, psnr

class Application:
  def __init__(self, master):
    self.builder = builder = pygubu.Builder()
    builder.add_from_file('main.ui')
    self.mainwindow = builder.get_object('scr_main', master)
    callbacks = {
      'btn_embed': btn_embed,
      'btn_decode': btn_decode,
      'btn_calculate': btn_calculate,
    }

    builder.connect_callbacks(callbacks)
    builder.connect_callbacks(self)

class Embed:
  def __init__(self, master):
    self.builder = builder = pygubu.Builder()
    builder.add_from_file('embed.ui')
    self.mainwindow = builder.get_object('scr_embed', master)
    self.imgepath = builder.get_object('path_image')
    self.filepath = builder.get_object('path_file_txt')
    
    callbacks = {
      'btn_embed': btn_embed,
      'btn_decode': btn_decode,
      'btn_calculate': btn_calculate,
    }

    builder.connect_callbacks(callbacks)
    builder.connect_callbacks(self)

    size = 300, 300

    img = Image.open('noImage.gif')
    img.thumbnail(size, Image.ANTIALIAS)

    self.img_label = builder.get_object('lbl_image', master)
    self.img_label.new_image = ImageTk.PhotoImage(img)
    self.img_label.config(image=self.img_label.new_image)

  def on_image(self, event=None):
    path = self.imgepath.cget('path')
    size = 300, 300

    img = Image.open(path)
    img.thumbnail(size, Image.ANTIALIAS)

    self.img_label.new_image = ImageTk.PhotoImage(img)
    self.img_label.config(image=self.img_label.new_image)
    tkMessageBox.showinfo('You choosed:', path)

  def on_file(self, event=None):
    path = self.filepath.cget('path')
    tkMessageBox.showinfo('You choosed:', path)

  def btn_process(self, event=None):
    now = datetime.now()
    current_time = now.strftime("%dd%M%Y%H%M%S")
    entry = self.builder.get_object('txt_alpha')
    vessel = self.imgepath.cget('path')
    file = self.filepath.cget('path')
    encfile = 'encoded/encoded_' + current_time + '.png'
    alpha = entry.get()

    if not vessel:
      tkMessageBox.showinfo('Warn: ', 'Fill Image input')
    elif not file:
      tkMessageBox.showinfo('Warn: ', 'Fill message input')
    elif not alpha:
      tkMessageBox.showinfo('Warn: ', 'Fill alpha input')
    else:
      bpcs.encode(vessel, file, encfile, float(alpha)) # embed msgfile in vslfile, write to encfile
  
  def btn_calculate(self, event=None):
    vessel = self.imgepath.cget('path')
    txt_alpha = self.builder.get_object('txt_alpha')
    txt_byte = self.builder.get_variable('byte_val')
    alpha = txt_alpha.get()

    if not vessel:
      tkMessageBox.showinfo('Warn: ', 'Fill Image input')
    elif not alpha:
      tkMessageBox.showinfo('Warn: ', 'Fill alpha input')
    else:
      cpt = bpcs.capacity(vessel, 'tmp', float(alpha))
      txt_byte.set(__builtin__.byte_val)
      tkMessageBox.showinfo('Info ', 'Job done')

  # def on_btn_embed(self, event=None):
    # hide_frame()
    # btn_embed()
    # print('embed btn')

  def on_btn_decode(self, event=None):
    btn_decode()
    print('embed decode')

  def on_btn_msepsnr(self, event=None):
    btn_calculate()
    print('embed mse psnr')

class Decode:
  def __init__(self, master):
    self.builder = builder = pygubu.Builder()
    builder.add_from_file('decode.ui')
    self.mainwindow = builder.get_object('scr_decode', master)
    self.imgepath = builder.get_object('path_image')
    callbacks = {
      'btn_embed': btn_embed,
      'btn_decode': btn_decode,
      'btn_calculate': btn_calculate,
    }

    size = 300, 300

    img = Image.open('noImage.gif')
    img.thumbnail(size, Image.ANTIALIAS)

    builder.connect_callbacks(callbacks)
    builder.connect_callbacks(self)
    self.img_label = builder.get_object('lbl_image', master)
    self.img_label.new_image = ImageTk.PhotoImage(img)
    self.img_label.config(image=self.img_label.new_image)

  def path_image(self, event=None):
    path = self.imgepath.cget('path')
    size = 300, 300
    img = Image.open(path)
    img.thumbnail(size, Image.ANTIALIAS)

    self.img_label.new_image = ImageTk.PhotoImage(img)
    self.img_label.config(image=self.img_label.new_image)
    tkMessageBox.showinfo('You choosed:', path)

  def btn_process(self, event=None):
    vessel = self.imgepath.cget('path')
    txt_alpha = self.builder.get_object('txt_alpha')
    alpha = txt_alpha.get()
    now = datetime.now()
    current_time = now.strftime("%dd%M%Y%H%M%S")
    msgfile_decoded = 'decoded/decoded_' + current_time + '_tmp.txt'

    if not vessel:
      tkMessageBox.showinfo('Warn: ', 'Fill Image input')
    elif not alpha:
      tkMessageBox.showinfo('Warn: ', 'Fill alpha input')
    else:
      bpcs.decode(vessel, msgfile_decoded, float(alpha))
      tkMessageBox.showinfo('Info ', 'Job done')

  def on_embed(self, event=None):
    hide_frame()
    btn_embed()
    print('embed btn')

  # def on_decode(self, event=None):
  #   btn_decode()
  #   print('embed decode')

  def on_msepsnr(self, event=None):
    btn_calculate()
    print('embed mse psnr')

class Calculate:
  def __init__(self, master):
    self.builder = builder = pygubu.Builder()
    builder.add_from_file('calculate.ui')
    self.mainwindow = builder.get_object('scr_calculate', master)
    self.img_cover = builder.get_object('path_cover')
    self.img_stego = builder.get_object('path_stego')


    callbacks = {
      'btn_embed': btn_embed,
      'btn_decode': btn_decode,
      'btn_calculate': btn_calculate,
    }

    builder.connect_callbacks(callbacks)
    builder.connect_callbacks(self)
    self.img_label_1 = builder.get_object('lbl_image_1', master)
    self.img_label_2 = builder.get_object('lbl_image_2', master)
    self.img_label_1.new_image = ImageTk.PhotoImage(file='noImage.gif')
    self.img_label_1.config(image=self.img_label_1.new_image)
    self.img_label_2.new_image = ImageTk.PhotoImage(file='noImage.gif')
    self.img_label_2.config(image=self.img_label_2.new_image)
  
  def btn_process(self, event=None):
    origin = self.img_cover.cget('path')
    encode = self.img_stego.cget('path')
    txt_mse = self.builder.get_variable('val_mse')
    txt_psnr = self.builder.get_variable('val_psnr')
    # im_origin = Image.open(origin, 'r')
    # im_encode = Image.open(encode, 'r')
    # raw_origin = list(im_origin.getdata())
    # raw_encode = list(im_origin.getdata())
    # matrix_origin = [x for sets in raw_origin for x in sets]
    # matrix_encode = [x for sets in raw_encode for x in sets]
    # cnt_origin = get_rgbycbcr(im_origin)
    # cnt_encode = get_rgbycbcr(im_encode)
    ref_img = cv2.imread(origin)
    noisy_img = cv2.imread(encode)
    MSE = compare_mse(ref_img, noisy_img)
    PSNR = compare_psnr(ref_img, noisy_img)
    txt_mse.set(round(MSE, 2))
    txt_psnr.set(round(PSNR, 2))
    # print('PSNR : '+ repr(PSNR))
    # print('MSE : '+ repr(MSE))
    # print(cnt_encode)

  def path_cover(self, event=None):
    size = 300, 300
    path = self.img_cover.cget('path')
    img = Image.open(path)
    img.thumbnail(size, Image.ANTIALIAS)
    self.img_label_1.new_image = ImageTk.PhotoImage(img)
    self.img_label_1.config(image=self.img_label_1.new_image)

  def path_stego(self, event=None):
    size = 300, 300
    path = self.img_stego.cget('path')
    img = Image.open(path)
    img.thumbnail(size, Image.ANTIALIAS)
    self.img_label_2.new_image = ImageTk.PhotoImage(img)
    self.img_label_2.config(image=self.img_label_2.new_image)

  def on_embed(self, event=None):
    hide_frame()
    btn_embed()
    print('embed btn')

  def on_decode(self, event=None):
    btn_decode()
    print('embed decode')

  # def on_msepsnr(self, event=None):
  #   btn_calculate()
  #   print('embed mse psnr')

### custom build
# def rgb_calc(ref_file):
#   img = Image.open(ref_file)
#   width, height = img.size
#   print(width)
#   print(height)
#   rgb_dict = {}
#   rgb = img.load()
#   for x in range(width):
#     for y in range(height):
#       r, g, b = rgb[x, y]
#       lum = 0.299 * r + 0.587 * g + 0.114 * b
#       cb = 128 - 0.168736 * r - 0.331264 * g + 0.5 * b
#       cr = 128 + 0.5 * r - 0.418688 * g - 0.081312 * b
#       rgb_dict[(x, y)] = (r, g, b, lum, cb, cr)
#   return rgb_dict

def get_rgbycbcr(img):
  R, G, B = np.array(img).transpose(2, 0, 1)[:3]  # ignore alpha if present
  Y = 0.299 * R + 0.587 * G + 0.114 * B
  Cb = 128 - 0.168736 * R - 0.331264 * G + 0.5 * B
  Cr = 128 + 0.5 * R - 0.418688 * G - 0.081312 * B
  return np.array([R, G, B, Y, Cb, Cr], dtype=float).transpose(2, 1, 0)

# define btn_process action
def btn_embed():
  root = tk.Toplevel()
  app = Embed(root)
  root.mainloop()

def btn_decode():
  root = tk.Toplevel()
  app = Decode(root)
  root.mainloop()

def btn_calculate():
  root = tk.Toplevel()
  app = Calculate(root)
  root.mainloop()

def hide_frame():
  root = tk.Toplevel()
  app = Embed(root)
  app.hide()

if __name__ == '__main__':
  root = tk.Tk()
  app = Application(root)
  root.mainloop()