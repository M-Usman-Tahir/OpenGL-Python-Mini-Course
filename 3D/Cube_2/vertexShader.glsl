#version 330 core
in vec3 in_position;
in vec3 in_color;
uniform mat4 transform;
out vec3 frag_color;
void main()
{
    gl_Position = transform * vec4(in_position, 1.0);
    frag_color = in_color;
}