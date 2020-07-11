from tkinter import *
from tkinter import ttk

import tkinter.font as font
from tkinter.colorchooser import *
from tkinter import messagebox
from tkinter import filedialog

from Model import *

from PIL import Image as PILImage
from PIL import ImageTk as PILImageTk

import pickle

from matplotlib import pyplot as plt



class loadingWindow:
    def __init__(self,root):
        self.root=root
        root.title('Loading...')

        framepic=ttk.Frame(root)
        framepic.grid(row=0,sticky=(W,E))

        load=PILImage.open("pics/background.png")
        self.render = PILImageTk.PhotoImage(load)
        
        img=Label(framepic,image=self.render)
        img.grid()
        
        self.root.after(1000,self.loaddata)
        self.center()
        

    def loaddata(self):               
        refreshingData=FetchData()
        getlocation=Location.getLocation()
        
        if refreshingData==True:
           print('data updated!') 
        else:
            print('could not update data will show older version')
            
        
        if getlocation==True:
            print('you are in',Location.country)
        else:
            print('could not get Location')

        self.root.destroy()

    def center(self):
        
        self.root.update_idletasks()  # Update "requested size" from geometry manager
        
        windowWidth = self.root.winfo_reqwidth()
        windowHeight = self.root.winfo_reqheight()

        positionRight = int(self.root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.root.winfo_screenheight()/2 - windowHeight/2)
        self.root.geometry("+{}+{}".format(positionRight, positionDown))
        
        
        self.root.overrideredirect(True)

########################################################################################


class adminPanel:
    def __init__(self,root,data):
        self.root=root
        self.feedbacks=data['feedbacks']
        self.userpass=data['userpass']

        root.title('Admin Panel')

        self.i=0
        i=self.i

        self.frame=ttk.LabelFrame(root,padding=(5,10),text='review #'+str(self.i+1))
        frame=self.frame
        
        ttk.Label(frame,text='Name:', font='Helvetica 13 bold').grid(sticky=(W))
        self.labelName=ttk.Label(frame,text=self.feedbacks[i]['name'], font='Helvetica 13')
        self.labelName.grid(sticky=(W))
            
        ttk.Label(frame,text='Email:', font='Helvetica 13 bold').grid(sticky=(W))
        self.labelEmail=ttk.Label(frame,text=self.feedbacks[i]['emailaddress'], font='Helvetica 13')
        self.labelEmail.grid(sticky=(W))
            
        ttk.Label(frame,text='Message:', font='Helvetica 13 bold').grid(sticky=(W))
        self.labelMessage=ttk.Label(frame,text=self.feedbacks[i]['message'], font='Helvetica 13')
        self.labelMessage.grid(sticky=(W))
            
        ttk.Label(frame,text='Stars:', font='Helvetica 13 bold').grid(sticky=(W))                                                                     
        self.labelStar=ttk.Label(frame,text=self.feedbacks[i]['stars'], font='Helvetica 13')
        self.labelStar.grid(sticky=(W))

        frame.grid(padx=10,pady=10)

        frame2=ttk.Frame(root,padding=(5,10))
        frame2.grid(padx=10,pady=10)

        btn3=ttk.Button(frame2,text='Send Message',command=self.SendMsg)
        btn3.grid(row=0,column=0,columnspan=2,sticky=(W,E))

        self.btn1=ttk.Button(frame2,text='Back',state='disabled',command=self.Back)
        self.btn1.grid(row=1,column=0,sticky=(W,E))
        self.btn2=ttk.Button(frame2,text='Next',command=self.Next)
        self.btn2.grid(row=1,column=1,sticky=(W,E))


        root.rowconfigure(0,weight=1)
        root.columnconfigure(0,weight=1)
        root.rowconfigure(1,weight=1)
        root.columnconfigure(0,weight=1)

    def SendMsg(self):
        mail=self.labelEmail['text']
        sendmail(mail,self.userpass['user'],self.userpass['pass'])

    def Next(self):

        if self.i<len(self.feedbacks)-1:
            self.i=self.i+1
            self.refreshButtons()
        
    def Back(self):
        if self.i>0:
            self.i=self.i-1
            self.refreshButtons()
        

    def refreshButtons(self):
        if self.i==0:
            self.btn1['state']='disabled'
        else:
            self.btn1['state']='normal'
            
        if self.i==len(self.feedbacks)-1:
            self.btn2['state']='disabled'
        else:
            self.btn2['state']='normal'
          
            
        self.labelName['text']=self.feedbacks[self.i]['name']
        self.labelEmail['text']=self.feedbacks[self.i]['emailaddress']
        self.labelMessage['text']=self.feedbacks[self.i]['message']
        self.labelStar['text']=self.feedbacks[self.i]['stars']

        self.frame['text']='review #'+str(self.i+1)



#########################################################################################################################4





class baseWindow:
    def initSV(self):
        self.SV=[]
        for elm in self.language:
            self.SV.append(StringVar())
    def french(self):
        for i in range(len(self.SV)):
            self.SV[i].set(self.language[i][1])
    def english(self):
        for i in range(len(self.SV)):
            self.SV[i].set(self.language[i][0])
        
    def checklanguage(self):
        
        if str(type(self))=="<class '__main__.locationWindow'>" or str(type(self))=="<class 'GUI.locationWindow'>":
            lang=self.preventionsWindow.configs['language']
        elif str(type(self))=="<class '__main__.mainWindow'>" or str(type(self))=="<class 'GUI.mainWindow'>":
            lang=self.configs['language']
        else:    
            lang=self.mainWindowInstance.configs['language']
            
        if lang=='english':
            self.english()
        if lang=='french':
            self.french()    


    def goBack(self):
        self.fenetre.destroy()
        self.root.deiconify()

    def setIcon(self):
        self.fenetre.iconbitmap('pics/icon2.ico')

    def setStyle(self):
        s=ttk.Style()
        s.configure('TFrame', background='white')
        s.configure('TLabelframe', background='white')
        s.configure('TLabelframe.Label', foreground='black', background='white')
        s.configure('TLabel', background='white')
        
        s.configure('new.TFrame', background='SystemButtonFace')
        s.configure('new.TLabel', background='SystemButtonFace')
        
    def initTopWindows(self,mainWindowInstance,title=''):
        self.mainWindowInstance=mainWindowInstance
        
        self.root=mainWindowInstance.root
        self.fenetre=Toplevel(self.root)
        self.root.withdraw()

        self.fenetre.title(title)
        self.setIcon()

        self.fenetre.protocol('WM_DELETE_WINDOW', self.root.destroy)




