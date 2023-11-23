#version 330 core
in vec3 position;
in vec3 color;

out vec3 newColor;
out vec4 FragPos;

uniform mat4 rotation;
uniform mat4 model;
uniform mat4 projection;

void main(){
  gl_Position = projection * model * rotation * vec4(position, 1.0);
  newColor = color;
  
  FragPos = vec4(gl_Position);
}