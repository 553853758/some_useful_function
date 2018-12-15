
def quchong( filename ):#每一行都读入列表，如果新的已经在列表中，则不保存。返回一个列表
    f = open(filename,"r")
    word_list = []
    for line in f.readlines():
        word = line.replace("\n","")
        if not word in word_list:
            word_list.append(word)
    f.close()
    return word_list

def write_list_into_file( filename,saved_list ):
    out = open(filename,"w")
    for line in saved_list:
        out.write(line+"\n")
    out.close()


if __name__ == "__main__":
    word_list = quchong("./doc/fuxiangci.txt")
    print(word_list[0])
    write_list_into_file("./doc/fuxiangci_去重.txt",word_list)