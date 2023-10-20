#version 330 core
in vec3 frag_color;  
in vec3 frag_pos;
in vec3 normal;

out vec4 out_color;

uniform vec3 ambient;
uniform vec3 lightPos;
uniform vec3 lightInt;

void main()
{
    vec3 Normal = normalize(normal);
    vec3 lightDir = normalize(lightPos - frag_pos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 Diffuse = diff * lightInt;
    
    vec3 color =  (Diffuse + ambient) * frag_color;
    out_color = vec4(color, 1.0);  
}
