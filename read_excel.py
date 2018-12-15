import xlrd


def read_excel_by_col( excel_name,col_index,sheet_index ):
    '''
    读入文件名和列号，返回列的数据。
    默认：保留第一行。需要删自己删
    return：文件某一列的list
    '''
    excel = xlrd.open_workbook( excel_name )
    sheet = excel.sheet_by_index(sheet_index)
    col_data = sheet.col_values( col_index )
    return col_data


def read_excel_by_row( excel_name,row_index,sheet_index ):
    '''
    读入文件名和列号，返回列的数据。
    默认：保留第一行。需要删自己删
    return：文件某一列的list
    '''
    excel = xlrd.open_workbook( excel_name )
    sheet = excel.sheet_by_index(sheet_index)
    row_data = sheet.row_values( row_index )
    return row_data

def read_excel( filename,sheet_index=0,has_head=True,key_col=False ):
    '''

    :param filename: The name of the file
    :param has_head: Whether the first row is the label.
    :param key_col:Whether there is a label col. If not, get number 0~col_num as label
    :return:
    '''

    excel_dict = {}
    labels = []
    excel_file = xlrd.open_workbook(filename)
    table = excel_file.sheet_by_index(sheet_index)
    cols_number = table.ncols
    if cols_number<key_col:
        print("The key_col is larger than cols_number")
        return False
    rows_number = table.nrows
    for row_num in range(0,rows_number):
        row_data = table.row_values(row_num)
        if row_num==0:
            if has_head:
                labels = row_data
                continue
            else:
                labels = [i for i in range(0,cols_number)]
        if not key_col:#There is no key_col
            excel_dict[str(row_num)] = row_data
        else:
            excel_dict[str(row_data[key_col])] = row_data
    return excel_dict,labels

if __name__ == "__main__":
    filename = "./doc/201701.xls"
    excel_dict,labels = read_excel(filename=filename,sheet_index=1,has_head=False)
    print("over")