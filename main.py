
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from math import sin
import pyrr
from PIL import Image
# from objData import objData
from window import *
from fantashader import fantaShader




# v1 = FantaWin(400, 300)
# v2 = FantaWin(400, 300)

# print(v1)
# print(v2)
# w1 = v1.getWindow()
# w2 = v2.getWindow()
# print(w1)
# print(w2)

fantawin = FantaWin(400, 300)



objSrcfile: str = "box.obj"
# objdata = objData(objSrcfile)

# Create vertex and color array

vertices = [-0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5,  0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5, -0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

             0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
             0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
            -0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
            -0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

             0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
            -0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
            -0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
             0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0]

# vertices = objdata.getVertexList()
# print(objdata.getVertexListLen())
# Create new array for holding indices

indices = [0,  1,  2,  2,  3,  0,
           4,  5,  6,  6,  7,  4,
           8,  9, 10, 10, 11,  8,
          12, 13, 14, 14, 15, 12,
          16, 17, 18, 18, 19, 16,
          20, 21, 22, 22, 23, 20]

# indices = objdata.getElementList()
# print(objdata.getElementListLen())




global proj_mat



checkerTex = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0,
              1.0, 1.0, 1.0, 0.0, 0.0, 0.0]


# Set screen clear color
glClearColor(0.5, 0.4, 0.6, 1)
glEnable(GL_DEPTH_TEST)


# convert python arrays to numpy arrays as OpenGL expects in this format
vertices = np.array(vertices, dtype = np.float32)
indices = np.array(indices, dtype = np.uint32)
checkerTex = np.array(checkerTex, dtype=np.uint8)

# print("GL_VENDOR : " + str(glGetString(GL_VENDOR)))
# print("GL_RENDERER : " + str(glGetString(GL_RENDERER)))
# print("GL_VERSION : " + str(glGetString(GL_VERSION)))
# print("GL_SHADING_LANGUAGE_VERSION : " + str(glGetString(GL_SHADING_LANGUAGE_VERSION)))
# print("GL_EXTENSIONS : " + str(glGetString(GL_EXTENSIONS)).replace(" ","\n") )




# Compile shader program from vertex and fragment shader source code
fShader = fantaShader()
shader = fShader.getProgram("")
shader = fShader.getProgram("test")

# Specify to use the shader program for rendering.
glUseProgram(shader)


## STEP 3
# Generate buffer objects name. In this case we generated 2 named buffer objects.
# one for vertices and another for color
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
glEnableVertexAttribArray(0)
glEnableVertexAttribArray(1)
glEnableVertexAttribArray(2)

EDO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EDO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

window = fantawin.getWindow()

w,h = glfw.get_window_size(window)
print(w,h)
proj_mat = pyrr.matrix44.create_perspective_projection_matrix(45, w/h , 0.1 , 100 )
trans_mat = pyrr.matrix44.create_from_translation(pyrr.vector3.create(0,0,-3))

model_loc = glGetUniformLocation(shader, "model")
projectoin_loc = glGetUniformLocation(shader, "projection")

glUniformMatrix4fv(projectoin_loc, 1, GL_FALSE, proj_mat)


tex = glGenTextures(2)
glBindTexture(GL_TEXTURE_2D, tex[0])
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
# glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
# glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

print( "GL_ACTIVE_TEXTURE", glGetInteger(GL_ACTIVE_TEXTURE) )
print( "GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS", glGetInteger(GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS) )

text_ref = Image.open("assets/texture/orange.png")
text_data = text_ref.convert("RGBA").tobytes()
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_ref.width, text_ref.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

# glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 2, 2, 0, GL_RGB, GL_FLOAT, checkerTex)
glGenerateMipmap(GL_TEXTURE_2D)

# glActiveTexture(GL_TEXTURE0)
# tex_loc = glGetAttribLocation(shader, "a_texture")
# glEnableVertexAttribArray(tex_loc)
# glVertexAttribPointer(tex_loc, 2, GL_FLOAT, GL_FALSE, 12, 0)


glBindTexture(GL_TEXTURE_2D, tex[1])
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
# glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
# glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

print( "GL_ACTIVE_TEXTURE", glGetInteger(GL_ACTIVE_TEXTURE) )
print( "GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS", glGetInteger(GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS) )

text_ref = Image.open("assets/texture/apple.jpg")
text_data = text_ref.convert("RGBA").tobytes()
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_ref.width, text_ref.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

# glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 2, 2, 0, GL_RGB, GL_FLOAT, checkerTex)
glGenerateMipmap(GL_TEXTURE_2D)



# Start main eventloop for window
while not glfw.window_should_close(window):

    # Fetch all event
    glfw.poll_events()

    # Quit logic
    if glfw.get_key(window, glfw.KEY_ESCAPE):
        # glDeleteTextures(2, tex)
        glDeleteTextures(len(tex), tex)
        glDeleteProgram(shader)
        print("VBO ", VBO, "EDO", EDO)
        # glBindBuffer(GL_ARRAY_BUFFER, 0)
        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        # glDeleteBuffers(1, EDO)
        # glDeleteBuffers(1, VBO)
        glfw.terminate()
        exit(0)

    # Indication to refresh screen color. It'll use the color mentioned in glClearColor()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_x = pyrr.Matrix44.from_x_rotation(glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(glfw.get_time())
    rotation = pyrr.matrix44.multiply(rot_x , rot_y)
    model = pyrr.matrix44.multiply(rotation , trans_mat)
    
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

    # Instruction to start drawing with data provided data in step 3
    # glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    
    if glfw.get_key(window, glfw.KEY_LEFT):
        glRotate(0.1, 0, 0, 1)
        glBindTexture(GL_TEXTURE_2D, tex[0])
    if glfw.get_key(window, glfw.KEY_RIGHT):
        glRotate(-0.1, 0, 0, 1)
        glBindTexture(GL_TEXTURE_2D, tex[1])
    
    # Swap buffers
    glfw.swap_buffers(window)




fantawin.destroy_window(0)


