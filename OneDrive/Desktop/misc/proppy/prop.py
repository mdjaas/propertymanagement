from tkinter import *
from functools import partial
import pickle
import mysql.connector
import re
import random
import smtplib
from datetime import date
mydb=mysql.connector.connect(host="localhost", user="root", passwd=" ", database="propertymanagement", buffered=True)
mycursor=mydb.cursor()
def retrieve():
  myuse=open("username.txt", "rb")
  mypwd=open("password.txt", "rb")
  use=pickle.load(myuse)
  pwd=pickle.load(mypwd)
  return use
use=retrieve()
pwd=retrieve()
notice=use
def file():
  myuse=open("username.txt","wb")
  mypwd=open("password.txt","wb")
  pickle.dump(use,myuse)
  pickle.dump(pwd,mypwd)
  myuse.close()
  mypwd.close()
  retrieve()
def unitmodification():
    a=Toplevel(tkWindow)
    community=StringVar()
    communityname=Label(a, text="community name").grid(row=0, column=0)
    communityentry=Entry(a, textvariable=community).grid(row=0, column=1)
    city=StringVar()
    cityname=Label(a, text="District").grid(row=1, column=0)
    cityentry=Entry(a, textvariable=city).grid(row=1, column=1)
    def addcommunity():
        communityname=StringVar()
        communitylabel=Label(a, text="Community name").grid(row=1, column=0)
        communityentry=Entry(a, textvariable=communityname).grid(row=1, column=1)
        street=StringVar()
        streetlabel=Label(a, text="street").grid(row=2, column=0)
        streetentry=Entry(a, textvariable=street).grid(row=2, column=1)
        district=StringVar()
        districtlabel=Label(a, text="District").grid(row=3, column=0)
        districtentry=Entry(a, textvariable=district).grid(row=3, column=1)
        state=StringVar()
        statelabel= Label(a, text="State").grid(row=4, column=0)
        stateentry=Entry(a, textvariable=state).grid(row=4, column=1)    
        def add():
          u=communityname.get()
          b=street.get()
          c=district.get()
          d=state.get()
          e=(u, b, c, d)
          r="insert into communities(communityname, street, district, state) values(%s,%s,%s,%s)"
          mycursor.execute(r, e)
          mydb.commit()
        addbutton=Button(a, text="add", command=add).grid(row=5, column=0)    
    def findcommunity():
        v=username.get()
        b=city.get()
        c=community.get()
        mycursor.execute("select district from communities where communityname='"+c+"'")
        for r in mycursor:
            if b in r:
              mycursor.execute("select type from ownersortenants where username='"+v+"'")
              for f in mycursor:
                  h="Owner"
                  if h in f: 
                    ownername=StringVar()
                    ownerlabel=Label(a, text="owner name").grid(row=0, column=0)
                    ownerentry=Entry(a, textvariable=ownername).grid(row=1, column=1)
                    unit=StringVar()
                    unitlabel=Label(a, text="unit number").grid(row=2, column=0)
                    unitEntry=Entry(a, textvariable=unit).grid(row=2, column=1)
                    bldg=StringVar()
                    bldglabel=Label(a, text="building").grid(row=3, column=0)
                    bldgentry=Entry(a, textvariable=bldg).grid(row=3, column=1)
                    def addunit(): 
                      br=ownername.get()
                      c=unit.get()
                      d=bldg.get()
                      mycursor.execute("select ownername from unitdetails")
                      for i in mycursor:
                        if br in i:
                          mycursor.execute("select unitno from unitdetails")
                          for m in mycursor:
                            if c in m:
                              mycursor.execute("select building from unitdetails")
                              for n in mycursor:
                                if d in n:
                                    mycursor.execute("select verification from unitdetails where ownername='"+br+"'")
                                    for o in mycursor:
                                      x="verified"
                                      if x in o:
                                        e="unit already added"
                                        f=Label(a, text=e).grid(row=5, column=0)
                                      else:
                                        mycursor.execute("update unitdetails set verification='verified' where ownername='"+br+"'")
                                        mydb.commit()
                    addunit=Button(a, text="Add unit", command=addunit).grid(row=4,column=0)  
                  else:
                    tenantname=StringVar()
                    tenantlabel=Label(a, text="Tenant name").grid(row=0, column=0)
                    tenantentry=Entry(a, textvariable=tenantname).grid(row=1, column=1)
                    unit=StringVar()
                    unitlabel=Label(a, text="unit number").grid(row=2, column=0)
                    unitEntry=Entry(a, textvariable=unit).grid(row=2, column=1)
                    bldg=StringVar()
                    bldglabel=Label(a, text="building").grid(row=3, column=0)
                    bldgentry=Entry(a, textvariable=bldg).grid(row=3, column=1)
                    def addtenantunit():
                        br=tenantname.get()
                        c=unit.get()
                        d=bldg.get()
                        mycursor.execute("select tenantname from tenantdetails")
                        for i in mycursor:
                            if br in i:
                                mycursor.execute("select unitno from tenantdetails")
                                for m in mycursor:
                                    if c in m:
                                        mycursor.execute("select building from tenantdetails")
                                        for n in mycursor:
                                            if d in n:
                                                mycursor.execute("select verification from tenantdetails")
                                                for o in mycursor:
                                                    x="verified"
                                                    if x in o:
                                                        e="unit already added"
                                                        f=Label(a, text=e).grid(row=5, column=0)
                                                    else:
                                                        mycursor.execute("update tenantdetails set verification='verified' where tenantname='"+br+"'")
                                                        mydb.commit()
                    addunit=Button(a, text="Add unit", command=addtenantunit).grid(row=4,column=0)                      
            else:
              addcommunity()                                  
    def verify(*verify):

      b=community.get()
      c=city.get()
      mycursor.execute("select communityname from communities")
      for i in mycursor:
          if b in i:
            for widgets in a.winfo_children():
                  widgets.destroy()
            findcommunity()  
          else:
            newvalidate=partial(addcommunity)
            select= Button(a, text="Add Now", command=newvalidate).grid(row=0, column=2) 
    selectvalidate=partial(verify)
    select= Button(a, text="Select", command=selectvalidate).grid(row=0, column=2)
          
