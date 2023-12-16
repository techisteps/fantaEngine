from fantaengine.globals import Globals
from icecream import ic
ic.configureOutput(prefix="DebugLog:-> " ,includeContext=True, contextAbsPath=True)

from fantaengine.fantanode import *
from fantaengine.rendertree import *

class NodeList:

    __instance = None
    __node_name_list = {}
    gv = None
    fantaRender = None

    def __new__(cls, *args, **kwargs):
        # Singleton code start
        if cls.__instance is None:
            # Create object
            cls.__instance = super().__new__(cls)
            
            # Define global objects
            cls.gv = Globals()
            cls.fantaRender = RenderTree()

            return cls.__instance
        else:
            return cls.__instance
        # Singleton code end


    def add_item(self, nodename:str, assetpath: str):

        if nodename != None:
            __nodename = nodename
        else:
            raise ValueError("Paremeter nodename can not be empty")
        ic(__nodename)
        if assetpath != None:
            __nodeasset = assetpath
        else:
            raise ValueError("Paremeter assetpath can not be empty")
        ic(__nodeasset)
        
        if __nodename not in NodeList.__node_name_list:
            obj = fantaNode(__nodename, __nodeasset)
            NodeList.__node_name_list[__nodename] = obj
            NodeList.gv.add_global("nodes", NodeList.__node_name_list)
            NodeList.fantaRender.add_child(obj)


    def delete_item(self, nodename:str):
        if nodename != None:
            __nodename = nodename
        else:
            raise ValueError("Paremeter nodename can not be empty")
        ic(__nodename)

        if __nodename in NodeList.__node_name_list:
            NodeList.fantaRender.remove_child( NodeList.__node_name_list[__nodename] )

            del NodeList.__node_name_list[__nodename]
            NodeList.gv.add_global("nodes", NodeList.__node_name_list)

            