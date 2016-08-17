# -*- coding: utf-8 -*-
import json
import sys
import subprocess
import os
def Excute_Command(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    msg = p.stdout.readlines()
#     sometimes the network in not stable, try 10 time to connect
    if msg:
        return msg
    else:
        for a in range(1,11):
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            msg = p.stdout.readlines()
            if msg:
                return msg
            else:
                print "Fail to connect to ServiceNow host"
                
def List_Users(username, password,url):
    usercontentlist=[]
    cmd = ".\Tool\curl.exe  curl -s " +url +"/api/v2/users.json -u " + username + ":" + password
    cond=Excute_Command(cmd)
    usersDic=json.loads(cond[0])
    useraccounts=usersDic["count"]
    pages=int(useraccounts)/100
    for mypage in range(1,pages+2):
        cmd = ".\Tool\curl.exe  curl -s "+url+"/api/v2/users.json?page="+str(mypage)+" -u " + username + ":" + password
        cond=Excute_Command(cmd)
        temp_userdic1=json.loads(cond[0])
        temp_userdic2=temp_userdic1['users']
        usercontentlist.extend(temp_userdic2)
    i=1
    userattribute=["id","role","email","phone","ctive","name",]
    for a in range(len(usercontentlist)):
        usersDic=usercontentlist[a]
        print "*************  ",i,"  ***************"
        for k,v in usersDic.iteritems():
            if k in userattribute:
                if v:
                    print k,v
                else:
                    print k

        i+=1    
#     return useridlist
def Get_Email_User_list(emailsuffix,username, password,url):
    useridlist=[]
    usercontentlist=[]
    cmd = ".\Tool\curl.exe  curl  -s " +url+"/api/v2/users.json -u " + username + ":" + password
    cond=Excute_Command(cmd)
    usersDic=json.loads(cond[0])
    useraccounts=usersDic["count"]
    pages=int(useraccounts)/100
    for mypage in range(1,pages+2):
        cmd = ".\Tool\curl.exe  curl -s "+url+"/api/v2/users.json?page="+str(mypage)+" -u " + username + ":" + password
        
        cond=Excute_Command(cmd)
        temp_userdic1=json.loads(cond[0])
        temp_userdic2=temp_userdic1['users']
        usercontentlist.extend(temp_userdic2)
    i=1
    for a in range(len(usercontentlist)):
        usersDic=usercontentlist[a]
        for k,v in usersDic.iteritems():
            if k =="email":
                if emailsuffix in v:
                    useridlist.append(str(usersDic["id"]))
#                     print "id",usersDic["id"],"Role",usersDic["role"],"user name:",usersDic["name"],"email: ", usersDic["email"]
    
#     cmd = ".\Tool\curl.exe  curl " + url + "/api/v2/users.json -v -u " + username + ":" + password
#     cond1=Excute_Command(cmd)
#     usersDic=json.loads(cond1[0])
#     if "page=2" in usersDic["next_page"]:
#         cmd = ".\Tool\curl.exe  curl " +usersDic["next_page"] +" -v -u " + username + ":" + password
#         cond2=Excute_Command(cmd)
#     cond=cond1+cond2
#     i=1
#     for a in range(2):
#         usersDic=json.loads(cond[a])
#         for u in usersDic["users"]:
#             if emailsuffix in u["email"]:
#                 useridlist.append(str(u["id"]))
#                 print i,"id",u["id"],"Role",u["role"],"user name:",u["name"],"email: ", u["email"]
#                 i+=1
    return useridlist
def Create_User(username, password, url, create_username, create_user_email):
#     create_user = ".\Tool\curl.exe curl -v " + url + "/api/v2/users/create_or_update.json -u " + username + ":" + password + " -H \"Content-Type:application/json\" -X POST -d \"{\\\"user\\\":{\\\"name\\\":\\\"" + create_username + "\\\",\\\"email\\\":\\\"" + create_user_email + "\\\"}}"""
    create_user = ".\Tool\curl.exe curl -s " + url + "/api/v2/users/create_or_update.json -u " + username + ":" + password + " -H \"Content-Type:application/json\" -X POST -d \"{\\\"user\\\":{\\\"name\\\":\\\"" + create_username + "\\\",\\\"email\\\":\\\"" + create_user_email + "\\\"}}"""
    mystatuscode=Excute_Command(create_user)
    if mystatuscode:
        myuser=json.loads(mystatuscode[0])
        mydetailuser=myuser["user"]
        mydetailuseattribute=["id","name","email","created_at"]
        print "Create user successfully!"
        for k, v in mydetailuser.iteritems():
            if k in mydetailuseattribute:
                print k,v
    else:
        print "Fail to create user: ",create_user_email
    
    
    
def Search_User_ByEmail(queryuseremail, username, password,url):
#     search_user = ".\Tool\curl.exe curl " + url + "/api/v2/users/search.json?query=" + queryuseremail + " -v -u" + username + ":" + password 
    search_user = ".\Tool\curl.exe curl -s " + url + "/api/v2/users/search.json?query=" + queryuseremail + " -u" + username + ":" + password
    getuserid = Excute_Command(search_user)
    return getuserid
def Get_UserAttribute(result, userattribute):
    d2 = json.loads(result)
    print d2['users'][0][userattribute]
    return d2['users'][0][userattribute]
def Delete_User(userid,username,password,url,):
#     search user and then get its id, and delete user by id
    userid=str(userid)
#     delete_user = ".\Tool\curl.exe curl " + " -v -u " + username + ":" + password+" " + url+"/api/v2/users/{"+userid +"}.json" +" -X DELETE"
    delete_user = ".\Tool\curl.exe curl " + " -i -u " + username + ":" + password+" " +" -s "+ url+"/api/v2/users/{"+userid +"}.json" +" -X DELETE"
    mydeleteinfo=Excute_Command(delete_user)
    
    if "HTTP/1.1 200 OK" in mydeleteinfo[0]:
        print "Delete user successfully!",mydeleteinfo[0]
def Bulk_Delte_Users(emailsuffix,username,password,url):
    useridlist=Get_Email_User_list(emailsuffix, username, password, url)
    print len(useridlist)
    ids=""
    for uid in range(len(useridlist)):
        if len(useridlist)-1==uid:
            ids=ids+useridlist[uid]
        else:
            ids=ids+useridlist[uid]+","
    print ids
#     bulkdelet=".\Tool\curl.exe curl " + " -v -u " + username + ":" + password+" " + url+"/api/v2/users/destroy_many.json?ids="+ids  +" -X DELETE"
    bulkdelet=".\Tool\curl.exe curl " + " -i -u " + username + ":" + password+" " +" -s "+ url+"/api/v2/users/destroy_many.json?ids="+ids  +" -X DELETE"
    Excute_Command(bulkdelet)
    f=file("log.txt","a+")
   
    f.write("Finished to delte users, their id are: "+"\n")
    f.write(ids+"\n")
    f.close() 
    
    
def Get_User_Id_Bymail(queryuseremail,username, password,url): 
    userinfo=Search_User_ByEmail(queryuseremail, username, password, url)
    usersDic=json.loads(userinfo[0])
    userentity=usersDic["users"]
    for k in userentity:
        for mykey in k.keys():
            if mykey=="id":
                print k[mykey]
                return k[mykey]
        
'''   
#1 get all users list(inorder to find user email)
#2 create a user 
#3 query user detail info by email
#4 delete user by url
#5 buk delte user(email end with suffix)
'''



# username = "michael.yu@wesoft.com"
# password = "HBC3ntr1fy!"
# url = "https://centrifyhelpdesk1354579520.zendesk.com"
# create_user = "xidada"
# create_user_email = "albert.chen@centrify.com"
# emailsuffix="ccappstestsi8.net"
# create_username="hero"
# # # List_Users(username, password, url)
# # # Get_Email_User_list(emailsuffix,username, password,url)
# # Create_User(username, password, url, create_username, create_user_email)
# # Delete_User("5573583578", username, password,url)
# userlist=Search_User_ByEmail(create_user_email, username, password, url)
# usersDic=json.loads(userlist[0])
# resultdic=usersDic["users"]
# if resultdic:
#     detailuser=usersDic["users"][0]
#     for k,v in detailuser.iteritems():
#         print "%s: %s"%(k,v)
# else:
#     print "can not find this user",create_user_email



userinput=sys.argv[1:]
if userinput[0]=="querys":
    username=sys.argv[2]
    password=sys.argv[3]
    url=sys.argv[4]
    List_Users(username, password,url)
elif userinput[0]=="create":
    username=sys.argv[2]
    password=sys.argv[3]
    url=sys.argv[4]
    create_username=sys.argv[5]
    create_user_email=sys.argv[6]
    Create_User(username, password, url, create_username, create_user_email)
elif userinput[0]=="query":  
    username=sys.argv[2]
    password=sys.argv[3]
    url=sys.argv[4]
    create_user_email=sys.argv[5]
    userlist=Search_User_ByEmail(create_user_email, username, password, url)
    usersDic=json.loads(userlist[0])
    resultdic=usersDic["users"]
    if resultdic:
        detailuser=usersDic["users"][0]
        for k,v in detailuser.iteritems():
            print "%s: %s"%(k,v)
    else:
            print "can not find this user",create_user_email
elif userinput[0]=="delete":
    username=sys.argv[2]
    password=sys.argv[3]
    url=sys.argv[4]
    delete_user_email=sys.argv[5]
    userid=Get_User_Id_Bymail(delete_user_email, username, password, url)
    Delete_User(userid, username, password,url)
elif userinput[0]=="deletes":  
    emailsuffix=sys.argv[2]
    username=sys.argv[3]
    password=sys.argv[4]
    url=sys.argv[5]
    Bulk_Delte_Users(emailsuffix, username, password, url)
     








