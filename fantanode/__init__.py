from OpenGL.GL import *
from gltfReader import *

class fantaNode:
    

    def __init__(self, assetpath: str):
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

    
    def createVAO(self):
        self.__vao = glGenVertexArrays(1)
        glBindVertexArray(self.__vao)
        ## STEP 3
        # Generate buffer objects name. In this case we generated 2 named buffer objects.
        # one for vertices and another for color
        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
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

        self.EDO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EDO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)
        glBindVertexArray(0)
        return self.__vao

    def getVBO(self):
        return self.VBO
    
    def getEDO(self):
        return self.EDO
    

    def draw(self):
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
