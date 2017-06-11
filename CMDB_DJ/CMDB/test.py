#encoding: utf-8

def file():
    file1 = open("nginx.conf","w+")
    file1.write("121212121")
    file1.close()
    g = open('update.conf', 'r')
    a = len(g.readlines())
    print(a)
    g.close()


if __name__=="__main__":
    file()