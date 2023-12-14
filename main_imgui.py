
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

import imgui
from imgui.integrations.glfw import GlfwRenderer

# ImGUI Start
path_to_font = None  # "path/to/font.ttf"
def render_frame(impl, window, font):
    # glfw.poll_events()
    impl.process_inputs()
    imgui.new_frame()

    # glClearColor(0.1, 0.1, 0.1, 1)
    # glClear(GL_COLOR_BUFFER_BIT)

    if font is not None:
        imgui.push_font(font)
    # frame_commands()


    with imgui.begin("Example: simple popup"):
        if imgui.button("select"):
            imgui.open_popup("select-popup")
        imgui.same_line()
        with imgui.begin_popup("select-popup") as popup:
            if popup.opened:
                imgui.text("Select one")
                imgui.separator()
                imgui.selectable("One")
                imgui.selectable("Two")
                imgui.selectable("Three")



    if font is not None:
        imgui.pop_font()

    imgui.render()
    impl.render(imgui.get_draw_data())

# ImGUI End

# ImGUI Start
imgui.create_context()
# ImGUI End

# Define window
fantawin = FantaWin(400, 300)


monkeynode = fantaNode("assets/model/monkey.gltf")
monkeynodeVAO = monkeynode.createVAO()

boxnode = fantaNode("assets/model/box.gltf")
boxnodeVAO = boxnode.createVAO()

conenode = fantaNode("assets/model/cone.gltf")
conenodeVAO = conenode.createVAO()


global proj_mat


# Set screen clear color
glClearColor(0.5, 0.4, 0.6, 1)
glEnable(GL_DEPTH_TEST)



# Compile shader program from vertex and fragment shader source code
fShader = fantaShader()
shader = fShader.getProgram("")
shader = fShader.getProgram("test")

# Specify to use the shader program for rendering.
glUseProgram(shader)

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

# ImGUI Start
impl = GlfwRenderer(window)
io = imgui.get_io()
jb = io.fonts.add_font_from_file_ttf(path_to_font, 30) if path_to_font is not None else None
impl.refresh_font_texture()
# ImGUI End

# Start main eventloop for window
while not glfw.window_should_close(window):

    # Fetch all event
    glfw.poll_events()

    # Quit logic
    if glfw.get_key(window, glfw.KEY_ESCAPE):
        fantaTexture.deleteAll()
        glDeleteProgram(shader)
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


    # ImGUI Start
    render_frame(impl, window, jb)
    # ImGUI End

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

    # Swap buffers
    glfw.swap_buffers(window)


# ImGUI Start
impl.shutdown()
# ImGUI End
fantawin.destroy_window(0)


