#version 330 core
layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_color;  // New input attribute for colors

out vec3 frag_color;  // Pass color to fragment shader

uniform mat4 transform;

void main()
{
    gl_Position = transform * vec4(in_position, 1.0);
    frag_color = in_color;  // Pass the vertex color to the fragment shader
}
