import re

def delete_HTML_string( sentence ):
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