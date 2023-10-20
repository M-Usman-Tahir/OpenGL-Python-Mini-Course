#version 330 core

in vec2 tex_coord;
in vec3 frag_pos;
in vec3 normal;
// in int postFunc;

out vec4 out_color;

uniform vec3 lightPos;
uniform vec3 camPos;
uniform vec3 lightInt;
uniform vec3 diffuseInt;
uniform vec3 specInt;
uniform vec3 ambient;

uniform sampler2D tex_sampler;

const float offset = 1.0 / 300.0;
const vec2[] offsets = vec2[](
    vec2(-offset,  offset), // top-left
    vec2( 0.0,    offset), // top-center
    vec2( offset,  offset), // top-right
    vec2(-offset,  0.0),   // center-left
    vec2( 0.0,    0.0),   // center-center
    vec2( offset,  0.0),   // center-right
    vec2(-offset, -offset), // bottom-left
    vec2( 0.0,   -offset), // bottom-center
    vec2( offset, -offset)  // bottom-right    
);

const float sobel_dx_kernel[9] = float[](
    1, 0, -1,
    2, 0, -2,
    1, 0, -1
);

const float sobel_dy_kernel[9] = float[](
     1,  2,  1,
     0,  0,  0,
    -1, -2, -1
);

const float gauss_blur_kernel[9] = float[](
    1.0 / 16.0, 2.0 / 16.0, 1.0 / 16.0,
    2.0 / 16.0, 4.0 / 16.0, 2.0 / 16.0,
    1.0 / 16.0, 2.0 / 16.0, 1.0 / 16.0
);

vec4 Monochrome(vec3 tintColor) {
    vec4 color = texture(tex_sampler, tex_coord);
    float average = 0.299*color.r + 0.587*color.g + 0.114*color.b;
    return vec4(tintColor * vec3(average), 1.0);
}

vec4 Edge(vec3 tintColor) {

    vec3 dx = vec3(0);
    vec3 dy = vec3(0);
    for(int i = 0; i < 9; i++)
    {
        dx += sobel_dx_kernel[i] * vec3(texture(tex_sampler, tex_coord.st + offsets[i]));
        dy += sobel_dy_kernel[i] * vec3(texture(tex_sampler, tex_coord.st + offsets[i]));
    }

    float r = sqrt(dx.r * dx.r + dy.r * dy.r);
    float g = sqrt(dx.g * dx.g + dy.g * dy.g);
    float b = sqrt(dx.b * dx.b + dy.b * dy.b);
    
    return vec4(tintColor * vec3(r, g, b), 1.0);
}

vec4 Blur(vec3 tintColor) {

    vec3 color = vec3(0);

    for(int i = 0; i < 9; i++)
    {
        color += gauss_blur_kernel[i] * vec3(texture(tex_sampler, tex_coord.st + offsets[i]));
    }
    
    return vec4(tintColor * color, 1.0);
}

vec4 Identity() {
    return texture(tex_sampler, tex_coord);
}

vec3 getAmbient(){
    return ambient;
}

vec3 getDiffuse(){
    vec3 Normal = normalize(normal);
    vec3 lightDir = normalize(lightPos- frag_pos);
    float diff = max(0, dot(lightDir, Normal));
    return diff * diffuseInt * lightInt;
}

vec3 getSpecular(){
    vec3 Normal = normalize(normal);
    vec3 lightDir = normalize(lightPos- frag_pos);

    vec3 viewDir = normalize(camPos-frag_pos);
    vec3 reflectedDir = reflect(-lightDir, Normal);
    float spec = pow(max(0, dot(viewDir, reflectedDir)), 32);
    return spec * specInt * lightInt;
}

void main() {
    vec4 frag_color = 0.5 * Monochrome(vec3(1,1,1)) + 0.5 * Edge(vec3(0,1,0));
    // vec4 frag_color = 0.5 * Blur(vec3(1,1, 1));
    out_color = vec4((getSpecular() + getDiffuse() + getAmbient()) * frag_color.xyz, 1.0);
}