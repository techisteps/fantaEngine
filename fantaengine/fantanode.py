from fantaengine.globals import Globals
from icecream import ic
ic.configureOutput(prefix="DebugLog:-> " ,includeContext=True, contextAbsPath=True)

from OpenGL.GL import *
from fantaengine.gltfReader import *

class fantaNode:

    __vao = None
    __VBO = None
    __EDO = None
    __node_ID = 0
    __node_name = None
    __node_name_list = []

    # gv = Globals()
    # gv.add_global("node_count", 0)

    def __new__(cls, *args, **kwargs):
        print("*args", args,"**kwargs", kwargs)

        _a1 = args[0] if len(args) else None
        _a2 = kwargs["nodename"] if len(kwargs) else None

        if (_a1 in fantaNode.__node_name_list) or (_a2 in fantaNode.__node_name_list):
            # return None
            raise ValueError(f"Node already exist.")
        else:
            return super().__new__(cls)
        # pass

    def __init__(self, nodename:str, assetpath: str):

        # if nodename not in fantaNode.__node_name_list:
        #     fantaNode.__node_name_list.append(nodename)
        #     ic("node present: " + nodename)

        fantaNode.__node_name_list.append(nodename)

        self.__node_ID += 1
        self.__node_name = nodename
    
        self.gltfSrcfile: str = assetpath
        self.gltfdata = gltfReader(self.gltfSrcfile)

        self._meshIndex = 0
        self._primitiveIndex = 0

        self.position_buf01 =  self.gltfdata.getMeshPosition(self._meshIndex, self._primitiveIndex)
        self.normal_buf02 =  self.gltfdata.getMeshNormal(self._meshIndex, self._primitiveIndex)
        self.tex0_buf03 =  self.gltfdata.getMeshTex0(self._meshIndex, self._primitiveIndex)
        self.indices = self.gltfdata.getMeshIndices(self._meshIndex, self._primitiveIndex)

        self.vertices1 = np.append(self.position_buf01, self.normal_buf02)
        self.vertices = np.append(self.vertices1, self.tex0_buf03)
        self._buf_pos_01 = 0
        self._buf_pos_02 = self.position_buf01.nbytes
        self._buf_pos_03 = self.position_buf01.nbytes + self.normal_buf02.nbytes

        fantaNode.createVAO(self)

    def getID(self):
        return self.__node_ID
    def getName(self):
        return self.__node_name
    
    def createVAO(self):
        self.__vao = glGenVertexArrays(1)
        glBindVertexArray(self.__vao)
        ## STEP 3
        # Generate buffer objects name. In this case we generated 2 named buffer objects.
        # one for vertices and another for color
        self.__VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.__VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        # glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        # glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        # glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(self._buf_pos_01))
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(self._buf_pos_02))
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8, ctypes.c_void_p(self._buf_pos_03))
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)

        self.__EDO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.__EDO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)
        glBindVertexArray(0)
        return self.__vao

    def getVBO(self):
        return self.__VBO
    
    def getEDO(self):
        return self.__EDO
    

    def render(self):
        glBindVertexArray(self.__vao)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
