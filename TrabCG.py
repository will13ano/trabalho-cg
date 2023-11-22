import sys
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
from OpenGL.GLUT import *
from math import sin, cos, tan, radians


vertex_code = '''
#version 330 core
in vec3 position;
in vec3 color;
out vec3 newColor;
uniform mat4 rotation;
uniform mat4 model;
uniform mat4 projection;

void main(){
  gl_Position = projection * model * rotation * vec4(position, 1.0);
  newColor = color;
}
'''

fragment_code = '''
#version 330 core
in vec3 newColor;
out vec4 color;

void main(){
  color = vec4(newColor, 1.0);
}
'''

vertices = np.array([
  # Vertices        Colors
  [-.5, -.5, -.5], [1, 0, 0],
  [.5, -.5, -.5], [0, 1, 0],
  [.5, .5, -.5], [0, 0, 1],
  [-.5, .5, -.5], [1, 1, 0],
  [-.5, -.5, .5], [0, 1, 1],
  [.5, -.5, .5], [1, 1, 1],
  [.5, .5, .5], [0.5, 0.5, 0.5],
  [-.5, .5, .5], [0.5, 0.5, 0.5],
], dtype=np.float32)

indices = np.array([
  0, 1, 2, 2, 3, 0,  # Front face
  1, 5, 6, 6, 2, 1,  # Right face
  5, 4, 7, 7, 6, 5,  # Back face
  4, 0, 3, 3, 7, 4,  # Left face
  3, 2, 6, 6, 7, 3,  # Top face
  4, 5, 1, 1, 0, 4,  # Bottom face
], dtype=np.uint32)



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

  # Create Vertex Buffer Object (VBO) and Element Buffer Object (EBO)
  vbo = glGenBuffers(1)
  glBindBuffer(GL_ARRAY_BUFFER, vbo)
  glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

  ebo = glGenBuffers(1)
  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
  glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

  # Set attribute pointers
  stride = 6 * vertices.itemsize
  position_offset = ctypes.c_void_p(0)
  color_offset = ctypes.c_void_p(3 * vertices.itemsize)
  glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, position_offset)
  glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, color_offset)
  glEnableVertexAttribArray(0)
  glEnableVertexAttribArray(1)
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
      [cos(time), 0.0, -sin(time), 0.0],
      [0.0, 1.0, 0.0, 0.0],
      [sin(time), 0.0, cos(time), 0.0],
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
  model_loc = glGetUniformLocation(shaderProgram, "model")
  rotation_loc = glGetUniformLocation(shaderProgram, "rotation")

  glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection)

  for idx, model in enumerate(models):
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rotations[idx])

    glBindVertexArray(vao)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

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