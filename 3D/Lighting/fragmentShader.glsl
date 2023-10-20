#version 330 core
in vec3 frag_color; 
out vec4 out_color;

uniform vec3 ambient;

void main()
{
    vec3 color = ambient * frag_color;
    out_color = vec4(color, 1.0); 
}