class introWindow(baseWindow):
    def __init__(self,mainWindowInstance):
        self.initTopWindows(mainWindowInstance,"Repartitions des cas du Covid-19 selon les pays")
         
        root=self.root
        fenetre=self.fenetre
        
        color=mainWindowInstance.configs['color']
        fontSize=mainWindowInstance.configs['fontSize']
        
        myFont = font.Font(fenetre,size=fontSize+2,weight='bold')
        myFont2 = font.Font(fenetre,size=fontSize)
        myFont3 = font.Font(fenetre,size=fontSize-7)
        
        
        self.language=[['Hello in this project we are going to do a quick study about the distribution of corona cases around the world',
                        'Salut dans ce projet on vas faire une etude rapide sur la repartition des nombres des corona dans le monde'],
                       ['Go back','Retour'],['Here are some tips that will help you using this app:',"Voici des informations qui vont vous aider en utilisant l'application"],
                       ['In the main window:','Dans la fenetre principale:'],
                       ['Preventions: Important preventions',
                        "Préventions: Préventions importantes"],
                       ['Graphs: Graphs of the top5 countries in death ,recovered,confirmed numbers of corona',
                        'Graphes: Graphes des top5 pays dans la mort,confirmé,rétablie,cas de corona'],
                       ['Symptoms: Symptoms of the virus','Symptomes: Symptomes de ce virus'],
                       ['Table: Find all the countries and their statistics','Table: Trouver tous les pays avec leurs statistics'],
                       ['Edit → Font: Choose the font size','Edit → Taille de police: Choisir la taille de police'],
                       ['Edit → Color: Choose the font color','Edit → Couleur: Choisir la couleur du police'],
                       ['Edit → Language: Choose french or english','Edit → Langage: Choisir francais ou englais'],
                       ['About → Feedback: Rate the application!',"About → Feedback: Évaluer l'application!"],
                       ['About → Help: Help how to use the application',"About → Help: Aide à utiliser l'application"],
                       ["File → Export data: Save the selected country's statistics in a file","File → Export data: Enregistrer les statistiques du pays sélectionné dans un fichier"],
                       
                       ['File → Exit: Exit the application',"File → Exit: Sortir de l'appication"],
                       ['Preventions → Hotline: Find the emergency numbers of the country you are in',
                        "Preventions → Hotline: Trouver les numéros d'urgence du pays dans lequel vous vous trouvez"]]
                       
                                      
        self.initSV()
        
        
        frame1=ttk.Frame(fenetre)
        frame1.grid(column=0,row=0,sticky=(N,S,W,E))
        frame1['padding']=(15,10)
        labelA1=ttk.Label(frame1,text='A 1-',foreground=color,font=myFont)
        labelA1.grid(row=4,column=0)
        labelA2=ttk.Label(frame1,text='A 2-',foreground=color,font=myFont)
        labelA2.grid(row=5,column=0)
        labelB=ttk.Label(frame1,text='B-',foreground=color,font=myFont)
        labelB.grid(row=6,column=0,sticky=W)
        labelC=ttk.Label(frame1,text='C-',foreground=color,font=myFont)
        labelC.grid(row=7,column=0,sticky=W)
        labelD=ttk.Label(frame1,text='D-',foreground=color,font=myFont)
        labelD.grid(row=8,column=0,sticky=W)
        labelE=ttk.Label(frame1,text='E 1-',foreground=color,font=myFont)
        labelE.grid(row=9,column=0)
        labelE2=ttk.Label(frame1,text='E 2-',foreground=color,font=myFont)
        labelE2.grid(row=10,column=0)
        labelE3=ttk.Label(frame1,text='E 3-',foreground=color,font=myFont)
        labelE3.grid(row=11,column=0)
        labelG1=ttk.Label(frame1,text='G 1-',foreground=color,font=myFont)
        labelG1.grid(row=12,column=0)
        labelG2=ttk.Label(frame1,text='G 2-',foreground=color,font=myFont)
        labelG2.grid(row=13,column=0)
        labelF1=ttk.Label(frame1,text='F 1-',foreground=color,font=myFont)
        labelF1.grid(row=14,column=0)
        labelF2=ttk.Label(frame1,text='F 2-',foreground=color,font=myFont)
        labelF2.grid(row=15,column=0)
    
        label1=ttk.Label(frame1,textvariable=self.SV[0],font=myFont)
        label1.grid(row=0,column=1)
        label0=ttk.Label(frame1,textvariable=self.SV[2],font=myFont)
        label0.grid(row=1,column=1)
        label2=ttk.Label(frame1,textvariable=self.SV[3],font=myFont)
        label2.grid(row=3,column=1,sticky=W)
        label3=ttk.Label(frame1,textvariable=self.SV[4],font=myFont2)
        label3.grid(row=4,column=1,sticky=W)
        label3b=ttk.Label(frame1,textvariable=self.SV[15],font=myFont2)
        label3b.grid(row=5,column=1,sticky=W)
        label4=ttk.Label(frame1,textvariable=self.SV[5],font=myFont2)
        label4.grid(row=6,column=1,sticky=W)
        label5=ttk.Label(frame1,textvariable=self.SV[6],font=myFont2)
        label5.grid(row=7,column=1,sticky=W)
        label6=ttk.Label(frame1,textvariable=self.SV[7],font=myFont2)
        label6.grid(row=8,column=1,sticky=W)
        label7=ttk.Label(frame1,textvariable=self.SV[8],font=myFont2)
        label7.grid(row=9,column=1,sticky=W)
        label8=ttk.Label(frame1,textvariable=self.SV[9],font=myFont2)
        label8.grid(row=10,column=1,sticky=W)
        label9=ttk.Label(frame1,textvariable=self.SV[10],font=myFont2)
        label9.grid(row=11,column=1,sticky=W)
        label10=ttk.Label(frame1,textvariable=self.SV[11],font=myFont2)
        label10.grid(row=12,column=1,sticky=W)
        label11=ttk.Label(frame1,textvariable=self.SV[12],font=myFont2)
        label11.grid(row=13,column=1,sticky=W)
        label12=ttk.Label(frame1,textvariable=self.SV[13],font=myFont2)
        label12.grid(row=14,column=1,sticky=W)
        label13=ttk.Label(frame1,textvariable=self.SV[14],font=myFont2)
        label13.grid(row=15,column=1,sticky=W)
        
        frame2=ttk.LabelFrame(fenetre,text='More')
        frame2['padding']=(30,10)
        frame2.grid(row=1,sticky=(N,S,W,E))
        bouton1=Button(frame2,textvariable=self.SV[1],bg=color,fg='white',width=10,font=myFont3,command=self.goBack)
        bouton1.grid(row=1,sticky=(W))
                       
        fenetre.rowconfigure(0,weight=3)
        fenetre.rowconfigure(1,weight=1)
        fenetre.columnconfigure(0,weight=1)
        
        
        self.checklanguage()

            
            
