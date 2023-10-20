#version 330
in layout(location = 0) vec3 in_position;
in layout(location = 1) vec2 in_tex_coord;

out vec2 outText;

void main()
{
    gl_Position =  vec4(in_position, 1.0);
    outText = in_tex_coord;
}