import glfw
import pyrr
from OpenGL.GL import *

class FantaWin:

    __instance = None
    window: any

    def __new__(cls, win_width: int, win_height: int, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.window = None

            # Initialise glfw module and raise exception if not able to do successfully.
            if not glfw.init():
                raise Exception("Can't initialise GLFW.")

            # Create the window object where OpenGL interaction will happen.
            cls.__instance.window  = glfw.create_window(800, 600, "OpenGL Test", None, None)

            # If window creation is not successful raise exception.
            if not cls.__instance.window:
                glfw.terminate()
                raise Exception("Can't create window.")

            # Below statement is optional. Its just to set window position on monitor.
            glfw.set_window_pos(cls.__instance.window, win_width, win_height)

            # Define a function for window resize callback. Inside function set the viewport size to new one.
            # def window_resize(window, w, h):
            #     # glfw.set_window_size(window, w, h)
            #     proj_mat = pyrr.matrix44.create_perspective_projection_matrix(45, w/h, 0.1 , 100 )
            #     glUniformMatrix4fv(projectoin_loc, 1, GL_FALSE, proj_mat)
            #     glViewport(0, 0, w, h)

            # SPecify and set callback function for window resize
            # glfw.set_window_size_callback(window, window_resize)

            # Make this window the current context to handle OpenGL
            # OpenGL commands need context to draw on screen.
            ###
            ### Call any OpenGL command only after successful creation of context
            ###
            glfw.make_context_current(cls.__instance.window)
            return cls.__instance
        else:
            return cls.__instance



    def destroy_window(self, exit_code: int):
        # Destroy the window
        glfw.terminate()
        exit(exit_code)

    def getWindow(self):
        return self.window