class mainWindow(baseWindow):

    def __init__(self,root):
        self.getDataFromDB_By_Country()
        
        countryNames=self.countryNames
        data=self.data

        self.configs=self.getConfigs()
        
        self.root=root
        fenetre=root
        fenetre.iconbitmap('pics/icon2.ico')
        #root.minsize(300, 400)
        
        fenetre.title('Main Window')
        self.language=[['Choose a country','Choisissez un pays'],
               ['Death:','Mort:'],['Confirmed:','Confirmé:'],['Recovered:','Rétabli:'],
               ['  Preventions  ','  Préventions  '],['Last updated:','Dernier mise a jour:'],['More','Plus'],['  Symptoms  ','  Symptômes  '],['  Graphs  ','  Graphes  '],['  Map  ','  Carte  ']]

        self.initSV()

        fenetre.option_add('#tearOff',FALSE)
        menubar = Menu(fenetre)
        fenetre['menu'] = menubar
        menu_file = Menu(menubar, tearoff=0)
        menu_edit = Menu(menubar, tearoff=0)
        menu_about = Menu(menubar, tearoff=0)

        menubar.add_cascade(menu=menu_file,label= 'File')
        menubar.add_cascade(menu=menu_edit,label = 'Edit')
        menubar.add_cascade(menu=menu_about,label = 'About')

        menu_file.add_command(label='Export Data',command=self.export)
        menu_file.add_command(label='Exit',command=root.destroy)

        menu_font = Menu(menu_edit, tearoff=0)#sous menus
        menu_font.add_command(label='Size',command=lambda:self.createWindow(sizeWindow))
        menu_font.add_command(label='Colors',command=lambda:self.createWindow(colorWindow))

        menu_language=Menu(menu_edit,tearoff=0)
        menu_language.add_command(label='Francais',command=self.french)
        menu_language.add_command(label='English',command=self.english)
        

        menu_edit.add_cascade(menu=menu_font,label='Font')
        menu_edit.add_command(label='Reset settings',command=self.resetPrompt)
        menu_edit.add_cascade(menu=menu_language,label='Language')

        

        menu_about.add_command(label='Feedback',command=lambda:self.createWindow(feedbackWindow))
        menu_about.add_command(label='Help',command=lambda:self.createWindow(introWindow))
        menu_about.add_command(label='Version 1.0')


        super().setStyle()


        btnColor=self.configs['color']
        
        
        frame2=ttk.Frame(fenetre)
        frame2.grid(row=0,column=0,sticky=(N,S,W,E))
        frame2['padding']=(30,10)
        
        self.label5=ttk.Label(frame2,textvariable=self.SV[0])
        self.label5.grid(row=2,column=1,columnspan=2,sticky=(N),pady=6)
        
        self.cb=ttk.Combobox(frame2,values=countryNames, state="readonly")
        self.cb.bind('<<ComboboxSelected>>', self.cbModified)
        self.cb.grid(row=3,column=1,columnspan=2,sticky=(W,E),pady=2)

        self.label1=ttk.Label(frame2,textvariable=self.SV[1],foreground='black')
        self.label2=ttk.Label(frame2,textvariable=self.SV[2],foreground='black')
        self.label3=ttk.Label(frame2,textvariable=self.SV[3],foreground='black')
        self.label1.grid(row=4,column=1,sticky=E,pady=2)
        self.label2.grid(row=5,column=1,sticky=E,pady=2)
        self.label3.grid(row=6,column=1,sticky=E,pady=2)

        
        self.labelDeaths=ttk.Label(frame2,text='')
        self.labelConfirmed=ttk.Label(frame2,text='')
        self.labelRecovered=ttk.Label(frame2,text='')
        self.labelDeaths.grid(row=4,column=2,sticky=W,pady=2)
        self.labelConfirmed.grid(row=5,column=2,sticky=W,pady=2)
        self.labelRecovered.grid(row=6,column=2,sticky=W,pady=2)
        
        frame3=ttk.LabelFrame(fenetre,text='More')
        frame3.grid(row=1,column=0,sticky=(N,S,W,E))
        frame3['padding']=(30,10)

        photo = PhotoImage(file = "pics/ploticon.png") 
        self.plotimg = photo.subsample(2, 2)
        photo = PhotoImage(file = "pics/tableicon.png") 
        self.tableimg = photo.subsample(2, 2)
        photo = PhotoImage(file = "pics/preventionsicon.png") 
        self.preventionsimg = photo.subsample(2, 2)
        photo = PhotoImage(file = "pics/symptomsicon.png") 
        self.symptomsimg = photo.subsample(2, 2)
        photo = PhotoImage(file = "pics/mapicon.png")
        self.mapimg = photo.subsample(2, 2)
        
        
        
        self.button1=Button(frame3,textvariable=self.SV[4], image = self.preventionsimg,compound=LEFT,command=lambda:self.createWindow(preventionsWindow))#
        self.button1.grid(row=0,column=0,sticky=(W,E),padx=2,pady=2)
        
        self.button2=Button(frame3,textvariable=self.SV[8], image = self.plotimg,compound=LEFT,command=lambda:self.createWindow(plotGraphs))
        self.button2.grid(row=1,column=0,sticky=(W,E),padx=2,pady=2)
        
        self.button3=Button(frame3,textvariable=self.SV[7], image = self.symptomsimg,compound=LEFT,command=lambda:self.createWindow(symptomsWindow))
        self.button3.grid(row=0,column=1,sticky=(W,E),padx=2,pady=2)
        
        self.button4=Button(frame3,text='  Table  ',image = self.tableimg, compound=LEFT, command=lambda:self.createWindow(tableWindow))
        self.button4.grid(row=1,column=1,sticky=(W,E),padx=2,pady=2)

        self.button5=Button(frame3,textvariable=self.SV[9],image = self.mapimg, compound=LEFT,command=lambda:self.createWindow(MapWindow))
        self.button5.grid(row=2,column=0,columnspan=2,sticky=(W,E),padx=2,pady=2)

        self.labellastmoddate=ttk.Label(frame3,textvariable=self.SV[5],foreground='#333333')
        self.labellastmoddate.grid(row=3,column=0,columnspan=2,pady=2)
        
        self.labellastmoddate2=ttk.Label(frame3,text=data[0][-1].split('Last updated: ')[1],foreground='#333333')
        self.labellastmoddate2.grid(row=4,column=0,columnspan=2)

            
        self.cb.set(countryNames[0])
        self.labelDeaths['text'] =str(data[0][2])
        self.labelConfirmed['text'] = str(data[0][3])
        self.labelRecovered['text'] = str(data[0][4])

        fenetre.columnconfigure(0, weight=1)
        fenetre.rowconfigure(0, weight=3)
        fenetre.rowconfigure(1, weight=1)

        frame2.rowconfigure(2,weight=1)
        frame2.rowconfigure(3,weight=1)
        frame2.rowconfigure(4,weight=1)
        frame2.rowconfigure(5,weight=1)
        frame2.rowconfigure(6,weight=1)

        frame2.columnconfigure(1, weight=1)
        frame2.columnconfigure(2, weight=1)

        frame3.rowconfigure(1,weight=1)
        frame3.rowconfigure(2,weight=1)
        frame3.rowconfigure(3,weight=1)

        frame3.columnconfigure(0, weight=1)
        frame3.columnconfigure(1, weight=1)

        self.english()
        self.updateFont()

    def createWindow(self,Window): #tableWindow preventionsWindow feedbackWindow introWindow symptomsWindow 
            Window(self)


    def french(self):
        self.configs['language']='french'
        super().french()
    def english(self):
        self.configs['language']='english'
        super().english()

    def export(self):
        country=self.cb.get()
        death=self.labelDeaths['text']
        confirmed=self.labelConfirmed['text']
        recovered=self.labelRecovered['text']
        
        parag=country+":\n\nDeath: "+str(death)+"\nConfirmed: "+str(confirmed)+"\nRecovered: "+str(recovered)+'\n\nData Generated from Python Script(TP Info3)'
        file_path=filedialog.asksaveasfilename(initialfile='countryInfo.txt',defaultextension=".txt",filetypes=[("Text Documents","*.txt")])
        if file_path:
            f=open(file_path,'w')
            f.write(parag)
            f.close()

        

