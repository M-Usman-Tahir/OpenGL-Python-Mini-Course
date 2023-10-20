#version 330
in vec2 outText;

out vec4 outColor;
uniform sampler2D tex_sampler;

void main()
{
    outColor = texture(tex_sampler, outText);
}