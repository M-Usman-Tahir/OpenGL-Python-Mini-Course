#version 330 core
in vec3 in_position;
in vec2 in_tex_cord;
uniform mat4 transform;
out vec2 frag_texcoord;
void main()
{
    gl_Position = transform * vec4(in_position, 1.0);
    frag_texcoord = in_tex_cord;
}