#version 330 core

out vec4 FragColor;
in vec3 newColor;
in vec4 FragPos;

uniform vec3 viewPos = vec3(0,0,1);
uniform float specularStrength = 0.5;
uniform vec3 lightPos = vec3(-.5, .1, .3);
uniform vec3 lightColor = vec3(1.0,1.0,1.0);

void main()
{
  vec3 position = vec3(FragPos.x, FragPos.y, FragPos.z)
  vec3 norm = normalize(position);
  vec3 lightDir = normalize(ligthPos - position);  

  vec3 viewDir = normalize(viewPos - position);
  vec3 reflectDir = reflect(-lightDir, norm);

  float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
  vec3 specular = specularStrength * spec * lightColor;  

  FragColor = vec4(specular * newColor, 1.0);
}
