#version 330 core
in vec3 in_position;
in vec3 in_normal;
in vec3 in_color;

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