while True:
  print("""1. Owners/ Tenants Login
2. Signup""")
  choice=int(input("enter what you want to do"))
  if choice==1:
    def login(username, password):
        a=username.get()
        b=password.get()
        if a in use:
            x=use.index(a)
            if b==pwd[x]:
                for widgets in tkWindow.winfo_children():
                  widgets.destroy()
                loginlabel=Label(tkWindow, text="hi " + a).grid(row=0, column=0)  
                menubar=Menu(tkWindow)
                unit=Menu(menubar, tearoff=0)
                def destroy():
                  unit.destroy()
                def myunit():
                   global w 
                   w=Toplevel(tkWindow)
                   mycursor.execute("select type from ownersortenants where username='"+a+"'")
                   p="Owner"
                   for k in mycursor:
                    if p in k: 
                     mycursor.execute("select ownername from unitdetails") 
                     for i in mycursor:
                      if a in i:
                       mycursor.execute("select verification from unitdetails where ownername='"+a+"'")
                       r="verified"
                       for m in mycursor:
                        if r in m:
                         mycursor.execute("select unitno from unitdetails where ownername='"+a+"'")
                         global n
                         for n in mycursor:
                           mycursor.execute("select building from unitdetails where ownername='"+a+"'")
                           global h
                           for h in mycursor:
                             unittilte=Label(w, text="Unitno").grid(row=0, column=0)
                             bldgtitle=Label(w, text="Building").grid(row=0, column=1)
                             unitlabel=Label(w, text=n).grid(row=1, column=0)
                             bldglabel=Label(w, text=h).grid(row=1, column=1)
                   mycursor.execute("select type from ownersortenants where username='"+a+"'")          
                   l="Tenant"
                   if l in k:
                       mycursor.execute("select tenantname from tenantdetails")
                       for i in mycursor:
                         if a in i:
                             mycursor.execute("select verification from tenantdetails where tenantname='"+a+"'")
                             r="verified"
                             for m in mycursor:
                                 if r in m:
                                     mycursor.execute("select unitno from tenantdetails where tenantname='"+a+"'")
                                     for n in mycursor:
                                         mycursor.execute("select building from tenantdetails where tenantname='"+a+"'")
                                         for h in  mycursor:
                                          unittilte=Label(w, text="Unitno").grid(row=0, column=0)
                                          bldgtitle=Label(w, text="Building").grid(row=0, column=1)
                                          unitlabel=Label(w, text=n).grid(row=1, column=0)
                                          bldglabel=Label(w, text=h).grid(row=1, column=1)                                    
                def addtenant():
                    l=Toplevel(tkWindow)
                    myunit()
                    w.destroy()
                    unitnumber=StringVar()
                    unitnum=Label(l, text="Unit number").grid(row=0, column=0)
                    unitentry=Entry(l, textvariable=unitnumber).grid(row=0,column=1)
                    bldg=StringVar()
                    bldglabel=Label(l, text="Building").grid(row=1, column=0)
                    bldgentry=Entry(l, textvariable=bldg).grid(row=1, column=1)
                    tenantunit=StringVar()
                    tenantlabel=Label(l, text="Tenant Name").grid(row=2, column=0)
                    tenantEntry=Entry(l, textvariable=tenantunit).grid(row=2, column=1)
                    def tenantdetails():
                      r=tenantunit.get()  
                      q=unitnumber.get()
                      g=bldg.get()
                      t=(r, q, g)
                      if q in n:
                        if g in h:
                         mycursor.execute("select username from ownersortenants")
                         for e in mycursor:
                            if r in e:
                              f="insert into tenantdetails(tenantname, unitno, building) values(%s,%s,%s)"
                              mycursor.execute(f, t)
                              mydb.commit()
                            else:
                              print("Tenant name does not exist")
                        else:
                          print("This unit not linked with your account")
                      else:  
                        print("This unit not linked with your account")
                    addtenantbutton=Button(l, text="Add Tenant", command=tenantdetails).grid(row=3,column=0)
                def paymaintenance():
                    myunit()
                    w.destroy()
                    global q
                    q=Toplevel(tkWindow)
                    datef="%Y/%m/%d"
                    today=date.today()
                    mycursor.execute("select duedate from maintenance where unitno='"+n[0]+"' and building='"+h[0]+"'")
                    for ee in mycursor:
                        if ee[0]>today:
                         mycursor.execute("select balanceamount from maintenance where unitno='"+n[0]+"' and building='"+h[0]+"'")
                         for u in mycursor:
                          maintenanceunit=Label(q, text=n).grid(row=0,column=0)
                          maintenancebldg=Label(q, text=h).grid(row=0, column=1)
                          maintenancelabel=Label(q, text=u).grid(row=0,column=2)
                        elif ee[0]<today:
                         mycursor.execute("select maintenanceamount from maintenance where unitno='"+n[0]+"' and building='"+h[0]+"'")
                         for www in mycursor:
                          mycursor.execute("select paidamount from maintenance where unitno='"+n[0]+"' and building='"+h[0]+"'")
                          for hhh in mycursor:                              
                           daydiff=ee[0]-today
                           jj=daydiff.days*-1
                           fine=10/100*www[0]*jj+www[0]
                           finea=10/100*www[0]*jj
                           qqq=fine-hhh[0] 
                           mycursor.execute("select fine from maintenance where unitno='"+n[0]+"' and building='"+h[0]+"'")
                           for iii in mycursor:
                               if iii[0]==finea:
                                qqe=www[0]+iii[0]-hhh[0]   
                                maintenanceunit=Label(q, text=n).grid(row=0,column=0)
                                maintenancebldg=Label(q, text=h).grid(row=0, column=1)
                                maintenancelabel=Label(q, text=qqe).grid(row=0,column=2)
                               else:
                                ooo=finea-iii[0]   
                                mycursor.execute("update maintenance set fine='"+str(ooo)+"' where unitno='"+n[0]+"' and building='"+h[0]+"'")
                                mycursor.execute("select balanceamount from maintenance where unitno='"+n[0]+"' and building='"+h[0]+"'")
                                for uuu in mycursor:
                                 eer=uuu[0]+finea
                                 mycursor.execute("update maintenance set balanceamount='"+str(eer)+"' where unitno='"+n[0]+"' and building='"+h[0]+"'")                                
                                 mydb.commit()
                                 maintenanceunit=Label(q, text=n).grid(row=0,column=0)
                                 maintenancebldg=Label(q, text=h).grid(row=0, column=1)
                                 maintenancelabel=Label(q, text=qqq).grid(row=0,column=2)                         
                        global pay
                        def pay():
                            for widgets in q.winfo_children():
                                widgets.destroy()
                            amount=IntVar()
                            amountlabel=Label(q, text="enter amount").grid(row=0, column=0)
                            amountentry=Entry(q, textvariable=amount).grid(row=0, column=1)
                            card=IntVar()
                            cardlabel=Label(q, text="Card Number").grid(row=1,column=0)
                            cardnum=Entry(q, textvariable=card).grid(row=1,column=1)
                            cardholder=StringVar()
                            cardname=Label(q, text="Name on Card").grid(row=2, column=0)
                            name=Entry(q, textvariable=cardholder).grid(row=2, column=1)
                            cvv=IntVar()
                            cvvlabel=Label(q, text="CVV").grid(row=3, column=0)
                            cvventry=Entry(q,textvariable=cvv).grid(row=3, column=1)
                            def paynow():
                                v=username.get()
                                p=amount.get()
                                b=str(amount.get())
                                s=cardholder.get()
                                m=card.get()
                                l=cvv.get()
                                mycursor.execute("select cardholdername from bankaccount")
                                for e in mycursor:
                                    if s in e:
                                        mycursor.execute("select cardnumber from bankaccount")
                                        for t in mycursor:
                                            if m in t:
                                              mycursor.execute("select cvv from bankaccount")
                                              for r in mycursor:
                                                  if l in r: 
                                                     mycursor.execute("select bankbalance from bankaccount where cardholdername='"+s+"'")
                                                     for d in mycursor:
                                                      if p<int(d[0]):
                                                       mycursor.execute("select email from bankaccount where cardnumber='"+str(m)+"'")
                                                       c=random.randint(1000,9999)
                                                       for bb in mycursor:
                                                        oo=bb[0]   
                                                        content="the otp for the transaction is"+str(c)
                                                        mail=smtplib.SMTP("smtp.gmail.com", 587)
                                                        mail.ehlo()
                                                        mail.starttls()
                                                        mail.login("projects.python2021@gmail.com","pythonproject$")
                                                        mail.sendmail("projects.python2021@gmail.com",oo, content)
                                                        mail.close()
                                                        otp=IntVar()
                                                        otplabel=Label(q, text="OTP").grid(row=5, column=0)
                                                        otpentry=Entry(q, textvariable=otp).grid(row=5, column=1)
                                                       def otpemail(): 
                                                        otpget=otp.get()
                                                        if otpget==c:
                                                           for widgets in q.winfo_children():
                                                               widgets.destroy()
                                                           paid=Label(q, text="Paid"+str(p), font='Helvetica 18 bold').grid(row=0, column=0)
                                                           mycursor.execute("select paidamount from maintenance where unitno='"+n[0]+"' and building='"+h[0]+"'")
                                                           for t in mycursor:
                                                             dd=str(int(t[0])+p)
                                                             mycursor.execute("update maintenance set paidamount='"+dd+"' where unitno='"+n[0]+"' and building='"+h[0]+"'")
                                                             mycursor.execute("select balanceamount from maintenance where unitno='"+n[0]+"' and building='"+h[0]+"'")
                                                             for o in mycursor:
                                                              mycursor.execute("select fine from maintenance where unitno='"+n[0]+"' and building='"+h[0]+"'")
                                                              for rrr in mycursor:
                                                               f=str(int(o[0])-p)
                                                               mycursor.execute("update maintenance set balanceamount='"+f+"' where unitno='"+n[0]+"' and building='"+h[0]+"'")
                                                               if rrr[0]<p or o[0]<=0:
                                                                  mycursor.execu
                                                                  te("update maintenance set fine=0 where unitno='"+n[0]+"' and building='"+h[0]+"'") 
                                                               mycursor.execute("select bankbalance from bankaccount where cardnumber='"+str(m)+"'")
                                                               for cc in mycursor:
                                                                  qq=str(int(cc[0])-p)
                                                                  mycursor.execute("update bankaccount set bankbalance='"+qq+"' where cardnumber='"+str(m)+"'")
                                                               mydb.commit()  
                                                        else:
                                                           incorrectotp=Label(q, text="Transaction Failed").grid(row=6,column=0)     
                                                      else:
                                                       unpaid=Label(q,text="you do not have sufficint balance").grid(row=6, column=0)
                                                  else:
                                                    incorrectcard=Label(q, text="Transaction Failed").grid(row=6, column=0)
                                            else:
                                                incorrectcard=Label(q, text="Transaction Failed").grid(row=6, column=0)
                                    else:
                                        incorrectcard=Label(q, text="Transaction Failed").grid(row=6, column=0)
                                    otpbutton=Button(q, text="Pay Now", command=otpemail).grid(row=6, column=0)            
                            paynow=Button(q, text="Pay", command=paynow).grid(row=4,column=0)
                        paybutton=Button(q, text="Pay", command=pay).grid(row=1, column=0)
                def charges():
                    paymaintenance()
                    q.destroy()
                def movein():
                    charges()
                    global q
                    q=Toplevel(tkWindow)
                    mycursor.execute("select remarks from maintenance where unitno='"+n[0]+"' and building='"+h[0]+"'")
                    for cc in mycursor:
                        if cc[0]=="moveinorout":
                          mycursor.execute("select balanceamount from maintenance where unitno='"+n[0]+"' and building='"+h[0]+"'")
                          for jj in mycursor:
                           labelcharge=Label(q, text="Move in/out charge").grid(row=0, column=0)
                           payment=Label(q, text=jj).grid(row=0, column=1)
                           Pay=Button(q, text="Pay", command=pay).grid(row=1, column=0)
                def raisemaintenance():
                  k=Toplevel(tkWindow)
                  myunit()
                  w.destroy()
                  unitno=StringVar()
                  unitlabel=Label(k, text="Unit number").grid(row=0, column=0)
                  unitentry=Entry(k, textvariable=unitno).grid(row=0, column=1)
                  building=StringVar()
                  buildinglabel=Label(k, text="Bulding").grid(row=1, column=0)
                  buildingentry=Entry(k, textvariable=building).grid(row=1, column=1)
                  def request():
                    tt=unitno.get()
                    ii=building.get()
                    mycursor.execute("select followup from maintenancerequest where unitno='"+tt+"' and building='"+ii+"'")
                    for l in mycursor:
                     previousrequest=Label(k, text="previous request follow up"+str(l)).grid(row=8,column=0)
                    if tt in n:
                      if ii in h:
                        maint=StringVar()
                        label=Label(k, text="Description").grid(row=2, column=0)
                        entry=Entry(k, textvariable=maint).grid(row=2, column=1)
                        def post():
                          xx=maint.get()
                          ff=(tt,ii, xx)
                          j="insert into maintenancerequest(unitno, building, description) values(%s,%s, %s)"
                          mycursor.execute(j, ff)
                          mydb.commit()
                          mycursor.execute("select requestid from maintenancerequest where description='"+xx+"' and unitno='"+n[0]+"' and building='"+h[0]+"'")
                          for pp in mycursor:
                            o="your request id"+str(pp[0])
                            mycursor.execute("update maintenancerequest set status='Open' where requestid='"+str(pp[0])+"'")
                            mydb.commit()
                            requestid=Label(k, text=o).grid(row=7, column=0)
                        postbutton=Button(k, text="Post", command=post).grid(row=3, column=0)  
                      else:
                        maintlabel=Label(k, text="Building not linked").grid(row=5, column=0)
                    else:
                      maintlabel=Label(k, text="unit not linked").grid(row=4, column=0)
                  requestbutton=Button(k, text="Post", command=request).grid(row=3, column=0)  
                def logout():
                  for widgets in tkWindow.winfo_children():
                    widgets.destroy()
                  usernameLabel = Label(tkWindow, text="Username").grid(row=0, column=0)
                  usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)                   
                  check()
                menubar.add_command(label="Home", command=destroy)
                unit.add_command(label="Add/Remove unit", command=unitmodification) 
                unit.add_command(label="My Unit", command=myunit)
                unit.add_command(label="Pay Maintenance charges", command=paymaintenance)
                unit.add_command(label="Move in/out charge", command=movein)
                unit.add_command(label="Raise maintenance request", command=raisemaintenance)
                mycursor.execute("select type from ownersortenants where username='"+a+"'")
                for t in mycursor:
                    u="Owner"
                    if u in t:                
                      unit.add_command(label="Add Tenant", command=addtenant)
                unit.add_command(label="Logout", command=logout)      
                menubar.add_cascade(label="My Account", menu=unit)
                tkWindow.config(menu=menubar)
                print("""What you want to do?
                1. Add/Remove Unit
                2. Raise Maintenance Request
                3. Pay maintenance""")
                if a=="admin": 
                  for widgets in tkWindow.winfo_children():
                      widgets.destroy()
                  def viewowners(): 
                     
                     e=Toplevel(tkWindow) 
                     mycursor.execute("select ownername, unitno, building, community from unitdetails")
                     r=0
                     for i in mycursor:
                       for j in range(len(i)):
                         memberlabel=Label(e, text="Owner name").grid(row=0,column=0)
                         memberlabel1=Label(e, text="Unit Number").grid(row=0, column=1)
                         memberlabel2=Label(e, text="Building").grid(row=0, column=2)
                         memberlabel3=Label(e, text="Community").grid(row=0, column=3)
                         ownersandtenants=Entry(e, fg='green')
                         ownersandtenants.grid(row=r+1, column=j)
                         ownersandtenants.insert(END, i[j])
                       r+=1
                     ownername=StringVar()
                     ownernamelabel=Label(e, text="Owner name").grid(row=r+3, column=0)
                     ownernameentry=Entry(e, textvariable=ownername).grid(row=r+3, column=1)
                     unitname=StringVar()
                     unitlabel=Label(e, text="Unit Number").grid(row=r+4, column=0)
                     unitentry=Entry(e, textvariable=unitname).grid(row=r+4,column=1)
                     building=StringVar()
                     buildinglabel=Label(e, text="Building").grid(row=r+5, column=0)
                     buildingentry=Entry(e, textvariable=building).grid(row=r+5, column=1)
                     community=StringVar()
                     communitylabel=Label(e, text="Community").grid(row=r+6, column=0)
                     communityentry=Entry(e, textvariable=community).grid(row=r+6, column=1)
                     def addowner(*args):
                          s=ownername.get()
                          j=unitname.get()
                          l=building.get()
                          v=community.get()
                          f=(s,j,l,v)
                          g="insert into unitdetails(ownername, unitno, building, community) values(%s, %s, %s, %s)"
                          mycursor.execute(g, f)
                          mydb.commit()
                          labeldone=Label(e, text="Owner Successfully added").grid(row=r+8, column=0)  
                     addownerb=Button(e, text="Add Owner", command=addowner).grid(row=r+7, column=0)
                     e.bind('<Return>', addowner)
                  def viewtenants():
                     u=Toplevel(tkWindow)
                     r=0
                     mycursor.execute("select tenantname, unitno, building, community from tenantdetails")
                     for i in mycursor:
                       for j in range(len(i)):
                         label1=Label(u, text="Tenant Name").grid(row=0, column=0)
                         label2=Label(u, text="Unit no.").grid(row=0, column=1)
                         label3=Label(u, text="Building").grid(row=0, column=2)
                         label4=Label(u, text="Community").grid(row=0, column=3)
                         d=Entry(u, fg='green')
                         d.grid(row=r+1, column=j)
                         d.insert(END, i[j])
                       r+=1
                  def maintenanceview():
                     v=Toplevel(tkWindow)
                     r=0
                     mycursor.execute("select * from maintenance")
                     for i in mycursor:
                       for j in range(len(i)):
                         label1=Label(v, text="Owner or Tenant").grid(row=0, column=0)
                         label2=Label(v, text="Unit No").grid(row=0, column=1)
                         label3=Label(v, text="Building").grid(row=0, column=2)
                         label4=Label(v, text="Community").grid(row=0, column=3)
                         label5=Label(v, text="Maintenance").grid(row=0, column=4)
                         label6=Label(v, text="Paid").grid(row=0, column=5)
                         label10=Label(v,text="Fine").grid(row=0, column=6)
                         label7=Label(v, text="Balance").grid(row=0, column=7)
                         label8=Label(v, text="Sq ft").grid(row=0, column=8)
                         label9=Label(v, text="Remarks").grid(row=0, column=9)
                         label11=Label(v, text="Due Date").grid(row=0, column=10)
                         u=Entry(v, fg='green')
                         u.grid(row=r+1, column=j)
                         u.insert(END, i[j])
                       r+=1
                  def maintenancerequestview():
                    p=Toplevel(tkWindow)
                    mycursor.execute("select unitno, building, description, requestid, status from maintenancerequest where status='Open'")
                    r=0
                    for i in mycursor:
                       for j in range(len(i)):
                         label1=Label(p, text="unitno").grid(row=0, column=0)
                         label2=Label(p, text="Building").grid(row=0, column=1)
                         label4=Label(p,text="Request Id").grid(row=0, column=3)
                         label5=Label(p, text="Status").grid(row=0, column=4)
                         u=Entry(p, fg='green')
                         u.grid(row=r+1, column=j)
                         u.insert(END, i[j])
                       r+=1  
                    followup=StringVar()
                    followuplabel=Label(p, text="Follow up").grid(row=r+2, column=0)
                    follwupentry=Entry(p, textvariable=followup).grid(row=r+2, column=1)
                    requestids=IntVar()
                    requestidlabel=Label(p, text="Request id").grid(row=r+3, column=0)
                    requestentry=Entry(p, textvariable=requestids).grid(row=r+3, column=1)
                    status=StringVar()
                    statuslabel=Label(p, text="Status").grid(row=r+4, column=0)
                    statusentry=Entry(p, textvariable=status).grid(row=r+4, column=1)
                    def close():
                           d=str(requestids.get())
                           g=followup.get()
                           t=status.get()
                           mycursor.execute("update maintenancerequest set followup='"+g+"' where requestid='"+d+"'")
                           mycursor.execute("update maintenancerequest set status='"+t+"' where requestid='"+d+"'")
                           mydb.commit()
                           label=Label(p, text="Request followup updated").grid(row=r+6, column=0)
                    delbutton=Button(p, text="Close", command=close).grid(row=r+5, column=0)
                    p.bind('<Return>', close)
                  def addmaintenance():
                    y=Toplevel(tkWindow)
                    maint=IntVar()
                    maintlabel=Label(y, text="Maintenance amount/ sqft").grid(row=0, column=0)
                    maintentry=Entry(y, textvariable=maint).grid(row=0, column=1)
                    duedate=StringVar()
                    duedatel=Label(y, text="Due date").grid(row=1, column=0)
                    duedatee=Entry(y, textvariable=duedate).grid(row=1, column=1)
                    def add():
                      h=maint.get()
                      b=duedate.get()
                      mycursor.execute("select sqft from maintenance")
                      for yy in mycursor:
                        c=str(int(yy[0])*h)
                        mycursor.execute("update maintenance set maintenanceamount='"+c+"'")
                        mycursor.execute("update maintenance set paidamount=0")
                        mycursor.execute("update maintenance set duedate='"+b+"'")
                        mydb.commit()
                        mycursor.execute("select balanceamount from maintenance")
                        for k in mycursor:
                         r=str(int(k[0])+h*yy[0])
                         mycursor.execute("update maintenance set balanceamount=maintenanceamount+balanceamount")
                         mydb.commit()
                        label=Label(y,text="Maintenance added").grid(row=3, column=0)  
                    addbutton=Button(y, text="Add", command=add).grid(row=2, column=0)
                    y.bind('<Return>', add)
                  menubar = Menu(tkWindow)
                  admin = Menu(menubar, tearoff=0)    
                  admin.add_command(label="Owners", command=viewowners)
                  admin.add_command(label='Tenant', command=viewtenants)
                  admin.add_command(label='Maintenance received', command=maintenanceview)
                  admin.add_command(label='Maintenance request', command=maintenancerequestview)
                  admin.add_command(label='Add maintenance', command=addmaintenance)
                  admin.add_command(label='Logout', command=logout)
                  menubar.add_cascade(label="Manage Community", menu=admin)
                   
                  tkWindow.config(menu=menubar)        
                  #print("""What you want to do?
                  #1. View monthly expense
                  #2. View maintenance request
                  #3. View maintenance transactions
                  #4. View Pending maintenance transacctions
                  #5. Add quarterly maintenance
                  #6. Create community notice""")
                  pass
            else:
                print("incorrect password")
        else:
            print("incorrect user")

    tkWindow = Tk()  
    tkWindow.geometry('400x300')  
    tkWindow.title('Community Management Login')
    usernameLabel = Label(tkWindow, text="Username").grid(row=0, column=0)
    global username
    username = StringVar()
    usernameEntry = Entry(tkWindow, textvariable=username, width='30').grid(row=0, column=1)
    def logout():
        for widgets in tkWindow.winfo_children():
            widgets.destroy()
        usernameLabel = Label(tkWindow, text="Username").grid(row=0, column=0)
        usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)                   
        check()    
    def usercheck(*args):
      a=username.get()
      if a in use:
        passwordLabel = Label(tkWindow,text="Password").grid(row=1, column=0)  
        password = StringVar()
        passwordEntry = Entry(tkWindow, textvariable=password, show='*', width='30').grid(row=1, column=1)
        usernameEntry = Entry(tkWindow, textvariable=username, state=DISABLED, width='30').grid(row=0, column=1)
        validateLogin = partial(login, username, password)
        usernamebutton= Button(tkWindow, text="Login", command=validateLogin, state=DISABLED).grid(row=4, column=0)
        back=Button(tkWindow, text="Back", command=logout).grid(row=4, column=1)
        def passchk(*pwd):
            m=password.get()
            if m:
               usernamebutton= Button(tkWindow, text="Login", command=validateLogin).grid(row=4, column=0)
            else:
               usernamebutton= Button(tkWindow, text="Login", command=validateLogin, state=DISABLED).grid(row=4, column=0)
        password.trace("w", passchk)   
      else:
        passwordLabel = Label(tkWindow,text="Password").grid(row=1, column=0)  
        password = StringVar()
        passwordEntry = Entry(tkWindow, textvariable=password, show='*', state=DISABLED, width='30').grid(row=1, column=1)
        print("incorrect user id")
    validate=partial(usercheck)
    usernamebutton= Button(tkWindow, text="Next", command=validate, state=DISABLED).grid(row=4, column=0)
    def check(*user):
        a=username.get()
        if a:
          usernamebutton= Button(tkWindow, text="Next", command=validate).grid(row=4, column=0)
        else:
          usernamebutton= Button(tkWindow, text="Next", command=validate, state=DISABLED).grid(row=4, column=0)
    username.trace("w",check)
    tkWindow.bind('<Return>', usercheck)
    tkWindow.mainloop()
  if choice==2:
    def signup(*args):
      emailvalid=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.com'  
      a=username.get()
      b=password.get()
      c=fname.get()
      d=sname.get()
      e=email.get()
      f=types.get()
      g=(c, d, a, f, e)
      if re.match(emailvalid, e):
        pass
      else:
        print("please enter a valid email")  
      if a in use:
        print("username already in use, select another")
      else:
        use.append(a)
        pwd.append(b)
        print("account created successfully")
        file()
        retrieve()
        mycursor.execute("use propertymanagement")
        insert="insert into ownersortenants(firstname, secondname, username, type, email) values(%s, %s, %s, %s, %s)"
        mycursor.execute(insert, g)
        mydb.commit()
    tkWindow=Tk()
    tkWindow.geometry('400x150')
    tkWindow.title("Community management Signup")
    fnamelabel= Label(tkWindow, text="First Name").grid(row=0, column=0)
    fname= StringVar()
    fentry= Entry(tkWindow, textvariable=fname).grid(row=0, column=1)
    sname= StringVar()
    snamelabel= Label(tkWindow, text="second Name").grid(row=0, column=2)
    snameentry=Entry(tkWindow, textvariable=sname).grid(row=0, column=3)
    username= StringVar()
    usernameLabel= Label(tkWindow, text="Username").grid(row=1, column=0)
    usernameEntry= Entry(tkWindow, textvariable=username).grid(row=1, column=1)
    email=StringVar()
    emaillabel= Label(tkWindow, text="Email Id").grid(row=1, column=2)
    emailentry= Entry(tkWindow, textvariable=email).grid(row=1, column=3)
    password= StringVar()
    passwordLabel= Label(tkWindow, text="Password").grid(row=2, column=0)
    passwordEntry= Entry(tkWindow, textvariable=password, show="*").grid(row=2, column=1)
    types=StringVar()
    choice=["Owner", "Tenant"]
    typesdropdown= OptionMenu(tkWindow, types, *choice).grid(row=2, column=3)
    typeslabel= Label(tkWindow, text="Owner/Tenant").grid(row=2, column=2)
    signupvalidate= partial(signup)
    signupbutton= Button(tkWindow, text="Signup", command=signupvalidate, state=DISABLED).grid(row=3, column=0)
    tkWindow.bind('<Return>', signup)
    def checksignup(*signup):
        emailvalid=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.com'
        a=fname.get()
        b=username.get()
        c=password.get()
        d=email.get()
        f=types.get()
        e=re.match(emailvalid, d)
  
        if a and b and c and d and e and f:
           signupbutton= Button(tkWindow, text="Signup", command=signupvalidate).grid(row=3, column=0)
        else:
           signupbutton= Button(tkWindow, text="Signup", command=signupvalidate, state=DISABLED).grid(row=3, column=0)
    fname.trace("w", checksignup)
    username.trace("w", checksignup)
    password.trace("w", checksignup)
    email.trace("w", checksignup)
    types.trace("w", checksignup) 
    tkWindow.mainloop()
