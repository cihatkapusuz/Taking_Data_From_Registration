import sys
import csv
spamwriter = csv.writer(sys.stdout)
import requests
import re
shortdept=["ASIA","ASIA","ATA","AUTO","BM","BIS","CHE","CHEM","CE","COGS","CSE","CET","CMPE","INT","CEM","CCS","EQE","EC","EF","ED","CET","EE","ETM","ENV","ENVT","XMBA","FE","PA","FLED","GED","GPH","GUID","HIST","HUM","IE","INCT","MIR","MIR","INTT","INTT","LS","LING","AD","MIS","MATH","SCED","ME","MECA","BIO","PHIL","PE","PHYS","POLS","PRED","PSY","YADYOK","SCED","SPL","SOC","SWE","SWE","TRM","SCO","TRM","WTR","TR","TK","TKL","LL"]
dept=["ASIAN+STUDIES","ASIAN+STUDIES+WITH+THESIS","ATATURK+INSTITUTE+FOR+MODERN+TURKISH+HISTORY","AUTOMOTIVE+ENGINEERING","BIOMEDICAL+ENGINEERING","BUSINESS+INFORMATION+SYSTEMS","CHEMICAL+ENGINEERING","CHEMISTRY","CIVIL+ENGINEERING","COGNITIVE+SCIENCE","COMPUTATIONAL+SCIENCE+%26+ENGINEERING","COMPUTER+EDUCATION+%26+EDUCATIONAL+TECHNOLOGY","COMPUTER+ENGINEERING","CONFERENCE+INTERPRETING","CONSTRUCTION+ENGINEERING+AND+MANAGEMENT","CRITICAL+AND+CULTURAL+STUDIES","EARTHQUAKE+ENGINEERING","ECONOMICS","ECONOMICS+AND+FINANCE","EDUCATIONAL+SCIENCES","EDUCATIONAL+TECHNOLOGY","ELECTRICAL+%26+ELECTRONICS+ENGINEERING","ENGINEERING+AND+TECHNOLOGY+MANAGEMENT","ENVIRONMENTAL+SCIENCES","ENVIRONMENTAL+TECHNOLOGY","EXECUTIVE+MBA","FINANCIAL+ENGINEERING","FINE+ARTS","FOREIGN+LANGUAGE+EDUCATION","GEODESY","GEOPHYSICS","GUIDANCE+%26+PSYCHOLOGICAL+COUNSELING","HISTORY","HUMANITIES+COURSES+COORDINATOR","INDUSTRIAL+ENGINEERING","INTERNATIONAL+COMPETITION+AND+TRADE","INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST","INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST+WITH+THESIS","INTERNATIONAL+TRADE","INTERNATIONAL+TRADE+MANAGEMENT","LEARNING+SCIENCES","LINGUISTICS","MANAGEMENT","MANAGEMENT+INFORMATION+SYSTEMS","MATHEMATICS","MATHEMATICS+AND+SCIENCE+EDUCATION","MECHANICAL+ENGINEERING","MECHATRONICS+ENGINEERING","MOLECULAR+BIOLOGY+%26+GENETICS","PHILOSOPHY","PHYSICAL+EDUCATION","PHYSICS","POLITICAL+SCIENCE%26INTERNATIONAL+RELATIONS","PRIMARY+EDUCATION","PSYCHOLOGY","SCHOOL+OF+FOREIGN+LANGUAGES","SECONDARY+SCHOOL+SCIENCE+AND+MATHEMATICS+EDUCATION","SOCIAL+POLICY+WITH+THESIS","SOCIOLOGY","SOFTWARE+ENGINEERING","SOFTWARE+ENGINEERING+WITH+THESIS","SUSTAINABLE+TOURISM+MANAGEMENT","SYSTEMS+%26+CONTROL+ENGINEERING","TOURISM+ADMINISTRATION","TRANSLATION","TRANSLATION+AND+INTERPRETING+STUDIES","TURKISH+COURSES+COORDINATOR","TURKISH+LANGUAGE+%26+LITERATURE","WESTERN+LANGUAGES+%26+LITERATURES"]
interval1 = sys.argv[1]
interval2 = sys.argv[2]
start = 0
start123 = 0
if(interval1[5:]=="Fall"):
    start = int(interval1[:4])
    start123=1
elif(interval1[5:]=="Spring"):
    start = int(interval1[:4])-1
    start123=2
else:
    start = int(interval1[:4])-1
    start123=3
finish = 0
finish123 = 0

if(interval2[5:]=="Fall"):
    finish = int(interval2[:4])
    finish123=1
elif(interval2[5:]=="Spring"):
    finish = int(interval2[:4])-1
    finish123=2
else:
    finish = int(interval2[:4])-1
    finish123=3
foricin = (finish-start)*3+(finish123-start123)+1
years =[]
liste =["Dept./Prog.(name)","Course Code","Course Name"]
temp=interval1
for i in range(foricin):
    liste.append(temp)
    if(temp[5:]=="Fall"):
        years.append(str(int(temp[:4]))+"/"+str(int(temp[:4])+1)+"-1")
        temp = str(int(temp[:4])+1)+"-"+"Spring"
    elif(temp[5:]=="Spring"):
        years.append(str(int(temp[:4])-1)+"/"+str(int(temp[:4]))+"-2")
        temp = temp[:5]+"Summer"
    else:
        years.append(str(int(temp[:4])-1)+"/"+str(int(temp[:4]))+"-3")
        temp = temp[:5]+"Fall"


