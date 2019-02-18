import requests
from requests.exceptions import ConnectionError
from tkinter import *
import json
from time import gmtime, strftime



            #files=files,
            #data=data or {},
            #json=json,
            #params=params or {},
            #auth=auth,
            #cookies=cookies,
            #hooks=hooks,

#get_cookie_header
#create_cookie
#cert
#verify
#proxies
#timeout
#files
#stream

#cookie
#session
#params yollama = &  ve get params link url yollama ? & =
#json yollama {'fsaf' : 'saf'}
#redirect allow or none
#response ile bilgileri ayırma

#BaseHTTPError
#ConnectTimeout
#ConnectionError
#HTTPError
#InvalidHeader
#InvalidURL
#RequestException
#SSLError
#Timeout
#TooManyRedirects
#URLRequired

class App():
    def __init__(self):
        Root = Tk()
        Root.withdraw()

        self.packetHistory = {}

        reqMethod = StringVar()
        reqMethod.set('get')

        MainWindow = Toplevel(Root)
        MainWindow.withdraw()
        MainWindow.resizable(width=TRUE, height=TRUE)
        MainWindow.geometry("+250+50")
        MainWindow.title('EUU - Http Packets')
        MainWindow.wm_iconbitmap("hourglass")
        MainWindow.deiconify()

        packetHistoryLabel = Label(MainWindow,text='PACKET HISTORY ').grid(row = 0, column = 2,rowspan=3)
        packetHistoryList = Listbox(MainWindow,width=50,state='disabled')
        packetHistoryList.bind('<<ListboxSelect>>',self.oldPacketView)
        packetHistoryList.grid(row = 2, column = 2,rowspan=3,sticky='WENS')
        
        ipLabel = Label(MainWindow,text='Ip Address : ').grid(row = 0, column = 0)
        ipInput = Entry(MainWindow)
        ipInput.grid(row = 0, column = 1,sticky='WE')
        
        portLabel = Label(MainWindow,text='Port Number : ').grid(row = 1, column = 0)
        portInput = Entry(MainWindow)
        portInput.grid(row = 1, column = 1)
        
        paramsLabel = Label(MainWindow,text='Parameters : ').grid(row = 2, column = 0)
        paramsInput = Entry(MainWindow)
        paramsInput.grid(row = 2, column = 1,sticky='WE')

        headerLabel = Label(MainWindow,text='Header ').grid(row = 3, column = 0)
        headerInput = Text(MainWindow,width=50,height=15,bg='sky blue')
        headerInput.grid(row = 4, column = 0)
        
        dataLabel = Label(MainWindow,text='Data ').grid(row = 3, column = 1)
        dataInput = Text(MainWindow,width=50,height=15,bg='sandy brown')
        dataInput.grid(row = 4, column = 1)

        methodsFrame= LabelFrame(MainWindow,relief = GROOVE)
        methodsFrame.grid(row = 5 ,column = 0,columnspan=3,sticky=W+E+N+S)
    
        methodLabel = Label(methodsFrame,text='Method : ').grid(row = 0, column = 0)
        methodGet = Radiobutton(methodsFrame,text='Get',variable=reqMethod,value='get').grid(row = 0, column = 1)
        methodPost = Radiobutton(methodsFrame,text='Post',variable=reqMethod,value='post').grid(row = 0, column = 2 )
        methodPut = Radiobutton(methodsFrame,text='Put',variable=reqMethod,value='put').grid(row = 0, column = 3)
        methodDelete = Radiobutton(methodsFrame,text='Delete',variable=reqMethod,value='delete').grid(row = 0, column = 4)

        responseLabel = Label(MainWindow,text='RESPONSE DATA').grid(row = 6, column = 0,columnspan=3)
        responseCloseText = Text(MainWindow,height=20,bg='medium purple2')
        responseCloseText.grid(row = 7, column = 0,columnspan=3,sticky='we')
        
        sendButton = Button(MainWindow,text="Send",bg='black',fg='white',activebackground='grey',command = lambda: self.sendData(headerInput.get("1.0",END) ,dataInput.get("1.0",END), reqMethod.get()))
        sendButton.grid(row = 8, column = 0,columnspan=3,sticky='we')

        ipInput.insert(INSERT,'192.168.1.10')
        portInput.insert(INSERT,'80')
        paramsInput.insert(INSERT,'/')
        headerInput.insert(INSERT,'User-Agent: euu-python-httpRequests/1.2 \n' 
                                + 'Accept-Encoding: gzip, deflate \n'
                                + 'Accept: */* \n'
                                + 'Connection: keep-alive \n'
                                + 'Content-Type: application/x-www-form-urlencoded')
        
        self.Root = Root
        self.MainWindow = MainWindow
        self.portInput = portInput
        self.ipInput = ipInput
        self.paramsInput = paramsInput
        self.responseText = responseCloseText
        self.packetList = packetHistoryList

        Root.mainloop()
        #this region will not work just tkinter loop
        
    def sendData(self,myHeader,myData,requestMethod):
        self.packetList.configure(state=NORMAL)
        reqHeaders = self.RawToJson(myHeader)
        reqData =self.RawToJson(myData)
        try:
            req = requests.Session()
            req.headers = reqHeaders
            
            request = getattr(req, requestMethod)('http://' + self.ipInput.get() + ':' + self.portInput.get() + '/' +self.paramsInput.get(),
                                                  headers=reqHeaders,
                                                  data=reqData,
                                                  timeout=1.0)
                        
            response = request.text

            self.responseText.delete('1.0',END)
            self.responseText.insert(INSERT,'RESPONSE TEXT: \n' + str(response) + '\n')
            self.responseText.insert(INSERT,'RESPONSE STATUS :' + str(request.status_code) + '\n')
            self.responseText.insert(INSERT,'RESPONSE HEADERS :' + str(request.headers) + '\n')
            self.responseText.insert(INSERT,'RESPONSE COOKIES :' + str(request.cookies))

            self.packetList.insert(END,self.ipInput.get() + ' --> ' + self.paramsInput.get()+ ' --> ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            self.packetHistory[int(self.packetList.size() - 1)] = ('RESPONSE TEXT: \n' + str(response) + '\n'
                                                            + 'RESPONSE STATUS :' + str(request.status_code) + '\n'
                                                            + 'RESPONSE HEADERS :' + str(request.headers) + '\n'
                                                            + 'RESPONSE COOKIES :' + str(request.cookies))
            
            self.responseText.tag_add("here", '1.0', '1.15')
            self.responseText.tag_config("here", foreground="blue")
            
        except: #Add Error Types
            print ("Http Error:")


    def RawToJson(self, rawString):
        jsonData = {}
        stringLines = rawString.splitlines()
        
        for line in stringLines:
            line = line.replace('\t','')
            jsonLine = line.split(':',1)
            if(len(jsonLine) == 2):
                key = jsonLine[0].lstrip().rstrip()
                value = jsonLine[1].lstrip().rstrip()
                jsonData[key] = value
            else:
                key = jsonLine[0].lstrip().rstrip()
                jsonData[key] = None
            
        return(json.loads(json.dumps(jsonData)))

    def oldPacketView(self,listBoxData):
        listbox = listBoxData.widget
        selection = listbox.curselection()
        packetData = self.packetHistory[selection[0]]
        self.responseText.delete('1.0',END)
        self.responseText.insert(INSERT,packetData)
        self.responseText.tag_add("here", '1.0', '1.15')
        self.responseText.tag_config("here", foreground="red")
        
if(__name__ == '__main__'):
    Run = App()

