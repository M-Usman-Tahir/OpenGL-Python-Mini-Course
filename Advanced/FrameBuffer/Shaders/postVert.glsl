#version 330 core
layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;
layout(location = 2) in vec2 in_tex_coord;
// layout(location = 3) in int in_postFunc;

uniform mat4 VP;
uniform mat4 M;

out vec2 tex_coord;
out vec3 frag_pos;
out vec3 normal;
// out int postFunc;

void main()
{   
    gl_Position = VP* M* vec4(in_position, 1.0);
    tex_coord = in_tex_coord;
    frag_pos = vec3(M*vec4(in_position, 1.0));
    normal = mat3(M) * normalize(in_normal);
    // postFunc = in_postFunc;
}