#!/usr/bin/env python
# coding=utf-8

#author:phantomer
#github:https://github.com/rootphantomer
#weibo:http://weibo.com/527819757


def jiahouzhui():
    txt=raw_input("字典名:")
    file=open(txt,"r+")
    lines=file.readlines()
    file.close()
    write=raw_input("要加入的后缀名:")
    file1=open("name.txt","w+")
    for line in lines:
        line=line.strip('\n')
        file1.write(line+write)
    file1.close()

def main():
    jiahouzhui()


if __name__=='__main__':
    main()
