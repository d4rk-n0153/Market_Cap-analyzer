import os
from PyQt5 import QtCore, QtGui, QtWidgets
from bs4 import BeautifulSoup as bsp
import json
import requests as rq
import jdatetime as jd
from pandas import *
from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MarketCap(object):
    def setupUi(self, MarketCap):
        app.processEvents()
        MarketCap.setObjectName("MarketCap")
        MarketCap.resize(380, 600)
        self.centralWidget = QtWidgets.QWidget(MarketCap)
        self.centralWidget.setObjectName("centralWidget")
        self.push_date = QtWidgets.QPushButton(self.centralWidget)
        self.push_date.setGeometry(QtCore.QRect(10, 10, 89, 25))
        self.push_date.setObjectName("push_date")
        self.date_text = QtWidgets.QTextEdit(self.centralWidget)
        self.date_text.setGeometry(QtCore.QRect(110, 10, 91, 31))
        self.date_text.setObjectName("date_text")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(190, 10, 171, 17))
        self.label_2.setObjectName("label_2")
        self.symbol_text = QtWidgets.QTextEdit(self.centralWidget)
        self.symbol_text.setGeometry(QtCore.QRect(20, 90, 341, 71))
        self.symbol_text.setObjectName("symbol_text")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(240, 70, 121, 20))
        self.label_3.setObjectName("label_3")
        self.push_symbol = QtWidgets.QPushButton(self.centralWidget)
        self.push_symbol.setGeometry(QtCore.QRect(150, 170, 89, 25))
        self.push_symbol.setObjectName("push_symbol")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 200, 341, 361))
        self.textBrowser.setObjectName("textBrowser")
        MarketCap.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MarketCap)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 370, 22))
        self.menuBar.setObjectName("menuBar")
        MarketCap.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MarketCap)
        self.mainToolBar.setObjectName("mainToolBar")
        MarketCap.addToolBar(QtCore.Qt.BottomToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MarketCap)
        self.statusBar.setObjectName("statusBar")
        self.sym=[]
        self.urls=[]
        self.market_cap=[]
        self.url='https://d4rk-n0153.github.io/tsetmc/market-watch2.html'
        self.response=rq.get(self.url)
        self.data=json.loads(self.response.text)
        self.retranslateUi(MarketCap)
        self.push_date.clicked.connect(self.get_dat)
        self.push_symbol.clicked.connect(self.sym_creat)
        MarketCap.setStatusBar(self.statusBar)
        app.processEvents()
        self.retranslateUi(MarketCap)
        self.desk=(os.path.normpath(os.path.expanduser('~/Desktop')))
        self.headers={
        #Accept: */*
        #Accept-Encoding: gzip, deflate
        'Accept-Language':'en-US',
        #'Cache-Control': 'no-cache',
        #'Connection':'keep-alive',
        #'Cookie':'_ga=GA1.2.1843003826.1607405830; _gid=GA1.2.864430428.1624673785; __qca=P0-1856150858-1624680910808; ASP.NET_SessionId=be4aok1ffxxnmkyogchg2qmt; _gat_gtag_UA_63076930_1=1',
        #'Host': 'cdn.tsetmc.com',
        #'Pragma': 'no-cache',
        #Referer: http://cdn.tsetmc.com/Loader.aspx?ParTree=15131P&i=46348559193224090&d=20210621
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    }
        QtCore.QMetaObject.connectSlotsByName(MarketCap)
