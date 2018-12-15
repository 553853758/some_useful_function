import xlwt
import read_csv

def write_two_level_dict_into_excel( filename,dict,second_labels,need_first_key=False,first_label="id",first_ignore_key=[],second_ignore_key=["all"] ):
    '''
    为了实现将一个字典写入一个excel表格而设计。字典是一个两层的字典，第一层可能是id，第二层是各个id对应的各组数据。有一些标签是之前为了方便处理写入的,需要忽略，分成一级需要忽略的标签和二级需要忽略的标签，就是上面的后两个参数。
    :param filename:
    :param dict: 需要写入的字典
    :param second_labels: 需要读取和保存的二级标签。等于这些就是第一列的"标题"
    :param need_first_key: 有的时候一级标签纯粹是用来区分各行，所以是否需要忽略可以决定。如果不忽略，默认写到第一行
    :param first_label: 一级的标签默认为"id"。
    :param first_ignore_key: 一级标签里面需要忽略的标签
    :param second_ignore_key: 二级标签里面需要忽略的标签
    :return:
    '''
    if type(first_ignore_key) != list or type(second_ignore_key)!=list:
        print("Make sure that first_ignore_key and second_ignore_key are list.")
        print("If there are no keys to be ignored ,let them=[].")
        return False
    out_file = xlwt.Workbook()
    sheet = out_file.add_sheet(u'sheet0',cell_overwrite_ok=True)
    row = 0
    col = 0
    if need_first_key == True:#需要写入一级标签
        sheet.write( row,col,first_label )
        col+=1
    for label in second_labels:
        if label in second_ignore_key:
            continue
        sheet.write( row,col,label )
        col+=1
    row+=1
    for first_key in dict.keys():
        col=0
        if first_key in first_ignore_key:#这一行需要忽略
            continue
        if need_first_key:
            sheet.write( row,col,first_key )
            col+=1
        for second_key in second_labels:
            if second_key in second_ignore_key:
                continue
            sheet.write(row, col, dict[first_key][second_key])
            col+=1
        row+=1
    out_file.save(filename)
    return True

if __name__ == "__main__":
    filename='./doc/clean_if_csv.csv'
    csv_dict, labels = read_csv.read_csv_as_dict(filename)
    if_data_labels = ["IF 2016-2017",'IF 2015-2016','IF 2014-2015','IF 2013-2014','IF 2012-2013','IF 2011-2012','IF 2010-2011','IF 2009-2010','IF 2008-2009','IF 2007-2008']
    if_data = {}
    range=[">=10",">=9",">=8",">=7",">=6",">=5","<5","none","all"]
    for key in if_data_labels:
        if_data[key]={}
        for r in range:
            if_data[key][r]=0
    for line in csv_dict.keys():
        for cur_year in if_data_labels:
            cur_year_data = csv_dict[line][cur_year]
            if float(cur_year_data)>=10:
                if_data[cur_year][">=10"]+=1

            elif float(cur_year_data)>=9:
                if_data[cur_year][">=9"]+=1

            elif float(cur_year_data)>=8:
                if_data[cur_year][">=8"]+=1

            elif float(cur_year_data)>=7:
                if_data[cur_year][">=7"]+=1

            elif float(cur_year_data)>=6:
                if_data[cur_year][">=6"]+=1

            elif float(cur_year_data)>=5:
                if_data[cur_year][">=5"]+=1

            elif float(cur_year_data)<5 and float(cur_year_data)>0:
                if_data[cur_year]["<5"]+=1

            else:
                if_data[cur_year]["none"]+=1
            if_data[cur_year]["all"]+=1

    filename = "./doc/out/"+"if_count"+".xls"
    write_two_level_dict_into_excel( filename=filename,dict=if_data,second_labels=range,first_label="year",need_first_key=True ,second_ignore_key=[])
    print("over")