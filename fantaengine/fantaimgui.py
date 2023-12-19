import imgui
from imgui.integrations.glfw import GlfwRenderer
import sys
from fantaengine.fantaevents import *


class fantaImGUI:
    """This class is to handle GUI in development phase.

    Returns:
        fantaImGUI: A singleton object of class fantaImGUI.
    """

    __imgui_vis = {"addNode": False}

    __instance = None
    __impl = None
    __visible = False
    __quiting  = False
    def __new__(cls, window, *args, **kwargs):
        """
        __new__ Creates a singleton instance of class {class}

        This class is used for GUI for development phase.

        Args:
            window (Object): Object of GLFW

        Returns:
            fantaImGUI: An instance of fantaImGUI
        """

        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            
            imgui.create_context()
            cls.__impl = GlfwRenderer(window)
            # self.io = imgui.get_io()
            # self.jb = self.io.fonts.add_font_from_file_ttf(path_to_font, 30) if path_to_font is not None else None
            cls.__impl.refresh_font_texture()

            cls.f_events = fantaEvents()

            return cls.__instance
        else:
            return cls.__instance


    # def __init__(self, win):
    #     imgui.create_context()


    def addnode(self):
        li = ["box", "monkey", "cone"]
        sel_item = None
        imgui.begin("Test")
        if imgui.begin_list_box("TestLB").opened:
            for item in li:
                if imgui.selectable(item, False):
                    if imgui.is_item_clicked():
                        sel_item = item
                        self.f_events.dispatch_event("TestLB", item)

            # imgui.selectable("monkey")
            imgui.end_list_box()
        imgui.end()
    
    # if sel_item is not None:
    #     print(f"{sel_item} selected")
    #     sel_item = None



    # path_to_font = None  # "path/to/font.ttf"
    # def render_frame(impl, window, font):
    def render_frame(self, font):
        # glfw.poll_events()
        self.__impl.process_inputs()
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
        
        self.addnode()

        if self.__imgui_vis["addNode"]:
            with imgui.begin("Nodes"):
                with imgui.begin_list_box("") as list_box:
                    if list_box.opened:
                        imgui.selectable("box")
                        imgui.selectable("monkey")



        with imgui.begin_main_menu_bar() as main_menu_bar:
            if main_menu_bar.opened:
                with imgui.begin_menu("File", True) as file_menu:
                    if file_menu.opened:
                        clicked_node, selected_node = imgui.menu_item("Add Node", "Ctrl+N")
                        if clicked_node:
                            self.__imgui_vis["addNode"] = True

                        clicked_quit, selected_quit = imgui.menu_item("Quit", "Ctrl+Q")
                        if clicked_quit:
                            self.__quiting = True



        if font is not None:
            imgui.pop_font()

        imgui.render()
        self.__impl.render(imgui.get_draw_data())


    # def create_context():
    #     imgui.create_context()


    # def create_renderer(self, window):

    #     self.__impl = GlfwRenderer(window)
    #     # self.io = imgui.get_io()
    #     # self.jb = self.io.fonts.add_font_from_file_ttf(path_to_font, 30) if path_to_font is not None else None
    #     self.__impl.refresh_font_texture()

    #         # ImGUI Start
    #         # render_frame(self.impl, self.jb)
    #         # ImGUI End


    def isQuiting(self):
        return self.__quiting

    def getVisible(self):
        return self.__visible

    def show(self):
        self.__visible = True

    def hide(self):
        self.__visible = False

    def toggle(self):
        self.__visible = False if self.__visible else True

    def destroy(self):
        self.__impl.shutdown()
