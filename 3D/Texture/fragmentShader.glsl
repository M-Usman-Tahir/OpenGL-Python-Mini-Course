#version 330 core
in vec2 frag_texcoord;  // Receive color from vertex shader
out vec4 out_color;

uniform sampler2D texture_sampler;

void main()
{
    out_color = texture(texture_sampler, frag_texcoord);  // Use the received color for the fragment
}
