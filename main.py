
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from math import sin
import pyrr
from PIL import Image
# from window import *
# from gltfReader import *
# from fantashader import fantaShader
# from fantatexture import fantaTexture
# from fantanode import fantaNode
# from fantaimgui import fantaImGUI
# from fantaengine import fantawindow, fantashader, fantanode, fantatexture, fantaimgui, gltfReader
from fantaengine import *



# Define window
fantawin = fantawindow.FantaWin(400, 300)
fantaRender = rendertree.RenderTree()

# Load 3D objects
monkeynode = fantanode.fantaNode("monkey", "assets/model/monkey.gltf")
# monkeynode = fantanode.fantaNode(nodename="monkey", assetpath="assets/model/monkey.gltf")
# print(monkeynode)
# monkeynode = fantanode.fantaNode("monkey", "assets/model/monkey.gltf")
# print(monkeynode)
# monkeynodeVAO = monkeynode.createVAO()
boxnode = fantanode.fantaNode("box", "assets/model/box.gltf")
# boxnodeVAO = boxnode.createVAO()
conenode = fantanode.fantaNode("cone", "assets/model/cone.gltf")
# conenodeVAO = conenode.createVAO()

fantaRender.add_child(monkeynode)
fantaRender.add_child(boxnode)
fantaRender.add_child(boxnode)
fantaRender.remove_child(boxnode)
fantaRender.remove_child(boxnode)
# fantaRender.add_child(conenode)


# Compile shader program from vertex and fragment shader source code
fShader = fantashader.fantaShader()
shader = fShader.getProgram("")
shader = fShader.getProgram("test")
# Specify to use the shader program for rendering.
glUseProgram(shader)


# Load Textures
tex_Orange = fantatexture.fantaTexture("assets/texture/orange.png")
tex_Apple = fantatexture.fantaTexture("assets/texture/apple.jpg")
tex_checker = fantatexture.fantaTexture("assets/texture/apple.jpg")
tex_checker.setChecker()



# Create window
window = fantawin.getWindow()
w,h = glfw.get_window_size(window)

global proj_mat
proj_mat = pyrr.matrix44.create_perspective_projection_matrix(45, w/h , 0.1 , 100 )
trans_mat = pyrr.matrix44.create_from_translation(pyrr.vector3.create(0,0,-3))

model_loc = glGetUniformLocation(shader, "model")
projectoin_loc = glGetUniformLocation(shader, "projection")

glUniformMatrix4fv(projectoin_loc, 1, GL_FALSE, proj_mat)

f_imgui = fantaimgui.fantaImGUI(window=window)



# Set screen clear color
glClearColor(0.5, 0.4, 0.6, 1)
glEnable(GL_DEPTH_TEST)


def enableGUI(win, key, scancode, action, mods):
    if glfw.get_key(window, glfw.KEY_ESCAPE):
        f_imgui.toggle()

glfw.set_key_callback(window, enableGUI)

# Start main eventloop for window
while not glfw.window_should_close(window):

    # Fetch all event
    glfw.poll_events()

    # Quit logic
    # if glfw.get_key(window, glfw.KEY_ESCAPE):
    if f_imgui.isQuiting():
        fantatexture.fantaTexture.deleteAll()
        glDeleteProgram(shader)
        glfw.terminate()
        exit(0)



    # Indication to refresh screen color. It'll use the color mentioned in glClearColor()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_x = pyrr.Matrix44.from_x_rotation(glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(glfw.get_time())
    rotation = pyrr.matrix44.multiply(rot_x , rot_y)
    model = pyrr.matrix44.multiply(rotation , trans_mat)


   
    # if glfw.get_key(window, glfw.KEY_M):
    #     glBindVertexArray(monkeynodeVAO)
    #     monkeynode.draw()
    # elif glfw.get_key(window, glfw.KEY_B):
    #     glBindVertexArray(boxnodeVAO)
    #     boxnode.draw()
    # else:
    #     glBindVertexArray(conenodeVAO)
    #     conenode.draw()


    """
    TODO add VAO to fantanode class and implement add_child and remove_child in rendertree class.
    """
    # glBindVertexArray(monkeynodeVAO)
    # monkeynode.render()
    # glBindVertexArray(boxnodeVAO)
    # boxnode.render()


    # if glfw.get_key(window, glfw.KEY_A):
    #     fantaRender.add_child(monkeynode)
    # if glfw.get_key(window, glfw.KEY_D):
    #     fantaRender.remove_child(monkeynode)


    fantaRender.render()
    

    # TODO should move GUI render to render function in rendertree
    if f_imgui.getVisible():   
        f_imgui.render_frame(font= None)

    # Swap buffers
    glfw.swap_buffers(window)

    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

    
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



f_imgui.destroy()
fantawin.destroy_window(0)


