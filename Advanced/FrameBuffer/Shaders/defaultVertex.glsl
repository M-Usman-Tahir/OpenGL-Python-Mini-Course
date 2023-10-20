#version 330 core
layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;
layout(location = 2) in vec3 in_color;

uniform mat4 VP;
uniform mat4 M;

out vec3 frag_color;
out vec3 frag_pos;
out vec3 normal;

void main()
{   
    gl_Position = VP* M* vec4(in_position, 1.0);
    frag_color = in_color;
    frag_pos = vec3(M*vec4(in_position, 1.0));
    normal = mat3(M) * normalize(in_normal);
}