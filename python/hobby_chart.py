'''
Some interesting chart
'''

import numpy as np
from PIL import Image

def line(imgsize):
  img = np.zeros((imgsize,imgsize,3))
  i = 0
  for line in img:
      j = 0
      for pexil in line:
          if i == imgsize/2 :
              pexil[0] = 0
              pexil[1] = 255
              pexil[2] = 0
          j+=1
      i+=1
  Image.fromarray(np.uint8(img)).show()

def r_and_g(imgsize):
  img = np.zeros((imgsize,imgsize,3))
  i = 0
  for line in img:
      j = 0
      for pexil in line:
          pexil[0] = i * 255 / imgsize 
          pexil[1] = j * 255 / imgsize
          pexil[2] = 0
          j+=1
      i+=1
  Image.fromarray(np.uint8(img)).show()

def blue(imgsize):
  img = np.zeros((imgsize,imgsize,3))
  i = imgsize
  for line in img:
      j = 0 
      for pexil in line:
          pexil[0] = 0
          pexil[1] = 0
          pexil[2] = (i + j) * 255 / imgsize / 2
          j+=1
      i-=1
  Image.fromarray(np.uint8(img)).show()

def circle(imgsize):
  img = np.zeros((imgsize,imgsize,3))
  i = 0.0
  for line in img:
      j = 0.0
      for pexil in line:
          if ((i-imgsize/2)/(imgsize/2))**2+((j-imgsize/2)/(imgsize/2))**2 < 1 :
              pexil[0] = (((i-imgsize/2)/(imgsize/2))**2+((j-imgsize/2)/(imgsize/2))**2)*255
              pexil[1] = (((i-imgsize/2)/(imgsize/2))**2+((j-imgsize/2)/(imgsize/2))**2)*255
              pexil[2] = (((i-imgsize/2)/(imgsize/2))**2+((j-imgsize/2)/(imgsize/2))**2)*255
          if (i == imgsize / 2) or (j == imgsize / 2):
              pexil[0] = 255
              pexil[1] = 255
              pexil[2] = 255
          j+=1
      i+=1
  Image.fromarray(np.uint8(img)).show()

###
# x**2 + (y - (x**2)**(1.0/3))**2 = 1
###
def heart(imgsize):
  img = np.zeros((imgsize,imgsize,3))
  i = 0.0
  for line in img:
      j = 0.0
      for pexil in line:
          x = (j-imgsize/2)/(imgsize/4)
          y = -(i-imgsize/2)/(imgsize/4)
          if (x**2 + (y - (x**2)**(1.0/3))**2) < 1 :
              pexil[0] = 255
              pexil[1] = 255 - 255 * (x**2 + (y - (x**2)**(1.0/3))**2)
              pexil[2] = 255
          j+=1
      i+=1
  Image.fromarray(np.uint8(img)).show()

def heart_1(imgsize):
  img = np.zeros((imgsize,imgsize,3))
  i = 0.0
  for line in img:
      j = 0.0
      for pexil in line:
          x = (j-imgsize/2)/(imgsize/4)
          y = -(i-imgsize/2)/(imgsize/4)
          if (x**2 + (y - (x**2)**(1.0/3))**2) < 1 :
              pexil[0] = 255
              pexil[1] = 1 - 255 * (x**2 + (y - (x**2)**(1.0/3))**2)
              pexil[2] = 255
          j+=1
      i+=1
  Image.fromarray(np.uint8(img)).show()

def heart_2(imgsize):
  img = np.zeros((imgsize,imgsize,3))
  i = 0.0
  for line in img:
      j = 0.0
      for pexil in line:
          x = (j-imgsize/2)/(imgsize/10)
          y = -(i-imgsize/2)/(imgsize/10)
          pexil[0] = 255
          pexil[1] = 255 - 255 * (x**2 + (y - (x**2)**(1.0/3))**2)
          pexil[2] = 255
          j+=1
      i+=1
  Image.fromarray(np.uint8(img)).show()
  #Image.fromarray(np.uint8(img*255)).save('heart.png')

###
# (x**2 + y**2 - 1)**3 - x**2 * y**3 = 0
# == x**2 + y**2 - (x**2 * y**3)**(1.0/3) = 1
###
def heart_3(imgsize):
  img = np.zeros((imgsize,imgsize,3))
  i = 0.0
  for line in img:
      j = 0.0
      for pexil in line:
          x = (j-imgsize/2)/(imgsize/10)
          y = -(i-imgsize/2)/(imgsize/10)
          pexil[0] = 255
          pexil[1] = 16 - 255 * (x**2 + y**2 - (x**2)**(1.0/3) * y)
          pexil[2] = 255
          j+=1
      i+=1
  Image.fromarray(np.uint8(img)).show()
  #Image.fromarray(np.uint8(img*255)).save('heart_3.png')

if __name__ == '__main__':
  #line(imgsize=1024)
  #r_and_g(1024)
  #blue(1024)
  #circle(1024)
  heart_3(1024)
