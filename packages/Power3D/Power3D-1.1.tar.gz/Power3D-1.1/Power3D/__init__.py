import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
from PIL import Image
import numpy
import math

objects = []

class GameObject(object):
    def __init__(self, mdl, tex):
        self.model = mdl
        self.x=0
        self.y=0
        self.z=0
        self.xrot=0
        self.texture = tex

    def getModel(self):
        return self.model

def draw(theobject,x,y,z,tex):
    obj = theobject.getModel()
    glTranslate(x,y,z)
    i = 0
    while i < len(obj[1]):
        glBegin(GL_LINES)
        glColor3f(1.0,1.0,1.0)
        glVertex3fv(obj[0][obj[1][i][0]])
        glVertex3fv(obj[0][obj[1][i][1]])
        glEnd()
        i+=1
    i = 0
    while i < len(obj[2]):
        glBindTexture(GL_TEXTURE_2D, tex)
        glBegin(GL_QUADS)
        glTexCoord2f(0,0)
        glVertex3fv(obj[0][obj[2][i][0]])
        glTexCoord2f(1,0)
        glVertex3fv(obj[0][obj[2][i][1]])
        glTexCoord2f(1,1)
        glVertex3fv(obj[0][obj[2][i][2]])
        glTexCoord2f(0,1)
        glVertex3fv(obj[0][obj[2][i][3]])
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)
        i+=1
    glTranslate(-x,-y,-z)

global camerax
global cameray
global cameraz

camerax = 0
cameray = 0
cameraz = 6

camerarotx = 0
cameraroty = 0

def getCameraPos():
    return (camerax,cameray,cameraz)

def getCameraRot():
    return (camerarotx,cameraroty)

def loadTexture(filename):
      # PIL can open BMP, EPS, FIG, IM, JPEG, MSP, PCX, PNG, PPM
      # and other file types.  We convert into a texture using GL.
      print('trying to open', filename)
      try:
         image = Image.open(filename)
      except IOError as ex:
         print('IOError: failed to open texture file')
         message = template.format(type(ex).__name__, ex.args)
         print(message)
         return -1
      print('opened file: size=', image.size, 'format=', image.format)
      imageData = numpy.array(list(image.getdata()), numpy.uint8)

      textureID = glGenTextures(1)
      glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
      glBindTexture(GL_TEXTURE_2D, textureID)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
      glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1],
         0, GL_RGB, GL_UNSIGNED_BYTE, imageData)
      glBindTexture(GL_TEXTURE_2D, 0)

      image.close()
      return textureID

def cast(x,y):
    ret = []
    ret.append(math.cos(math.radians(y))*3)
    ret.append(math.sin(math.radians(x))*3)
    ret.append(math.sin(math.radians(y))*3)
    return ret

def drawScene():
    glPushMatrix()
    glLoadIdentity()

    lookat = cast(camerarotx,cameraroty)
    gluLookAt(camerax,cameray,cameraz,lookat[0]+camerax,lookat[1]+cameray,lookat[2]+cameraz,0,1,0)
    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    for obj in objects:
        draw(obj,obj.x,obj.y,obj.z,obj.texture)
    glPopMatrix()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.flip()
    pygame.time.wait(20)

def addToScene(obj):
    objects.append(obj)

def rotateCamera(xr,yr):
    global cameraroty
    global camerarotx
    cameraroty+=yr
    camerarotx+=xr

def moveCamera(xm, ym, zm):
    global camerax
    global cameray
    global cameraz
    camerax += xm
    cameray += ym
    cameraz += zm

def moveCameraCorrectly(xm,ym,zm):
    global camerax
    global cameray
    global cameraz
    cameraz+=zm*math.sin(math.radians(cameraroty))
    camerax+=zm*math.cos(math.radians(cameraroty))
    cameraz+=math.sin(math.radians(cameraroty+90))*xm
    camerax+=math.cos(math.radians(cameraroty+90))*xm
    cameray+=ym

def initGL():
    pygame.display.set_mode((500,400), DOUBLEBUF|OPENGL)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45,500/400,0.1,100.0)
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
