#version 330 core

out vec4 FragColor;
in vec3 newColor;
in vec4 FragPos;

uniform vec3 lightPos = vec3(0, 0, 3);
uniform vec3 lightColor = vec3(1.0,1.0,1.0);

void main()
{
  vec3 position = vec3(FragPos.x, FragPos.y, FragPos.z);
  vec3 norm = normalize(position);
  vec3 lightDir = normalize(lightPos - position);  

  float diff = max(dot(norm, lightDir), 0.0);
  vec3 diffuse = diff * lightColor;

  FragColor = vec4(diffuse * newColor, 1.0);
}
