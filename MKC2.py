import os
from json import loads as l
import requests as rq
import jdatetime as jd
from pandas import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MarketCapgui(object):
    def setupUi(self, MarketCapgui):
        MarketCapgui.setObjectName("MarketCapgui")
        MarketCapgui.resize(352, 531)
        MarketCapgui.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MarketCapgui)
        self.centralwidget.setObjectName("centralwidget")
        self.datetext = QtWidgets.QTextEdit(self.centralwidget)
        self.datetext.setGeometry(QtCore.QRect(9, 9, 332, 31))
        self.datetext.setMinimumSize(QtCore.QSize(332, 0))
        self.datetext.setMaximumSize(QtCore.QSize(16777215, 6777215))
        self.datetext.setObjectName("datetext")
        self.processpush = QtWidgets.QPushButton(self.centralwidget)
        self.processpush.setGeometry(QtCore.QRect(12, 450, 331, 28))
        font = QtGui.QFont()
        font.setFamily("B Nazanin")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.processpush.setFont(font)
        self.processpush.setObjectName("processpush")
        self.datepush = QtWidgets.QPushButton(self.centralwidget)
        self.datepush.setGeometry(QtCore.QRect(10, 45, 331, 28))
        font = QtGui.QFont()
        font.setFamily("B Nazanin")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.datepush.setFont(font)
        self.datepush.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.datepush.setAutoFillBackground(False)
        self.datepush.setDefault(False)
        self.datepush.setFlat(False)
        self.datepush.setObjectName("datepush")
        self.processtext = QtWidgets.QTextEdit(self.centralwidget)
        self.processtext.setGeometry(QtCore.QRect(10, 80, 331, 361))
        self.processtext.setObjectName("processtext")
        MarketCapgui.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MarketCapgui)
        self.statusbar.setObjectName("statusbar")
        MarketCapgui.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MarketCapgui)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 352, 26))
        self.menubar.setObjectName("menubar")
        MarketCapgui.setMenuBar(self.menubar)
        self.datepush.clicked.connect(self.dategir)
        self.retranslateUi(MarketCapgui)
        QtCore.QMetaObject.connectSlotsByName(MarketCapgui)
        self.processpush.clicked.connect(self.process)
        self.url_ztitad=[]
        self.url_lastprice=[]
        self.total_shares=[]
        self.sym=[]
        self.lastPrices=[]
        self.desk=(os.path.normpath(os.path.expanduser('~/Desktop')))
        self.url_database='https://d4rk-n0153.github.io/tsetmc/market-watch2.html'
    def retranslateUi(self, MarketCapgui):
        _translate = QtCore.QCoreApplication.translate
        MarketCapgui.setWindowTitle(_translate("MarketCapgui", "MarketCapgui"))
        self.processpush.setText(_translate("MarketCapgui", "شروع فرآیند"))
        self.datepush.setText(_translate("MarketCapgui", "ثبت تاریخ"))

    def dategir(self):
        app.processEvents()
        dat=(self.datetext.toPlainText()).split('/')
        app.processEvents()
        self.gdate=str(jd.date(int(dat[0]),int(dat[1]),int(dat[2])).togregorian()).replace('-','')
        app.processEvents()
        self.datetext.append(self.gdate)
    def process(self):
        app.processEvents()
        response_database=rq.get(self.url_database)
        self.data=l(response_database.content.decode('utf-8-sig'))
        if self.processtext.toPlainText() not in self.sym:
            app.processEvents()
            for user_sym in (self.processtext.toPlainText()).split('\n'):
                self.sym.append(user_sym)
        nums=[self.data[0].get(b) for b in self.sym]
        dick=dict(zip(self.sym,nums))
        #print(dick)
        #print(response_database.status_code)
        for k in self.sym:
            urlztitad=f'http://cdn.tsetmc.com/api/Instrument/GetInstrumentHistory/{dick.get(k)}/{self.gdate}'
            urllastprice=f'http://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceHistory/{dick.get(k)}/{self.gdate}'
            if urlztitad not in self.url_ztitad:
                self.url_ztitad.append(urlztitad)
            if urllastprice not in self.url_lastprice:
                self.url_lastprice.append(urllastprice)
        for ztitad in range(len(self.url_ztitad)):
            response_zTitad=rq.get(self.url_ztitad[ztitad],headers={'User-Agent':'D4rk-N0153 was here'})
            total_share=(l(response_zTitad.text))['instrumentHistory'].get('zTitad')
            self.total_shares.append(total_share)
        for last_price in range(len(self.url_lastprice)):
            response_lastprice=rq.get(self.url_lastprice[last_price],headers={'User-Agent':'D4rk-N0153 was here'})
            lastPrice=l(response_lastprice.text)['closingPriceHistory'][0].get('pClosing')
            self.lastPrices.append(lastPrice)
            #print((lastPrice))
        market_cap=[self.lastPrices[i]*self.total_shares[i]/(10000000000) for i in range(len(self.lastPrices))]
        df=DataFrame(index=(self.sym),columns=(self.sym))
        df.insert(len(market_cap),'ارزش بازار(میلیارد تومان)','none')
        for num1 in range(len(market_cap)):
            for num2 in range(len(market_cap)):
                df.loc[str(self.sym[num1]),str(self.sym[num2])]=(market_cap[num1]/market_cap[num2])
                df.loc[str(self.sym[num1]),'ارزش بازار(میلیارد تومان)']=round(market_cap[num1])
        writer=ExcelWriter(f'{self.desk}\\MarketCap.xlsx', mode='w')
        df.to_excel(writer,sheet_name=self.gdate)
        writer.save()
        self.processtext.append('pls close everything tnx')
        exit()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MarketCapgui = QtWidgets.QMainWindow()
    ui = Ui_MarketCapgui()
    ui.setupUi(MarketCapgui)
    MarketCapgui.show()
    sys.exit(app.exec_())
    