# =============================================================================
#     def get_count(self):
#         # def get_count_sym(self):
#         self.Symbols_counts=(self.count_text.toPlainText())
#         
#         
#         print(type(int(self.Symbols_counts)))
# =============================================================================
    def get_dat(self):
        app.processEvents()
        self.dat=(self.date_text.toPlainText()).split('/')
        app.processEvents()
        self.gdate=str(jd.date(int(self.dat[0]),int(self.dat[1]),int(self.dat[2])).togregorian()).replace('-','')
        
        app.processEvents()
        self.textBrowser.append(self.gdate)
    
    def sym_creat(self):
        app.processEvents()
        if self.symbol_text.toPlainText() not in self.sym:
            app.processEvents()
            for i8 in (self.symbol_text.toPlainText()).split('\n'):
                app.processEvents()
                self.sym.append(i8)
        self.nums=[self.data[0].get(b) for b in self.sym]
        self.dick=dict(zip(self.sym,self.nums))
        
        for k in self.sym:
            app.processEvents()
            if (f'http://cdn.tsetmc.com/Loader.aspx?ParTree=15131P&i={self.dick.get(k)}&d={self.gdate}') not in self.urls:
                app.processEvents()
                self.urls.append(f'http://cdn.tsetmc.com/Loader.aspx?ParTree=15131P&i={self.dick.get(k)}&d={self.gdate}')
        for s in range(len(self.urls)):
            app.processEvents()
            self.responses=rq.get(self.urls[s],headers=self.headers)
            if 'ClosingPriceData=[]' not in self.responses.text and 'GeneralError.aspx' not in self.responses.text and self.responses.status_code==200:
                app.processEvents()
                self.soup=bsp(self.responses.text,'html.parser')
                self.s1=self.soup.select('script')
                self.a=((((str(self.s1[4])).replace('<script>var InstSimpleData=', '')).replace('</script>','')).split(';'))
                self.Total_share=int((self.a[0].split(','))[8])
                self.last_price=((((str(self.s1[5]).split(';'))[1]).split(','))[-10]).replace("'","")
                self.market_cap.append((int(self.last_price)*int(self.Total_share)))
                app.processEvents()
                self.textBrowser.append(self.urls[s]+'Finished')
                app.processEvents()
            else:
                app.processEvents()
                while  'GeneralError.aspx?' in self.responses.text or self.responses.status_code!=200:
                    app.processEvents()
                    sleep(1)
                    app.processEvents()
                    self.responses=rq.get(self.urls[s],headers=self.headers)
                    app.processEvents()
                    self.textBrowser.append(self.urls[s]+':error code is: '+ str(self.responses.status_code)+'finished')
                    app.processEvents()
                    if 'ClosingPriceData=[]' not in self.responses.text and 'GeneralError.aspx' not in self.responses.text and self.responses.status_code==200:
                         app.processEvents()
                         self.soup=bsp(self.responses.text,'html.parser')
                         app.processEvents()
                         self.s1=self.soup.select('script')
                         app.processEvents()
                         self.a=((((str(self.s1[4])).replace('<script>var InstSimpleData=', '')).replace('</script>','')).split(';'))
                         app.processEvents()
                         self.Total_share=int((self.a[0].split(','))[8])
                         app.processEvents()
                         self.last_price=((((str(self.s1[5]).split(';'))[1]).split(','))[-10]).replace("'","")
                         app.processEvents()
                         self.market_cap.append((int(self.last_price)*int(self.Total_share)))
                         app.processEvents()
                    if 'ClosingPriceData=[]'  in self.responses.text and 'GeneralError.aspx' not in self.responses.text and self.responses.status_code==200:
                        app.processEvents()
                        self.market_cap.append(None)
                        app.processEvents()
                        continue       

        self.df=DataFrame(index=(self.sym),columns=(self.sym))
        self.df.insert(len(self.market_cap),'ارزش بازار(میلیارد تومان)','none')

        for self.num1 in range(len(self.market_cap)):
            for self.num2 in range(len(self.market_cap)):
               self.df.loc[str(self.sym[self.num1]),str(self.sym[self.num2])]=(self.market_cap[self.num1]/self.market_cap[self.num2])
               self.df.loc[str(self.sym[self.num1]),'ارزش بازار(میلیارد تومان)']=round(self.market_cap[self.num1]/10000000000)
              
            self.writer=ExcelWriter(f'{self.desk}\\MarketCap.xlsx', mode='w')
            self.df.to_excel(self.writer,sheet_name=self.gdate)
            self.writer.save()
            self.textBrowser.append('نرم افزار را ببندید')            
        
    
    def retranslateUi(self, MarketCap):
        app.processEvents()
        _translate = QtCore.QCoreApplication.translate
        MarketCap.setWindowTitle(_translate("MarketCap", "MarketCap"))
        self.push_date.setText(_translate("MarketCap", "ثبت"))
        self.label_2.setText(_translate("MarketCap", "تاریخ مورد نظر را ورد کنید"))
        self.label_3.setText(_translate("MarketCap", "نمادها را وارد کنید"))
        self.push_symbol.setText(_translate("MarketCap", "ثبت"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MarketCap = QtWidgets.QMainWindow()
    ui = Ui_MarketCap()
    ui.setupUi(MarketCap)
    MarketCap.show()
    sys.exit(app.exec_())
