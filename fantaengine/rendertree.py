from fantaengine.globals import Globals
from icecream import ic
ic.configureOutput(prefix="DebugLog:-> " ,includeContext=True, contextAbsPath=True)

class RenderTree:

    __instance = None
    __render_tree = {}
    __obj_id = 0

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.gv = Globals()
            cls.gv.add_global("InstanceCount", 0)

            return cls.__instance
        else:
            return cls.__instance

    def add_child(self, obj: any):
        self.__render_tree[obj.getName()] = obj
        self.__obj_id += 1
        RenderTree.gv.add_global("InstanceCount", self.__obj_id)
        ic(self.__render_tree)

    def remove_child(self, obj:any):
        name = obj.getName()
        if name in self.__render_tree:
            self.__render_tree.pop( obj.getName() )
            self.__obj_id -= 1
            RenderTree.gv.add_global("InstanceCount", self.__obj_id)
            ic(self.__render_tree)

    def render(self):
        for key, value in self.__render_tree.items():
            value.render()

    def print_tree(self):
        print(self.__render_tree)
        ic(RenderTree.gv.get_global("InstanceCount"))

    

if __name__ == "__main__":
    print("Test")

    tree = RenderTree()
    tree.add_child("test1")
    tree.add_child("test2")
    tree.print_tree()