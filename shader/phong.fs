#version 330 core

out vec4 FragColor;
in vec3 newColor;
in vec4 FragPos;

uniform vec3 lightPos = vec3(0, 0, 3);
uniform vec3 lightColor = vec3(1.0,1.0,1.0);
uniform float ambientStrength = 0.23;
uniform float specularStrength = 0.27;
uniform float diffuseStrength = 0.77;
uniform vec3 camPos = vec3(0,0,1);
uniform float n = 89;

void main() {
  vec3 position = vec3(FragPos.x, FragPos.y, FragPos.z);
  vec3 ambient = ambientStrength * lightColor; //cor da luz

  //Difusa
  vec3 normal = normalize(position);
  vec3 ligthDir = normalize(lightPos - position);
  float cosTeta = clamp(dot(normal,ligthDir),0.,1.);
  vec3 diffuse = lightColor*diffuseStrength*cosTeta;

  float dist = length(lightPos - position);
  float atenuacao = 1.0/(1+0.09*dist+0.032*dist*dist);

  //Especular
  vec3 reflex = 2*cosTeta*normal- normalize(lightPos);
  float cosAlfa = clamp(dot(camPos,reflex),0.,1.);
  vec3 specular = lightColor*specularStrength*pow(cosAlfa,n);

  //Combinação
  FragColor = vec4((ambient+diffuse+specular)*newColor, 1.0)*atenuacao;
}