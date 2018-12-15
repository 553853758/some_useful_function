# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 17:58:30 2016

@author: Ricky
"""
import xlwt


def ricWriteExcelCol( excel_name,write_data=[[],[]] ):
    '''
    将要写的数据保存到excel表格
    write_data可以是一个两级列表，则每一个子列表保存一列
    也可以是一个单级列表，此时相当于只有一列
    '''
    excel = xlwt.Workbook(encoding='utf-8')
    sheet = excel.add_sheet("sheet0")
    if type(write_data[0]) == list:#多级列表，相当于有很多列
        for col in range( len(write_data) ):
            col_data = write_data[col]
            for row in range( len(col_data) ):
                sheet.write( row,col,str(col_data[row]) )
    else:
        col = 0
        for row in range( len(write_data) ):
            sheet.write( row,col,str(write_data[row]) )
    excel.save(excel_name)
    return True
                
if __name__ == "__main__":
    write_data = [[1,2,3],[2,3,4,5]]
    excel_name = "try.xls"
    ricWriteExcelCol( excel_name,write_data )