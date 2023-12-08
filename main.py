
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from math import sin
import pyrr
from PIL import Image
# from objData import objData
from window import *
from gltfReader import *
from fantashader import fantaShader
from fantatexture import fantaTexture
from fantanode import fantaNode
# Define window
fantawin = FantaWin(400, 300)


monkeynode = fantaNode("assets/model/monkey.gltf")
monkeynodeVAO = monkeynode.createVAO()

boxnode = fantaNode("assets/model/box.gltf")
boxnodeVAO = boxnode.createVAO()

conenode = fantaNode("assets/model/cone.gltf")
conenodeVAO = conenode.createVAO()

# Define 3d object
# gltfSrcfile: str = "assets/model/monkey.gltf"
# gltfdata = gltfReader(gltfSrcfile)

# _meshIndex = 0
# _primitiveIndex = 0

# position_buf01 =  gltfdata.getMeshPosition(_meshIndex,_primitiveIndex)
# normal_buf02 =  gltfdata.getMeshNormal(_meshIndex,_primitiveIndex)
# tex0_buf03 =  gltfdata.getMeshTex0(_meshIndex,_primitiveIndex)
# indices = gltfdata.getMeshIndices(_meshIndex,_primitiveIndex)

# vertices1 = np.append(position_buf01, normal_buf02)
# vertices = np.append(vertices1, tex0_buf03)
# _buf_pos_01 = 0
# _buf_pos_02 = position_buf01.nbytes
# _buf_pos_03 = position_buf01.nbytes + normal_buf02.nbytes



global proj_mat



# checkerTex = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0,
#               1.0, 1.0, 1.0, 0.0, 0.0, 0.0]


# Set screen clear color
glClearColor(0.5, 0.4, 0.6, 1)
glEnable(GL_DEPTH_TEST)


# convert python arrays to numpy arrays as OpenGL expects in this format
# vertices = np.array(vertices, dtype = np.float32)
# indices = np.array(indices, dtype = np.uint32)
# checkerTex = np.array(checkerTex, dtype=np.uint8)


# Compile shader program from vertex and fragment shader source code
fShader = fantaShader()
shader = fShader.getProgram("")
shader = fShader.getProgram("test")

# Specify to use the shader program for rendering.
glUseProgram(shader)


        # monkey_vao = glGenVertexArrays(1)
        # glBindVertexArray(monkey_vao)
        # ## STEP 3
        # # Generate buffer objects name. In this case we generated 2 named buffer objects.
        # # one for vertices and another for color
        # VBO = glGenBuffers(1)
        # glBindBuffer(GL_ARRAY_BUFFER, VBO)
        # glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        # # glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        # # glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        # # glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
        # glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(_buf_pos_01))
        # glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(_buf_pos_02))
        # glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8, ctypes.c_void_p(_buf_pos_03))
        # glEnableVertexAttribArray(0)
        # glEnableVertexAttribArray(1)
        # glEnableVertexAttribArray(2)

        # EDO = glGenBuffers(1)
        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EDO)
        # glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        # glBindVertexArray(0)

window = fantawin.getWindow()

w,h = glfw.get_window_size(window)
print(w,h)
proj_mat = pyrr.matrix44.create_perspective_projection_matrix(45, w/h , 0.1 , 100 )
trans_mat = pyrr.matrix44.create_from_translation(pyrr.vector3.create(0,0,-3))

model_loc = glGetUniformLocation(shader, "model")
projectoin_loc = glGetUniformLocation(shader, "projection")

glUniformMatrix4fv(projectoin_loc, 1, GL_FALSE, proj_mat)

tex_Orange = fantaTexture("assets/texture/orange.png")
tex_Apple = fantaTexture("assets/texture/apple.jpg")
tex_checker = fantaTexture("assets/texture/apple.jpg")
tex_checker.setChecker()

# Start main eventloop for window
while not glfw.window_should_close(window):

    # Fetch all event
    glfw.poll_events()

    # Quit logic
    if glfw.get_key(window, glfw.KEY_ESCAPE):
        # glDeleteTextures(2, tex)
        # glDeleteTextures(len(tex), tex)
        fantaTexture.deleteAll()
        glDeleteProgram(shader)
        # print("VBO ", VBO, "EDO", EDO)
        # print("VBO", monkeynode.getVBO(), "EDO", monkeynode.getEDO())
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
    
    
    
    if glfw.get_key(window, glfw.KEY_M):
        glBindVertexArray(monkeynodeVAO)
        monkeynode.draw()
    elif glfw.get_key(window, glfw.KEY_B):
        glBindVertexArray(boxnodeVAO)
        boxnode.draw()
    else:
        glBindVertexArray(conenodeVAO)
        conenode.draw()

    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)


    # Instruction to start drawing with data provided data in step 3
    # glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
    # glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    
    
    if glfw.get_key(window, glfw.KEY_LEFT):
        glRotate(0.1, 0, 0, 1)
        glBindTexture(GL_TEXTURE_2D, tex_Orange.getTexID())
    if glfw.get_key(window, glfw.KEY_RIGHT):
        glRotate(-0.1, 0, 0, 1)
        glBindTexture(GL_TEXTURE_2D, tex_Apple.getTexID())
    if glfw.get_key(window, glfw.KEY_UP):
        glRotate(-0.1, 0, 0, 1)
        glBindTexture(GL_TEXTURE_2D, 0)
    if glfw.get_key(window, glfw.KEY_DOWN):
        glRotate(-0.1, 0, 0, 1)
        tex_checker.setChecker()
        glBindTexture(GL_TEXTURE_2D, tex_checker.getTexID())

    # Swap buffers
    glfw.swap_buffers(window)




fantawin.destroy_window(0)


