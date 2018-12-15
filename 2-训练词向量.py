# -*- coding: utf-8 -*-
"""
Created on Fri Dec 09 17:21:42 2016

@author: Ricky
"""

'''
写一个训练词向量的函数，
'''

import xlrd
from gensim.models import Word2Vec
import jieba
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 
    
def trainWordToVectorModel( data_set,save_file_name="../docs/WordToVec.model" ):
    '''
    读入数据集，自动训练词向量，保存到save_file_name制定的文件下
    数据集要求是没有切分好词的数据
    return:词向量模型
    '''
    print("Strat to build WordToVec..")
    if not type(data_set[0])==list:#如果不是列表，说明没有分词
        data_cut = [] #切分后的词的数据集
        for sentence in data_set:
            data_cut.append( list( jieba.cut(sentence) ) )
    else:#说明分好词了
        data_cut = data_set
    model = Word2Vec(data_cut, size=100, window=5, min_count=2, workers=1)
    model.save( save_file_name )
    return model

def ricReadExcelCol( excel_name,col_index ):
    '''
    读入文件名和列号，返回列的数据。
    默认：保留第一行。需要删自己删
    return：文件某一列的list
    '''
    excel = xlrd.open_workbook( excel_name )
    sheet = excel.sheet_by_index(0)
    col_data = sheet.col_values( col_index )
    return col_data
    
def deleteHTMLString( sentence ):
    '''
    读入一个句子，将里面的HTML的语言删除
    常见的HTML符号为：
    &nbsp;  空格
    &amp;   &
    &lt;       <
    &gt;      >
    &quot;   "
    &qpos;   '
    根据观察，大部分的HTML语言以“&lt;”到“&gt;”为一个单位，因此使用正则表达式删除
    “&lt.*?&gt;”这些类型的语言。
    另外发现一个特例“&amp;nbsp;”不在上面所说的单位里面，所以使用nbsp;|amp;|quot;|qpos;
    将这些符号删除。
    return:删掉HTML语言的字符串
    '''
    match_result = re.sub( "&lt.*?&gt;","",sentence )#删掉符合这个规范的HTML语言
    match_result = re.sub( "nbsp;|amp;|quot;|qpos;","",match_result )#不符合上面规范，但属于HTML语言的，删掉。先忽略&符号
    match_result = re.sub("&","",match_result)#最后再删掉"&"符号
    return match_result

def getCorrespongdingRow( excel_name,answer_col=1):
    '''
    因为文档中出现了单元格拆分，例如问题1位于第1行，但他对应的回答可能占1~10行。
    因此写这个函数来统计:问题行数————对应答案行数。
    返回一个字典如下：
    {1:[1:10],10:[10:14]..}表示，第一个问题位于1行，他对应的回答位于1~9行（PY的减一）；
    第二个问题位于10行，他对应的回答位于10~13行。。
    算法运用的原理为：统计问题列下，哪一行非空。这就表示这一行有问题，那么一直到
    下一个非空行（即下一个问题之前），右边所有的回答都属于这个问题。
    return:一个问题-答案的映射字典
    '''
    data = xlrd.open_workbook(excel_name)
    table = data.sheets()[0]
    question_list = []
    for rownum in range(table.nrows):
        data_list = []
        data_list.extend(table.row_values(rownum))
        if data_list[answer_col]:#如果问题列有文字，表示这一行是问题行。
            question_list.append(rownum)

    question_dic = {}
    for i in range(len(question_list)):
        try:
            question_dic[question_list[i]] = [question_list[i],question_list[i+1]]
        except:
            question_dic[question_list[i]] = [question_list[i],-1]
    return question_dic

def combineAnswerAndQuestionByCorrespongdingRow( excel_name,correspongding_row,answer_col=1,explain_col=2,result_col=6 ):
    '''
    根据行对应的字典（来自getCorrespongdingRow函数）——即一个问题对应多个回答。
    将问题、问题描述和回答进行拼接，返回拼接的数据集。
    读入文件路径为标注语料的路径；answer_col为问题列数。explain_col为问题描述列数。result_col为回答列数。
    思路为：correspongding_row是这样的字典：{1:[1:10]..}，键是问题数据的行数，值是答案的行数（默认问题和问题描述在同一行）
    所以result_data[1]就是问题，explain_data[1]是问题描述，answer_data[1:10]就是答案。三个字符串相加即可。
    return：将问题、问题描述以及答案拼接后，产生的新数据集。
    '''
    data = xlrd.open_workbook(excel_name)
    table = data.sheets()[0]
    result_data = table.col_values(result_col)
    answer_data = table.col_values(answer_col)    
    explain_data = table.col_values(explain_col)    
    data_set=[]
    for cur_key in correspongding_row.keys() :
        sentence = str(answer_data[cur_key])#这是问题数据       
        sentence = sentence+str(explain_data[cur_key])#这是问题描述数据
        result_start = correspongding_row[cur_key][0]
        result_end = correspongding_row[cur_key][1]
        for result in result_data[result_start:result_end]:#这是答案数据的列表
            sentence = sentence+str(result)
            if sentence[-1]!="。":#每进来一个新句子，如果结尾不是句号，认为加一个句号
                sentence+="。"
            else:
                pass
        data_set.append( deleteHTMLString( sentence ) )#删除HTML字符
    return data_set
    
if __name__=="__main__":    
    #excel_name = u'../docs/161202青年之声.xlsx'
    excel_name = u'../docs/161213数据1.xlsx'
    question_data = ricReadExcelCol( excel_name,1)
    #answer_data = ricReadExcelCol( excel_name,5)
    #correspongding_row = getCorrespongdingRow( excel_name )
    #combined_data_set = combineAnswerAndQuestionByCorrespongdingRow( excel_name,correspongding_row,answer_col=1,explain_col=3,result_col=5 )
    #trainWordToVectorModel(combined_data_set)