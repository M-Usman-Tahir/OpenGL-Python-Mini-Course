#version 330 core
in vec3 in_position;
uniform mat4 transform;
uniform vec3 color;
out vec3 frag_color;
void main()
{
    gl_Position = transform * vec4(in_position, 1.0);
    frag_color = color;
}