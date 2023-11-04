import sys
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
from OpenGL.GLUT import *
from math import sin, cos, tan, radians


vertex_code = """
#version 330 core
layout(location = 0) in vec3 vertexPosition;
uniform mat4 rotation;
uniform mat4 model;
uniform mat4 projection;

void main(){
  gl_Position = projection * rotation * model * vec4(vertexPosition, 1.0);
}
"""

fragment_code = '''
#version 330 core
out vec4 color;

void main(){
  color = vec4(1,0,0,1);//define color as red (RGB)
}
'''

vertices = np.array([
  [ 0.0, 1.0, 0.0],
  [ 1.0, -1.0, 0.0],
  [ -1.0, -1.0, 0.0]], dtype='f')


def init():
  global shaderProgram
  global vao
  global vbo

  glClearColor(0, 0, 0, 0)


  # compile shaders and program
  vertexShader = shaders.compileShader(vertex_code, GL_VERTEX_SHADER)
  fragmentShader = shaders.compileShader(fragment_code, GL_FRAGMENT_SHADER)
  shaderProgram = shaders.compileProgram(vertexShader, fragmentShader)

  vao = glGenVertexArrays(1)
  glBindVertexArray(vao)

  vbo = glGenBuffers(1)
  glBindBuffer(GL_ARRAY_BUFFER, vbo)

  glBindBuffer(GL_ARRAY_BUFFER, vbo)
  glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

  stride = 3 * vertices.itemsize
  position_offset = ctypes.c_void_p(0)
  glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, position_offset)
  glEnableVertexAttribArray(0)

def display():
  global shaderProgram
  global vao
  global width
  global height

  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  # load everthing back
  glUseProgram(shaderProgram)
  glBindVertexArray(vao)

  glBindBuffer(GL_ARRAY_BUFFER, vbo)
  glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

  time = glutGet(GLUT_ELAPSED_TIME) / 1000

  models = [
    np.array([[0.25, 0.0, 0.0, 0.0],
              [0.0, 0.25, 0.0, 0.0],
              [0.0, 0.0, 1.0, 0.0],
              [0.6, 0.0, 0.0, 1.0]]),

    np.array([[0.25, 0.0, 0.0, 0.0],
              [0.0, 0.25, 0.0, 0.0],
              [0.0, 0.0, 1.0, 0.0],
              [0.0, 0.0, 0.0, 1.0]]),

    np.array([[0.25, 0.0, 0.0, 0.0],
              [0.0, 0.25, 0.0, 0.0],
              [0.0, 0.0, 1.0, 0.0],
              [-0.6, 0.0, 0.0, 1.0]]),
  ]

  rotations = [
    [
      [cos(time), 0.0, -sin(time), 0.0],
      [0.0, 1.0, 0.0, 0.0],
      [sin(time), 0.0, cos(time), 0.0],
      [0.0, 0.0, -3.0, 1.0]
    ],

    [
      [cos(time), 0.0, sin(time), 0.0],
      [0.0, 1.0, 0.0, 0.0],
      [-sin(time), 0.0, cos(time), 0.0],
      [0.0, 0.0, -3.0, 1.0]
    ],
    [
      [1.0, 0.0, 0.0, 0.0],
      [0.0, 1.0, 0.0, 0.0],
      [0.0, 0.0, 1.0, 0.0],
      [0.0, 0.0, -3.0, 1.0]
    ],
  ]

  aspect_ratio = width / height
  near = 0.1
  far = 100.0
  fov = 45.0

  top = near * tan(radians(fov) / 2.0)
  right = top * aspect_ratio

  projection = ([near / right, 0.0, 0.0, 0.0],
              [0.0, near / top, 0.0, 0.0],
              [0.0, 0.0, -(far + near) / (far - near), -1.0],
              [0.0, 0.0, -(2 * far * near) / (far - near), 0.0])

  projection_loc = glGetUniformLocation(shaderProgram, "projection")
  glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection)

  for idx, model in enumerate(models):
    model_loc = glGetUniformLocation(shaderProgram, "model")
    rotation_loc = glGetUniformLocation(shaderProgram, "rotation")

    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rotations[idx])

    glDrawArrays(GL_TRIANGLES, 0, 8)
    glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
    glBindAttribLocation(shaderProgram, 0, 'vertexPosition')
    glEnableVertexAttribArray(0)


  glBindBuffer(GL_ARRAY_BUFFER, 0)
  glBindVertexArray(0)

  #clean things up
  glBindBuffer(GL_ARRAY_BUFFER, 0)
  glBindVertexArray(0)
  glUseProgram(0)

  glutSwapBuffers()

def reshape(newWidth, newHeight):
  global width
  global height

  width = newWidth
  height = newHeight

  glViewport(0, 0, newWidth, newHeight)

if __name__ == '__main__':
  global width
  global height

  width = 640
  height = 640

  glutInit()
  glutInitContextVersion(3, 0)
  glutInitContextProfile(GLUT_CORE_PROFILE);
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

  glutInitWindowSize(width, height)

  glutCreateWindow(b'Hello world!')

  glutReshapeFunc(reshape)
  glutDisplayFunc(display)
  glutIdleFunc(display)

  init()

  glutMainLoop()
