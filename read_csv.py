import csv

def check_encoding( filename ):
    try:
        csv_file = open(filename,"r",encoding="gbk")
        csv_reader = csv.reader(csv_file)
        i=0
        for row in csv_reader:
            if i >= 2:
                break
            i += 1
        return("gbk")
    except:
        return("utf-8")

def read_csv_as_dict ( filename,has_head=True,ignore_col=[],key_col=0 ):
    '''
    Read a CSV file.
    :param filename: The path of the file.
    :param has_head: Whether the head row is a label. If there is no head, the label will be the index of the col
    :param ignore_col: Whether there exist cols that need not to be read. Must be a list
    :param key_col: The keyword-col of the file.
    :return: A dictionary like {key_col1:{label1:col1,label2:col2...}}
    '''
    csv_dict = {}
    if type(ignore_col)!=list:
        print("The type of ignore_col must be a list.")
        return False
    csv_file = open(filename,"r", encoding=check_encoding(filename),errors='ignore')
    row_num = 0
    for row in csv.reader(csv_file):
        if row_num==0:
            if has_head:
                labels=row
                row_num += 1
                continue#If it is a head lable. Jump this row.
            else:
                labels=list( range(0,len(row) ))
        keyword = row[key_col]
        for n in range(0,len(row)):
            #print(len(row))
            if n in ignore_col:
                continue
            try:
                csv_dict[keyword][labels[n]] = row[n]
            except:
                csv_dict[keyword]= {}
                csv_dict[keyword][labels[n]] = row[n]
            csv_dict[keyword]["all"]=row
        row_num += 1
    return csv_dict,labels

if __name__ == "__main__":
    #先把所有文件读了
    filename='./doc/clean_if_csv.csv'
    csv_dict, labels = read_csv_as_dict(filename)
    print("Over")
