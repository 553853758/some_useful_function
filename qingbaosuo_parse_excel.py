import xlrd
import xlwt

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
    excel_name = "201707"
    filename = "./doc/%s.xls"%(excel_name)
    excel_dict,labels = read_excel(filename=filename,sheet_index=1,has_head=False)
    car_labels = read_excel_by_row(excel_name="./doc/cars_label.xls",row_index=0,sheet_index=0)

    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('sheet0')
    write_col = 0
    write_row = 1

    for first_col in range(0,len(car_labels)):
        worksheet.write(0,first_col,car_labels[first_col])

    for key in excel_dict.keys():
        current_data = excel_dict[key]
        row_count = current_data[1].count("and")+1
        for row_n in range(0,row_count):
            for write_col in range(0,len(car_labels)):
                for cur_data_index in range(0,len(current_data)):
                    cur_data = current_data[cur_data_index]
                    cur_label = car_labels[write_col]
                    cur_data_type = cur_data.split("：")[0]
                    if write_col==0:
                        worksheet.write(write_row,write_col,current_data[0])
                        break
                    else:
                        #涉及到"最高车速" in "30分钟最高车速"问题。所以单独拎出来
                        if "30分钟最高车速" in cur_label and "30分钟最高车速" not in cur_data_type:
                            continue
                        elif "30分钟最高车速" in cur_data_type and "30分钟最高车速" not in cur_label:
                            continue

                        #涉及到"续驶里程" in "纯电动模式下续驶里程"的问题，所以也是拎出来。
                        if "纯电动模式下续驶里程" in cur_label and "纯电动模式下续驶里程" not in cur_data_type:
                            continue
                        elif "纯电动模式下续驶里程" in cur_data_type and "纯电动模式下续驶里程" not in cur_label:
                            continue

                        if cur_data_type in cur_label or cur_label in cur_data_type:
                            if "and" in cur_data:
                                if "：" in cur_data:
                                    cur_write_data = cur_data.split("：")[1].split("and")[row_n]
                                else:
                                    cur_write_data = cur_data.split("and")[row_n]
                            else:
                                if "：" in cur_data:
                                    cur_write_data = cur_data.split("：")[1]
                                else:
                                    cur_write_data = cur_data
                            worksheet.write(write_row,write_col,cur_write_data)
                            break
                        else:
                            pass
            write_col = 0
            write_row += 1


    workbook.save("./doc/out/%s_out.xls"%(excel_name))
    print("over")