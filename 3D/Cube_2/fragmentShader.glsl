#version 330 core
in vec3 frag_color;  // Receive color from vertex shader
out vec4 out_color;

void main()
{
    out_color = vec4(frag_color, 1.0);  // Use the received color for the fragment
}
