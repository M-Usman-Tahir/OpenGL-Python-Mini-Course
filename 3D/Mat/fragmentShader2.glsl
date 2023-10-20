#version 330 core
in vec2 tex_coord;  // Receive color from vertex shader
in vec3 frag_pos;
in vec3 normal;

out vec4 out_color;

uniform vec3 lightPos;
uniform vec3 camPos;
uniform vec3 lightInt;
uniform vec3 specInt;
uniform vec3 ambient;
uniform int r_Spec;

uniform sampler2D tex_sampler;

void main()
{
    vec3 Normal = normalize(normal);
    vec3 lightDir = normalize(lightPos- frag_pos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * lightInt;

    vec3 viewDir = normalize(camPos-frag_pos);
    vec3 reflectedDir = reflect(-lightDir, Normal);
    float spec = pow(max(0, dot(viewDir, reflectedDir)), r_Spec);
    vec3 specular = spec * specInt;

    vec3 texColor = texture(tex_sampler, tex_coord).xyz; 

    vec3 color = (specular + diffuse + ambient) * texColor; 
    out_color = vec4(color, 1.0);
}
