from icecream import ic
ic.configureOutput(prefix="DebugLog:-> " ,includeContext=True, contextAbsPath=True)

class Globals:

    __instance = None
    __globals = {}

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        else:
            return cls.__instance

    def add_global(self, key: any, value: any):
        try:
            if key == None:
                raise ValueError("Key cannot be None.")
            val = self.__globals.get(key)
            self.__globals[key] = value            
            # if val == None:
            #     self.__globals[key] = value
            # else:
            #     self.__globals[key] = value
        except ValueError as err:
            print(err)


    def remove_global(self, key: any):
        val = self.__globals.pop(key)
        # print("Item removed : ", val)
        ic(("Item removed : " + val))

    def get_global(self, key: any) -> any:
        return self.__globals.get(key)

    def print_globals(self):
        print(self.__globals)
    

if __name__ == "__main__":
    gv = Globals()
    gv.add_global("key1","test1")
    gv.add_global("key1","test2")
    gv.add_global("key2","test3")
    gv.add_global(key=None, value="None")
    gv.add_global("key3", value=None)
    gv.add_global(4, value="int")
    gv.print_globals()

    print(gv.get_global("key1"))
    print(gv.get_global(4))
    gv.remove_global("key1")
    print(gv.get_global("key1"))
    gv.print_globals()    