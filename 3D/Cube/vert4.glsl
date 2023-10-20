#version 330 core
in vec2 in_texture_coords;
in vec3 in_position;
out vec2 fragTextureCoords;

uniform mat4 transform;
uniform sampler2D texture_sampler;

void main()
{
    gl_Position = transform * vec4(in_position, 1.0);
    fragTextureCoords = in_texture_coords;
}
