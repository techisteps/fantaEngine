from OpenGL.GL import *
from typing import List
from OpenGL.GL.shaders import compileProgram, compileShader


class ShaderProgram:
    src_filename: str
    shaderprog: int

class fantaShader:
    __instance = None
    __shaders: any
    __program = {}

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.window = None

            return cls.__instance
        else:
            return cls.__instance



    vertex_src = """
    # version 330 core

    layout (location = 0) in vec3 a_position;
    layout (location = 1) in vec3 a_color;
    layout (location = 2) in vec2 a_texture;

    out vec3 v_color;
    out vec2 v_texture;

    uniform mat4 model;
    uniform mat4 projection;

    void main(){
        gl_Position = projection * model * vec4(a_position, 1.0);
        v_color = a_color;
        v_texture = a_texture;
    }
    """

    fragment_src = """
    # version 330 core

    in vec3 v_color;
    in vec2 v_texture;
    out vec4 out_color;

    uniform sampler2D s_texture;

    void main(){
        //out_color = vec4(v_color, 1.0);
        out_color = texture(s_texture, v_texture);
    }
    """

    def getShaderSrc(self, t: str):
        if t == "vertex":
            return self.vertex_src
        elif t == "fragment":
            return self.fragment_src

    # def getProgram(self):
    #     return self.getProgram("")
    
    def getProgram(self, src_file: str):
        v_src: any = None
        f_src: any = None

        if src_file == "":
            v_src = self.vertex_src
            f_src = self.fragment_src
        else:
            if src_file in self.__program.keys():
                return self.__program[src_file]

            try:
                vertex_src_path = "assets/shaders/" + src_file + ".vert"
                with open(file = vertex_src_path, mode = "r") as file:
                    v_src = file.readlines()
                
                fragment_src_path = "assets/shaders/" + src_file + ".frag"
                with open(file = fragment_src_path, mode = "r") as file:
                    f_src = file.readlines()
            except IOError:
                print(f"ERROR: Cannot open file {src_file}.vert or {src_file}.frag.")
                exit(0)
            except:
                print(f"ERROR: Unexpected error while opening file {src_file}.vert or {src_file}.frag.")
                exit(0)
                

        # print("Vertex")
        # print(v_src)
        # print("Fragment")
        # print(f_src)

        vs = compileShader(v_src,GL_VERTEX_SHADER)
        fs = compileShader(f_src, GL_FRAGMENT_SHADER)
        shaderProgram = compileProgram(vs, fs)
        self.__program[src_file] = shaderProgram
        # shader = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER), validate = True)
        # glDeleteShader(vs)
        # glDeleteShader(fs)

        # Specify to use the shader program for rendering.
        # glUseProgram(shader)
        return shaderProgram

    def getDefaultProgram(self, src_file: str):
        return fantaShader.getProgram(src_file)