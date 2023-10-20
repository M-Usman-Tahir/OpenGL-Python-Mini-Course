#version 330 core
layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_color;

uniform mat4 M;
uniform mat4 VP;

out vec3 frag_color;

void main()
{   
    gl_Position = VP*M*vec4(in_position, 1.0);
    frag_color = in_color;
}