# version 330 core

in vec3 v_color;
in vec2 v_texture;
out vec4 out_color;

uniform sampler2D s_texture;

void main(){
    //out_color = vec4(v_color, 1.0);
    out_color = texture(s_texture, v_texture);
}