#data: id country death confirmed recovered lastchecked
    def cbModified(self,event):
        countryname=self.cb.get()
        for elm in self.data:
            if elm[1]==countryname: 
                self.labelDeaths['text'] =str(elm[2])
                self.labelConfirmed['text'] = str(elm[3])
                self.labelRecovered['text'] = str(elm[4])



    def resetPrompt(self):
        answer = messagebox.askyesno("Warning","Reset seetings?")
        if answer==True:
            self.setConfigs(('color','#70b570'))
            self.setConfigs(('fontSize',16))
            self.updateFont()

    def updateFont(self):
        Labels=[self.label1,self.label2,self.label3,self.labelDeaths,self.labelRecovered,self.labelConfirmed]
        fontSize=self.configs['fontSize']
        color=self.configs['color']
        myFont = font.Font(self.root,size=fontSize,weight='bold')
        myFont2 = font.Font(self.root,size=fontSize-7)
        myFont3 = font.Font(self.root,size=fontSize)
        
        for elm in Labels:
            elm['font']=myFont
            
        self.labelDeaths['foreground']=color
        self.labelRecovered['foreground']=color
        self.labelConfirmed['foreground']=color

        self.labellastmoddate['font']=myFont2
        self.labellastmoddate2['font']=myFont2

        self.button1.config(bg=color,fg='white',font=myFont2)
        self.button2.config(bg=color,fg='white',font=myFont2)
        self.button3.config(bg=color,fg='white',font=myFont2)
        self.button4.config(bg=color,fg='white',font=myFont2)
        self.button5.config(fg=color,bg='white',font=myFont2)

        self.label5.config(font=myFont3)

    def getConfigs(self): 
        with open('configs.txt','rb') as f:
            a=pickle.load(f)
            a['language']='english'
            return a #color fontSize language
            
    def setConfigs(self,value): #type(value)=tuple (param,newValue)
        if value[0]=='color' or value[0]=='fontSize' or value[0]=='language':
            self.configs[value[0]]=value[1]

        open('configs.txt', 'w').close()
        with open('configs.txt', 'wb') as f:
            pickle.dump(self.configs, f)


    def getDataFromDB_By_Country(self):
        self.countryNames=[]
        conn = create_connection()
        with conn:
            self.data=select_by_country(conn,'ASC')
        for elm in self.data:
            self.countryNames.append(elm[1]) #elm[1]=countryName

        
class tableWindow(baseWindow):
    def __init__(self,mainWindowInstance):
        self.mainWindowInstance=mainWindowInstance

        self.root=mainWindowInstance.root
        root=mainWindowInstance.root 
        fenetre=Toplevel(root)
        self.fenetre=fenetre

        
        fenetre.title('TableView')
        self.setIcon()

        self.language=[["Country",'Pays'],['Deaths','Mort'],['Confirmed','Confirmé'],['Recovered','Rétabli']]
        self.initSV()
        self.checklanguage()
        
        self.countryOrder='DESC'
        self.deathsOrder='DESC'
        self.confirmedOrder='DESC'
        self.recoveredOrder='DESC'

        frame=ttk.Frame(fenetre)
        frame.grid(sticky='nswe')
        
        fenetre.columnconfigure(0, weight=1)
        fenetre.rowconfigure(0, weight=1)
               
        

        tree=ttk.Treeview(frame)
        tree.pack(side='left',expand=True,fill='both')

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        vsb.pack(side='right',fill='y')

        tree.configure(yscrollcommand=vsb.set)

        tree["columns"]=("one","two","three")
        tree.column("#0",minwidth=200)
        tree.column("one",minwidth=150)
        tree.column("two",minwidth=150)
        tree.column("three",minwidth=150)

        tree.heading("#0",text=self.SV[0].get(),anchor=W,command=self.countryListener)
        tree.heading("one", text=self.SV[1].get(),anchor=W,command=self.deathsListener)
        tree.heading("two", text=self.SV[2].get(),anchor=W,command=self.confirmedListener)
        tree.heading("three", text=self.SV[3].get(),anchor=W,command=self.recoveredListener)

        self.tree=tree
        self.countryListener()

        
    def countryListener(self):
        
        self.tree.delete(*self.tree.get_children())
        
        if self.countryOrder=="ASC":
            self.countryOrder="DESC"
        else:
            self.countryOrder="ASC"
            
        conn=create_connection()
        with conn:
            self.country=select_by_country(conn,self.countryOrder)
        for elm in self.country:
            self.tree.insert('', 'end', text=elm[1],values=(elm[2],elm[3],elm[4]))

    def deathsListener(self):
        
        self.tree.delete(*self.tree.get_children())
        if self.deathsOrder=="ASC":
            self.deathsOrder="DESC"
        else:
            self.deathsOrder="ASC"
            
        conn=create_connection()
        with conn:
            self.deaths=select_by_deaths(conn,self.deathsOrder)
        for elm in self.deaths:
            self.tree.insert('', 'end', text=elm[1],values=(elm[2],elm[3],elm[4]))
    def confirmedListener(self):
        
        self.tree.delete(*self.tree.get_children())
        if self.confirmedOrder=="ASC":
            self.confirmedOrder="DESC"
        else:
            self.confirmedOrder="ASC"
            
        conn=create_connection()
        with conn:
            self.confirmed=select_by_confirmed(conn,self.confirmedOrder)
        for elm in self.confirmed:
            self.tree.insert('', 'end', text=elm[1],values=(elm[2],elm[3],elm[4]))
    def recoveredListener(self):
        
        self.tree.delete(*self.tree.get_children())
        if self.recoveredOrder=="ASC":
            self.recoveredOrder="DESC"
        else:
            self.recoveredOrder="ASC"
            
        conn=create_connection()
        with conn:
            self.recovered=select_by_recovered(conn,self.recoveredOrder)
        for elm in self.recovered:
            self.tree.insert('', 'end', text=elm[1],values=(elm[2],elm[3],elm[4]))
            

                
