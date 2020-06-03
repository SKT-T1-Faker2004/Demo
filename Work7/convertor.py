a = 1
b = 2
c = 3
state = a
text = ''
path_in = input('文件的绝对路径: ')
path_out = input('输出的绝对路径: ')
with open(path_in, 'r') as f: #打开srt字幕文件，并去掉文件开头的\ufeff
   for line in f.readlines(): #遍历srt字幕文件
       if state == a: #跳过第一行
           state = b
       elif state == b: #跳过第二行
           state = c
       elif state == c: #读取第三行字幕文本
           if len(line.strip()) !=0:
               text += ' ' + line.strip() #将同一时间段的字幕文本拼接
               state = c
           elif len(line.strip()) ==0:
               with open(path_out + '/test.txt', 'a') as fa: #写入txt文本文件中
                   fa.write(text)
                   text = '\n'
                   state = a