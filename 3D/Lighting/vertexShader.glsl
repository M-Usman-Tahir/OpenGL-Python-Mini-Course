#version 330 core
in vec3 in_position;
in vec3 in_color;
uniform mat4 MVP;
out vec3 frag_color;
void main()
{
    gl_Position = MVP * vec4(in_position, 1.0);
    frag_color = in_color;
}