class feedbackWindow(baseWindow):
    def __init__(self,mainWindowInstance):
        self.initTopWindows(mainWindowInstance,'Feedback')
         
        root=self.root
        fenetre=self.fenetre
        

        color=mainWindowInstance.configs['color']
        fontSize=mainWindowInstance.configs['fontSize']
        
        myFont = font.Font(fenetre,size=fontSize)
        myFont2 = font.Font(fenetre,size=fontSize-7)
        
        self.language=[['Name:','Prenom:'],['Submit','Soumettre'],['Go back','Retour']]
        self.initSV()

        frame1 = ttk.Frame(fenetre,padding=(30,30),style='new.TFrame')
        frame1.grid(column=0,row=0,sticky=(N,S,W,E))


        photo = PhotoImage(file = "pics/nameicon.png") 
        self.nameimg = photo.subsample(2, 2)
        photo = PhotoImage(file = "pics/emailicon.png") 
        self.emailimg = photo.subsample(2, 2)
        photo = PhotoImage(file = "pics/msgicon.png") 
        self.msgimg = photo.subsample(2, 2)
        photo = PhotoImage(file = "pics/submiticon.png") 
        self.submitimg = photo.subsample(2, 2)
        

        label1=ttk.Label(frame1,textvariable =self.SV[0],image = self.nameimg, compound=LEFT,font=myFont,style='new.TLabel')
        label1.grid(row=1,column=1,sticky=(W))

        self.entry1 = ttk.Entry(frame1)
        self.entry1.grid(row=2,column=1,sticky=(N,S,E,W))

        label2=ttk.Label(frame1,text = 'Email :',image = self.emailimg, compound=LEFT,font=myFont,style='new.TLabel')
        label2.grid(row=3,column=1,sticky=(W))

        self.entry2 = ttk.Entry(frame1)
        self.entry2.grid(row=4,column=1,sticky=(N,S,E,W))

        label3=ttk.Label(frame1,text = 'Message :',image = self.msgimg, compound=LEFT,font=myFont,style='new.TLabel')
        label3.grid(row=5,column=1,sticky=(W))

        self.entry3 = Text(frame1,width=30,height=10)
        self.entry3.grid(row=6,column=1,sticky=(N,S,E,W))

        frame2 = ttk.Frame(fenetre,padding=(20,20),style='new.TFrame')
        frame2.grid(column=0,row=1,sticky=(N,S,W,E))


        self.starwhite = PhotoImage(file = "pics/star.png")
        self.starorange = PhotoImage(file = "pics/starorange.png")
        self.starcount=''
        
        self.btn1star=Button(frame2, image = self.starwhite,relief='flat',command=lambda:self.stardef(1))
        self.btn1star.grid(row=0,column=1,sticky=(W,E))
 
        self.btn2star=Button(frame2, image = self.starwhite,relief='flat',command=lambda:self.stardef(2))
        self.btn2star.grid(row=0,column=2,sticky=(W,E))

        self.btn3star=Button(frame2, image = self.starwhite,relief='flat',command=lambda:self.stardef(3))
        self.btn3star.grid(row=0,column=3,sticky=(W,E))
        self.btn4star=Button(frame2, image = self.starwhite,relief='flat',command=lambda:self.stardef(4))
        self.btn4star.grid(row=0,column=4,sticky=(W,E))
        self.btn5star=Button(frame2, image = self.starwhite,relief='flat',command=lambda:self.stardef(5))
        self.btn5star.grid(row=0,column=5,sticky=(W,E))

        frame3 = ttk.Frame(fenetre,padding=(20,20),style='new.TFrame')
        frame3.grid(column=0,row=2,sticky=(N,S,W,E))
        
        self.submit_button=Button(frame3, textvariable =self.SV[1],bg=color,fg='white',height=25,font=myFont2,command=self.SubmitForm,image = self.submitimg, compound=RIGHT)
        self.submit_button.grid(row=1,column=1,sticky=(W,E),pady=5)
        

        backbtn=Button(frame3, textvariable =self.SV[2],bg=color,fg='white',font=myFont2,command=self.goBack)
        
        backbtn.grid(row=2,column=1,sticky=(W,E),pady=5)


        fenetre.columnconfigure(0, weight=1)
        fenetre.rowconfigure(0, weight=6)
        fenetre.rowconfigure(1, weight=1)
        fenetre.rowconfigure(2, weight=2)

        frame1.rowconfigure(2,weight=1)
        frame1.rowconfigure(3,weight=1)
        frame1.rowconfigure(4,weight=1)
        frame1.rowconfigure(5,weight=1)
        frame1.rowconfigure(6,weight=1)

        frame1.columnconfigure(1, weight=1)


        frame2.rowconfigure(0,weight=1)

        frame2.columnconfigure(1, weight=1)
        frame2.columnconfigure(2, weight=1)
        frame2.columnconfigure(3, weight=1)
        frame2.columnconfigure(4, weight=1)
        frame2.columnconfigure(5, weight=1)


        self.checklanguage()

        frame3.rowconfigure(1,weight=1)
        frame3.rowconfigure(2,weight=1)
        frame3.columnconfigure(1, weight=1)
      
    def SubmitForm(self):
        
        name=self.entry1.get()
        email=self.entry2.get()
        themsg=self.entry3.get("1.0","end-1c")
        
        if name!='' and email!='' and themsg!='' and self.starcount!='':
            response=posttoserver(name,email,themsg,self.starcount)
            if response=='done':          
                messagebox.showinfo("Information","Your feedback was sent successfully!")
            else:
                messagebox.showerror("Error", 'Could not send the feedback')
        else:
            messagebox.showerror("Error", 'empty fields')

    def stardef(self,n):
        self.starcount=n
        btns=[self.btn1star,self.btn2star,self.btn3star,self.btn4star,self.btn5star]
        for elm in btns:
            elm['image']=self.starwhite
        for i in range(n):
            btns[i]['image']=self.starorange
            
           

class sizeWindow(baseWindow):
    
    def __init__(self,mainWindowInstance):
        self.initTopWindows(mainWindowInstance,'Choose font size')
         
        root=self.root
        fenetre=self.fenetre

        color=mainWindowInstance.configs['color']
        fontSize=mainWindowInstance.configs['fontSize']
        
        myFont = font.Font(fenetre,size=fontSize)
        

        
        self.language=[['Choose a font size:','Choisir une taille de police:'],[' Apply ',' Postuler '],[' Go back ',' Retour '],[' Preview ',' Apercu ']]
        self.initSV()

        frame1 = ttk.Frame(fenetre,padding=(15,15),style='new.TFrame')
        frame1.grid()
        label1=ttk.Label(frame1,textvariable=self.SV[0],style='new.TLabel')
        label1.grid(row=0,column=2,columnspan=2)

        self.scale=Scale(frame1,from_=5,to=30,orient=HORIZONTAL,command=self.updatevalue)
        self.scale.grid(row=1,column=2,columnspan=2,pady=5)

        initValue=mainWindowInstance.configs['fontSize']
        self.scale.set(initValue)

        self.labelPreview=ttk.Label(frame1,textvariable=self.SV[3],font=myFont,style='new.TLabel')
        self.labelPreview.grid(row=2,column=2,columnspan=2,pady=5)

        bouton1=Button(frame1,textvariable=self.SV[1],fg='white',bg=color,width=10,command=self.applyFont)
        bouton1.grid(row=3,column=2,sticky=(W,E),padx=5,pady=5)
        bouton2=Button(frame1,textvariable=self.SV[2],fg='white',bg=color,width=10,command=self.goBack)
        bouton2.grid(row=3,column=3,sticky=(W,E),padx=5,pady=5)

        fenetre.columnconfigure(0, weight=1)
        fenetre.rowconfigure(0, weight=1)

        self.checklanguage()

    def updatevalue(self,event):
        self.labelPreview['font']=font.Font(self.fenetre,size=self.scale.get())

    def applyFont(self):
        value=self.scale.get()
        self.mainWindowInstance.setConfigs(('fontSize',value))
        self.mainWindowInstance.updateFont()
        self.goBack()