liste.append("Total Offerings")
spamwriter.writerow(liste)
sume=0
for i in range(len(dept)):
    #if(shortdept[i]=="YADYOK"):
    #    continue
    templist = []
    tempstring=shortdept[i]+"("+(dept[i].replace("+"," ").replace("%26","&").replace("%3a",":").replace("%2c",","))+")"
    templist.append(tempstring)
    tempname=[]
    temparr=[]
    tempinstructor=[]
    yearray=[]
    yearbyyear=[]
    tupleset =[]
    instructorset =[]
    for j in range(foricin):

        r = requests.get("https://registration.boun.edu.tr/scripts/sch.asp?donem={}&kisaadi={}&bolum={}".format(years[j],shortdept[i],dept[i]))
        coursecode = re.findall("font-size:12px'>([A-Z]+ *[0-9A-Z]{3})\.[0-9]{1,2}",r.text)
        coursenames = re.findall("Desc.[\D]+?<td>([^{]+?)&nbsp;</td>",r.text) #Desc.[\D]+<td>([\D]+?)&nbsp;</td>
        coursecodetemp = coursecode.copy()
        for k in range(len(coursecode)):
            tupleset.append((coursecode[k],coursenames[k]))
        coursecode = sorted(list(set(coursecode)))
        for k in range(len(coursecode)):
            temparr.append(coursecode[k])
        yearbyyear.append(coursecode)
        totalu =0
        totalg=0
        for k in range(len(coursecode)):
            if(coursecode[k][-3]=="5" or coursecode[k][-3]=="6" or coursecode[k][-3]=="7"): #coursecode[k][-3]=="5" or coursecode[k][-3]=="6" or coursecode[k][-3]=="7"  #int(coursecode[k][-3])>4
                totalg+=1
            else:
                totalu+=1

        yearray.append(totalu)
        yearray.append(totalg)

        totali = re.findall("Desc.[\D]+?<td>.+?&nbsp;</td>[\D]+?<td>[\S]*?&nbsp;</td>[\D]+?<td>[\S]*?&nbsp;</td>[\D]+?<td>([\D]+?)&nbsp;</td>",r.text) #totali = re.findall("Desc.[\D]+?<td>[\D]+?&nbsp;</td>[\D]+?<td>[\S]+?&nbsp;</td>[\D]+?<td>[\S]+?&nbsp;</td>[\D]+?<td>([\D]+?)&nbsp;</td>",r.text)

        totali2 = re.findall(">Info</a>&nbsp;</td>[\D]+?<td>([\D]+?)&nbsp;</td>",r.text)
        totali = totali+totali2

        while(len(totali)!=0):
            if(totali[0].startswith("&nbsp")):
                totali.pop(0)
            else:
                break

        for k in range(len(totali)):
            instructorset.append((coursecodetemp[k],totali[k]))
            tempinstructor.append(totali[k])
        yearray.append(len(set(totali)))
        sume=0
        for u in range(len(totali)):
            if(totali[u]=="STAFF STAFF"):
                sume+=1
        yearray[-1] = yearray[-1]-sume

    totalu =0
    totalg =0
    temparr = list(set(temparr))
    for k in range(len(temparr)):
            if(temparr[k][-3]=="5" or temparr[k][-3]=="6" or temparr[k][-3]=="7"):
                totalg+=1
            else:
                totalu+=1
    templist.append("U"+str(totalu)+" G"+str(totalg))
    templist.append("")
    totalofferingu=0
    totalofferingg=0
    #print(yearray)
    for j in range(foricin):
        templist.append("U"+str(yearray[3*j])+" G"+str(yearray[3*j+1])+" I"+str(yearray[3*j+2]))
        totalofferingu += yearray[3*j]
        totalofferingg += yearray[3*j+1]
    tempinstructor = list(set(tempinstructor))
    sume=0
    for u in range(len(tempinstructor)):
        if(tempinstructor[u]=="STAFF STAFF"):
            sume+=1

    templist.append("U"+str(totalofferingu)+" G"+str(totalofferingg)+" I"+str(len(tempinstructor)-sume))
    spamwriter.writerow(templist)
    ###print(templist)
    #print("temparr",sorted(temparr))
    tupleset = sorted(list(set(tupleset)))
    instructorset = sorted(list(set(instructorset)))
    for j in range(len(tupleset)):
        templist =[]
        templist.append("")
        templist.append(tupleset[j][0])
        templist.append(tupleset[j][1])
        numberofx=0
        for k in range(len(yearbyyear)):

            if(tupleset[j][0] in yearbyyear[k]):
                templist.append("x")
                numberofx+=1
            else:
                templist.append("")
        dinstructorcount=0
        for k in range(len(instructorset)):

            if(instructorset[k][0]==tupleset[j][0] and instructorset[k][1] != "STAFF STAFF"):
                dinstructorcount+=1
        templist.append(str(numberofx)+"/"+str(dinstructorcount))
        spamwriter.writerow(templist)
        ###print(templist)
