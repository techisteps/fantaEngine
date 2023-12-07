from fantashader import fantaShader


test1 = fantaShader()
test2 = fantaShader()


print(test1)
print(test2)

sp1 = test1.getProgram("test")
sp2 = test1.getProgram("test")