class colorWindow(baseWindow):
    def __init__(self,mainWindowInstance):
        self.initTopWindows(mainWindowInstance,'choose font Color')
         
        root=self.root
        fenetre=self.fenetre
        
        color=mainWindowInstance.configs['color']
        fontSize=mainWindowInstance.configs['fontSize']
        
        frame1 = ttk.Frame(fenetre,padding=(15,15),style='new.TFrame')
        frame1.grid()
        self.language=[['Choose a color','Choisir la couleur'],[' Apply ',' Postuler '],[' Go back ',' Retour '],[' Preview ',' Apercu ']]
        self.initSV()

        label1=ttk.Label(frame1,textvariable=self.SV[0],style='new.TLabel')
        label1.grid(row=0,column=2,columnspan=2,pady=5)

        bouton3=ttk.Button(frame1,textvariable=self.SV[0], command=self.getColor)
        bouton3.grid(row=2,column=2,columnspan=2,pady=5)

        initValue=mainWindowInstance.configs['color']
        self.labelPreview=ttk.Label(frame1,textvariable=self.SV[3],font=('bold'),style='new.TLabel',foreground=initValue)
        self.labelPreview.grid(row=3,column=2,columnspan=2,pady=5)

        bouton1=Button(frame1,textvariable=self.SV[1],fg='white',bg=color,width=10,command=self.setColor)
        bouton1.grid(row=4,column=2,sticky=(W,E),padx=5,pady=5)
        bouton2=Button(frame1,textvariable=self.SV[2],fg='white',bg=color,width=10,command=self.goBack)
        bouton2.grid(row=4,column=3,sticky=(W,E),padx=5,pady=5)

        fenetre.columnconfigure(0, weight=1)
        fenetre.rowconfigure(0, weight=1)

        self.checklanguage()

    def getColor(self):
        color = askcolor()
        self.labelPreview['foreground']=color[1]

    def setColor(self):
        value=str(self.labelPreview['foreground'])
        self.mainWindowInstance.setConfigs(('color',value))
        self.mainWindowInstance.updateFont()
        self.goBack()
        

class preventionsWindow(baseWindow):
    def __init__(self,mainWindowInstance):
        self.initTopWindows(mainWindowInstance,'Preventions')
         
        root=self.root
        fenetre=self.fenetre

        fontSize=mainWindowInstance.configs['fontSize']
        color=mainWindowInstance.configs['color']
        
        
        myFont = font.Font(fenetre,size=fontSize,weight='bold')
        myFont2 = font.Font(fenetre,size=fontSize-2)
        
        
        self.language=[['Keep','Garder'],['a safe distance','une distance de sécurité'],
               ['Wash','Se laver'],['your hands often','les mains souvent'],
               ['Cover','Couvrir'],['your cough more','votre toux plus'],['Stay','Rester'],['home as much as you can','à la maison autant que possible'],
                       [' Go back ',' Retour ']]
                       
        self.initSV()

        
        
        frame3=ttk.Frame(fenetre)
        frame3.grid(row=0,column=0,sticky=(N,S,W,E))
        frame3['padding']=(30,10)




        label5=ttk.Label(frame3,text='1-',font=myFont,foreground=color)
        label5.grid(row=2,column=1)        
        label8=ttk.Label(frame3,textvariable=self.SV[6],font=myFont,foreground='black')
        label8.grid(row=2,column=2)
        label9=ttk.Label(frame3,textvariable=self.SV[7],font=myFont2,foreground='black')
        label9.grid(row=2,column=3,sticky=W)

        label6=ttk.Label(frame3,text='2-',font=myFont,foreground=color)
        label6.grid(row=3,column=1)        
        label10=ttk.Label(frame3,textvariable=self.SV[0],font=myFont,foreground='black')
        label10.grid(row=3,column=2)
        label11=ttk.Label(frame3,textvariable=self.SV[1],font=myFont2,foreground='black')
        label11.grid(row=3,column=3,sticky=W)

        label7=ttk.Label(frame3,text='3-',font=myFont,foreground=color)
        label7.grid(row=4,column=1)        
        label12=ttk.Label(frame3,textvariable=self.SV[2],font=myFont,foreground='black')
        label12.grid(row=4,column=2)
        label13=ttk.Label(frame3,textvariable=self.SV[3],font=myFont2,foreground='black')
        label13.grid(row=4,column=3,sticky=W)

        label16=ttk.Label(frame3,text='4-',font=myFont,foreground=color)
        label16.grid(row=5,column=1)        
        label14=ttk.Label(frame3,textvariable=self.SV[4],font=myFont,foreground='black')
        label14.grid(row=5,column=2)
        label15=ttk.Label(frame3,textvariable=self.SV[5],font=myFont2,foreground='black')
        label15.grid(row=5,column=3,sticky=W)
        
        
        
        
        
        frame4=ttk.LabelFrame(fenetre,text='More')
        frame4['padding']=(30,10)
        frame4.grid(row=1,column=0,sticky=(N,S,W,E))
        
        button=Button(frame4,textvariable=self.SV[8],bg=color,fg='white',font=myFont2,command=self.goBack)
        button2=Button(frame4,text='Hotline',bg=color,fg='white',font=myFont2,command=self.createLocationWindow)
        button.grid(row=0,column=0,sticky=(W,E),padx=2,pady=2)
        button2.grid(row=0,column=1,sticky=(W,E),padx=2,pady=2)
        
        fenetre.columnconfigure(0, weight=1)
        fenetre.rowconfigure(0, weight=3)
        fenetre.rowconfigure(1, weight=1)
        

        frame3.rowconfigure(2,weight=1)
        frame3.rowconfigure(3,weight=1)
        frame3.rowconfigure(4,weight=1)
        frame3.rowconfigure(5,weight=1)

        frame3.columnconfigure(1, weight=1)
        frame3.columnconfigure(2, weight=1)
        frame3.columnconfigure(3, weight=1)
        
        frame4.rowconfigure(0,weight=1)

        frame4.columnconfigure(0, weight=1)
        frame4.columnconfigure(1, weight=1)

        self.checklanguage()

        
    def createLocationWindow(self):
        self.configs=self.mainWindowInstance.configs
        locationWindow(self)

     

