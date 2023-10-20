#version 330
in layout(location = 0) vec3 position;
in layout(location = 1) vec2 textCoords;

out vec2 outText;

void main()
{
    gl_Position =  vec4(position, 1.0);
    outText = textCoords;
}