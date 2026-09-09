class File_actions():


    def Write(file_name, data):
        file = open(file_name,"w")
        file.write(str(data))
        file.close()

    def write_array(file_name, array):
        file = open(file_name,"a")
        for index in range(len(array)):
            ##We use a carriage return shortcut in order to deal with improper line reading
            file.write(str(array[index])+"\n")
            print(array[index])
        file.close()

    def append(file_name, data,):
        file = open(file_name,"a")
        file.write(str(data))
        file.close()

    def Read(file_name):

        file = open(file_name,"r")
        contents = []
        counter = 0
        while True:
            
            ##All files, in order to be read and appended properly, have the \n shortcut at the end of them. When python reads strings, these are countedd
            ##So they must be removed, the code below removes them
            n = file.readline()
            if not n: break
            n= n.strip()
            contents = n
        return contents

    def wipe(file_name):
        file = open(file_name,"w")
        file.write("")
        file.close()