class locationWindow(baseWindow):
    def __init__(self,preventionsWindow):
        self.preventionsWindow=preventionsWindow
        
        self.root=preventionsWindow.fenetre
        root=self.root
        self.fenetre=Toplevel(root)
        fenetre=self.fenetre
        root.withdraw()
        
        self.setIcon()
        fenetre.title('Location')
        self.fenetre.protocol('WM_DELETE_WINDOW', preventionsWindow.root.destroy)

        fontSize=preventionsWindow.configs['fontSize']
        color=preventionsWindow.configs['color']
        
        
        myFont = font.Font(fenetre,size=fontSize-1,weight='bold')
        myFont2 = font.Font(fenetre,size=fontSize,weight='bold')
        myFont3 = font.Font(fenetre,size=fontSize-2)

        
        self.language=[['Your location is:','Votre emplacement est a:'],['More','Plus'],['Go back','Retour']]
        self.initSV()


        fenetre.title('Hotline')
        frame6=ttk.Frame(fenetre)
        frame6.grid(row=0,column=0,sticky=(N,S,W,E))
        frame6['padding']=(30,10)
        
        
        label2=ttk.Label(frame6,textvariable=self.SV[0],font=myFont)
        label2.grid(row=0,column=0,sticky=(N))
        LabelCountry=ttk.Label(frame6,text=Location.country,foreground=color,font=myFont2)
        LabelCountry.grid(row=1,column=0,sticky=(N))

        self.LabelNumbers=ttk.Label(frame6,text='',font=myFont3)
        self.LabelNumbers.grid(row=2,column=0,sticky=(N))
        
        
        
        frame7=ttk.LabelFrame(fenetre,text='More')
        frame7.grid(row=1,column=0,sticky=(N,S,W,E))
        frame7['padding']=(30,10)
        button1=Button(frame7,textvariable=self.SV[2],bg=color,fg='white',width=10,font=myFont3,command=self.goBack)
        button1.grid(sticky=(W))
        
        fenetre.columnconfigure(0, weight=1)
        fenetre.rowconfigure(0, weight=3)
        fenetre.rowconfigure(1, weight=1)
   

        frame6.columnconfigure(0, weight=1)
        frame6.rowconfigure(0,weight=1)
        frame6.rowconfigure(1,weight=1)
        frame6.rowconfigure(2,weight=1)
        
        frame7.rowconfigure(0,weight=1)
        frame7.columnconfigure(0, weight=1)

        

        self.checklanguage()
        self.getPhoneNumbers()

    def getPhoneNumbers(self):
        with open('phoneNumbers.txt','rb') as f:
            PhoneNumbers= pickle.load(f)

            selectedCountryNumbers=PhoneNumbers[Location.country]
            
            police=selectedCountryNumbers['police']
            ambulance=selectedCountryNumbers['ambulance']
            fire=selectedCountryNumbers['fire']
            
            self.LabelNumbers['text']='Police: '+police+' Ambulance: '+ambulance+' Fire: '+fire
        



class symptomsWindow(baseWindow):
    def __init__(self,mainWindowInstance):
        self.initTopWindows(mainWindowInstance,'Symptoms')
         
        root=self.root
        fenetre=self.fenetre


        fontSize=mainWindowInstance.configs['fontSize']
        color=mainWindowInstance.configs['color']
        
        myFont = font.Font(fenetre,size=fontSize+2,weight='bold')
        myFont2 = font.Font(fenetre,size=fontSize)
        myFont3 = font.Font(fenetre,size=fontSize-7)
        

        
        self.language=[['Common symptoms:','Symptomes communs:'],['Fever','Fièvre'],['Tiredness','Fatigue'],
                  ['Dry cough','Toux sèche'],['Some people may experience:','Certaines personnes peuvent éprouver:'],
                  ['Aches and pains','Maux et douleurs'],['Nasal congestion','Congestion nasale'],
                  ['Runny nose','Nez qui coule'],['Sore throat','Gorge irritée'],['Diarrhoea','Diarhée'],
                  ['On average it takes 5–6 days from when someone is infected',"Cela prend en moyenne 5-6 jours à partir du moment ou quelqu'un est infecté"],
                  ['with the virus for symptoms to show, however it can take up to 14 days',"avec le virus pour que les symptomes apparaissent ,mais cela peut prendre jusqu'a 14 jours"],
                       ['Back','Retourner']]
        self.initSV()


        frame2=ttk.Frame(fenetre,padding=(30,10))
        frame2.grid(row=0,column=0,sticky=(N,W,S,E))

        label1=ttk.Label(frame2,text='A-',font=myFont,foreground=color)
        label1.grid(row=0,column=0,sticky=(W))
        
        label2=ttk.Label(frame2,textvariable=self.SV[0],font=myFont)
        label2.grid(row=0,column=1,sticky=W)
        
        label3=ttk.Label(frame2,text='1-',foreground=color,font=myFont2)
        label3.grid(row=1,column=0,sticky=W)
        
        label4=ttk.Label(frame2,textvariable=self.SV[1],font=myFont2)#
        label4.grid(row=1,column=1,sticky=W)
        
        label4=ttk.Label(frame2,text='2-',foreground=color,font=myFont2)
        label4.grid(row=2,column=0,sticky=W)
        
        label5=ttk.Label(frame2,textvariable=self.SV[2],font=myFont2)#
        label5.grid(row=2,column=1,sticky=W)

        label20=ttk.Label(frame2,text='3-',foreground=color,font=myFont2)
        label20.grid(row=3,column=0,sticky=W)

        label7=ttk.Label(frame2,textvariable=self.SV[3],font=myFont2)#
        label7.grid(row=3,column=1,sticky=W)
        
        label9=ttk.Label(frame2,text='B-',font=myFont,foreground=color)
        label9.grid(row=4,column=0,sticky=W)

        label8=ttk.Label(frame2,textvariable=self.SV[4],font=myFont)
        label8.grid(row=4,column=1,sticky=W)
        
        label15=ttk.Label(frame2,text='1-',foreground=color,font=myFont2)
        label15.grid(row=5,column=0,sticky=W)

        label10=ttk.Label(frame2,textvariable=self.SV[5],font=myFont2)#
        label10.grid(row=5,column=1,sticky=W)
        
        label16=ttk.Label(frame2,text='2-',foreground=color,font=myFont2)
        label16.grid(row=6,column=0,sticky=W)


        label11=ttk.Label(frame2,textvariable=self.SV[6],font=myFont2)#
        label11.grid(row=6,column=1,sticky=W)
        
        label17=ttk.Label(frame2,text='3-',foreground=color,font=myFont2)
        label17.grid(row=7,column=0,sticky=W)

        label12=ttk.Label(frame2,textvariable=self.SV[7],font=myFont2)#
        label12.grid(row=7,column=1,sticky=W)
        
        label18=ttk.Label(frame2,text='4-',foreground=color,font=myFont2)
        label18.grid(row=8,column=0,sticky=W)


        label13=ttk.Label(frame2,textvariable=self.SV[8],font=myFont2)#
        label13.grid(row=8,column=1,sticky=W)
        
        label19=ttk.Label(frame2,text='5-',foreground=color,font=myFont2)
        label19.grid(row=9,column=0,sticky=W)

        label14=ttk.Label(frame2,textvariable=self.SV[9],font=myFont2)#
        label14.grid(row=9,column=1,sticky=W)
        
        label22=ttk.Label(frame2,text='C-',font=myFont,foreground=color)
        label22.grid(row=10,column=0,sticky=W)

        label21=ttk.Label(frame2,textvariable=self.SV[10],font=myFont)
        label21.grid(row=10,column=1,sticky=W)
        
        label24=ttk.Label(frame2,textvariable=self.SV[11],font=myFont)
        label24.grid(row=11,column=1,sticky=W)
        
        frame3=ttk.Labelframe(fenetre,text='More')
        frame3.grid(row=1,column=0,sticky=(N,S,W,E))
        frame3['padding']=(30,10)
        
        button1=Button(frame3,textvariable=self.SV[12],fg='white',bg=color,width=10,font=myFont3,command=self.goBack)
        button1.grid(row=0,column=0,columnspan=2,sticky=(W))
        
        fenetre.columnconfigure(0, weight=1)
        fenetre.rowconfigure(0, weight=3)
        fenetre.rowconfigure(1, weight=1)
        

        frame2.rowconfigure(0,weight=1)
        frame2.rowconfigure(1,weight=1)
        frame2.rowconfigure(2,weight=1)
        frame2.rowconfigure(3,weight=1)
        frame2.rowconfigure(4,weight=1)
        frame2.rowconfigure(5,weight=1)
        frame2.rowconfigure(6,weight=1)
        frame2.rowconfigure(7,weight=1)
        frame2.rowconfigure(8,weight=1)
        frame2.rowconfigure(9,weight=1)
        frame2.rowconfigure(10,weight=1)
        frame2.rowconfigure(11,weight=1)

        frame2.columnconfigure(0, weight=1)
        frame2.columnconfigure(1, weight=1)
        
        frame3.rowconfigure(0,weight=1)
        frame3.rowconfigure(0, weight=1)

        
        self.checklanguage()



