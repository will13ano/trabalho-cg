#version 330 core

out vec4 FragColor;
in vec3 newColor;
in vec4 FragPos;

uniform vec3 lightColor = vec3(1.0,1.0,1.0); //luz branca
uniform float ambientStrength = .5;

void main()
{
  vec3 ambient = ambientStrength * lightColor;

  FragColor = vec4(ambient * newColor, 1.0);
}