def plotGraphs(mainWindowInstance):
    color=mainWindowInstance.configs['color']
    plt.figure(figsize=(9,7))
    plt.gcf().canvas.set_window_title('Graph Top5')
        
    data1=[]
    data2=[]
    data3=[]
    conn = create_connection()
    with conn:
        data1=select_top5_deaths(conn)
        data2=select_top5_confirmed(conn)
        data3=select_top5_recovered(conn)

    columns = list(zip(*data1))

    countryNamesForDeathsDESC=columns[0]
    deathsDESC=columns[1]


    ay1 = plt.subplot(221)
    ax1=plt.bar(countryNamesForDeathsDESC,deathsDESC)
    plt.title('Top 5 Deaths')

    for elm in ax1:
        elm.set_color(color)

    #################################

    columns = list(zip(*data2))

    countryNamesForConfirmedDESC=columns[0]
    confirmedDESC=columns[1]

    y2=plt.subplot(212)
    ax2=plt.bar(countryNamesForConfirmedDESC,confirmedDESC)
    plt.ylabel('Top 5 Confirmed')

    for elm in ax2:
        elm.set_color(color)

    #################################
        

    columns = list(zip(*data3))

    countryNamesForRecoveredDESC=columns[0]
    recoveredDESC=columns[1]

    ay3=plt.subplot(222)
    ax3=plt.bar(countryNamesForRecoveredDESC,recoveredDESC)
    plt.title('Top 5 Recovered')

    for elm in ax3:
        elm.set_color(color)

    plt.show()



class MapWindow(baseWindow):
    def __init__(self,mainWindowInstance):
        self.initTopWindows(mainWindowInstance,'Map Top5')
         
        root=self.root
        fenetre=self.fenetre
                     

        fontSize=mainWindowInstance.configs['fontSize']
        color=mainWindowInstance.configs['color']
        myFont = font.Font(fenetre,size=fontSize-7)
        
        self.language=[['  Death  ','  Mort  '],['  Confirmed  ','  Confirmé  '],['  Recovered  ','  Rétabli  ']]
        self.initSV()
        
        
        frame1=Frame(fenetre)
        frame1.grid(row=0,column=0,sticky=(N,S,W,E))

        self.canvas = Canvas(frame1,width=800,height=440) 
        self.canvas.grid()

        img=PILImage.open("pics/map.png")
        self.imgrender = PILImageTk.PhotoImage(img)     
        self.canvas.create_image(400,220,image=self.imgrender)
        self.canvas.image=self.imgrender

        frame2=ttk.LabelFrame(fenetre,text='More')
        frame2['padding']=(30,10)
        frame2.grid()

        btn1=Button(frame2,textvariable=self.SV[0],command=self.DeathsMarkers,bg=color,fg='white',font=myFont)
        btn1.grid(row=0,column=0,sticky=(W,E),padx=2,pady=2)

        btn2=Button(frame2,textvariable=self.SV[1],command=self.ConfirmedMarkers,bg=color,fg='white',font=myFont)
        btn2.grid(row=0,column=1,sticky=(W,E),padx=2,pady=2)

        btn3=Button(frame2,textvariable=self.SV[2],command=self.RecoveredMarkers,bg=color,fg='white',font=myFont)
        btn3.grid(row=0,column=2,sticky=(W,E),padx=2,pady=2)

        btn4=Button(frame2,text='Back',command=self.goBack,fg=color,bg='white',font=myFont)
        btn4.grid(row=1,column=0,columnspan=3,sticky=(W,E),padx=2,pady=2)



        self.LatLongDict=getLatLong()

        conn=create_connection()
        with conn:
            self.top5deaths=select_top5_deaths(conn)
            self.top5confirmed=select_top5_confirmed(conn)
            self.top5recovered=select_top5_recovered(conn)

            self.top5deaths=list(zip(*self.top5deaths))[0]
            self.top5confirmed=list(zip(*self.top5confirmed))[0]
            self.top5recovered=list(zip(*self.top5recovered))[0]


        self.Labels=[]
        self.checklanguage()
        
    def addMarker(self,lat,long,n=1,color='black'):
        lat=float(lat)
        long=float(long)
        
        widget = Label(self.canvas, text=n, fg='white', bg=color)

        y=-2.8008*lat+  218.7668
        x=2.2778*long+327.6441
        
        self.canvas.create_window(x, y, window=widget)
        self.Labels.append(widget)

    def DeathsMarkers(self):
        self.deleteLabels()
        for i in range(len(self.top5deaths)):

            a=self.LatLongDict[self.top5deaths[i]]
            lat=a[1]
            long=a[2]
                
            self.addMarker(lat,long,i+1,'blue')

        widget = Label(self.canvas, textvariable=self.SV[0], fg='white', bg='blue')
        self.canvas.create_window(35, 20, window=widget)
        self.Labels.append(widget)        

    def ConfirmedMarkers(self):
        self.deleteLabels()
        for i in range(len(self.top5confirmed)):

            a=self.LatLongDict[self.top5confirmed[i]]
            lat=a[1]
            long=a[2]
                
            self.addMarker(lat,long,i+1,'green')

        widget = Label(self.canvas, textvariable=self.SV[1], fg='white', bg='green')
        self.canvas.create_window(35, 20, window=widget)
        self.Labels.append(widget) 
        
    def RecoveredMarkers(self):
        self.deleteLabels()
        for i in range(len(self.top5recovered)):

            a=self.LatLongDict[self.top5recovered[i]]
            lat=a[1]
            long=a[2]
                
            self.addMarker(lat,long,i+1,'orange')
            
        widget = Label(self.canvas, textvariable=self.SV[2], fg='white', bg='orange')
        self.canvas.create_window(35, 20, window=widget)
        self.Labels.append(widget)

        

    def deleteLabels(self):
        for elm in self.Labels:
            elm.destroy()



        
if __name__ == "__main__":
    #Location.getLocation()
    root=Tk()
    mainWindow(root)
    root.mainloop()



