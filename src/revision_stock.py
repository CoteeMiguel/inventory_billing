import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

class DlvGeneration:

    def __init__(self):
        self.stocks4 = os.getenv('PATH_STOCK')
        self.backlog = os.getenv('PATH_BACKLOG')
        self.workbook = os.getenv('PATH_WORKBOOK')
        self.listcharlie = os.getenv('PATH_CHARLIELIST')
        self.output = os.getenv('PATH_OUTPUT')

    def prep_filteredlist(self):
        stocks4 = pd.read_excel(self.stocks4)
        #preparar lista material disponible en s4
        stocks4 = stocks4[stocks4['Storage location'] != 1005]
        stocks4.drop(stocks4.tail(1).index,inplace=True)
        stocks4 = stocks4.groupby('Material').sum()['Unrestricted']
        stocks4 = stocks4.to_frame()

        #preparar lista general material tomado en backlog
        backlog = pd.read_excel(self.backlog)
        backlog = backlog[backlog.Plant == 'CL20']

        #lista stock tomado con dlv
        stockdlv = backlog[backlog.ShipDate.isnull()]
        stockdlv = stockdlv[stockdlv.Delivery.notnull()]
        stockdlv = stockdlv.groupby('Material').sum()['Status Qty']

        #lista stock tomado por oc bloqueada
        stockoc = backlog[backlog.Delivery.isnull()]

        workbook = pd.read_excel(self.workbook, sheet_name='User Status Playbook LA',)
        #preparar serie con bloqueos
        workbook.columns = workbook.loc[1]
        workbook = workbook[2:]
        ListaBloqueoDlv = workbook.loc[workbook['Block Delivery'] == 'Yes']['User Status']
        ListaBloqueos = list(ListaBloqueoDlv)
        Lista = ListaBloqueoDlv.reset_index().drop(columns="index")
        #Lista.to_excel(r'C:\Users\varasaya\Desktop\ModeloGeneracionDlv\ListaCharlie.xlsx')

        #preparar lista de OC
        #backlog = pd.read_excel(r"C:\Users\varasaya\Desktop\ModeloGeneracionDlv\osreport_BacklogS4CLUYPY-TEST_2021-02-18_1507.xls")
        stockoc["UltimaBloqueo"] = stockoc.apply(lambda row: BloqueoDlv(row['ItemStati']),axis=1)
        stockoc = stockoc[stockoc.UltimaBloqueo==True]
        stockoc = stockoc.groupby('Material').sum()['ConfirmedQty']
        stockoc = stockoc.to_frame()

        stocks4 = stocks4.merge(stockdlv, how='left', on='Material')
        stocks4 = stocks4.merge(stockoc,how='left', on='Material')
        stocks4 = stocks4.fillna(0)
        # agregar columna con calculo

        filtered = stocks4
        return filtered

        
    def BloqueoDlv(items,us=ListaBloqueos):

        #función para usar apply y determinar si una linea tiene bloqueo
        listaitem = []
        listaitem = items.split()
        '''for line in listaitem:
            if line in ListaBloqueos:
                return True
            else:
                return listaitem'''
        check = any(i in us for i in listaitem)
        if check:
            return True
        else:
            return False
        
    def calculatestock(self,filtered):
        filtered['StockDisponible'] = filtered['Unrestricted'] - filtered['Status Qty'] - filtered['ConfirmedQty']
        return filtered
        
    def dlvgenerationpred(self,filtered):
        generaciondlv = pd.read_excel(self.listcharlie)
        generaciondlv = generaciondlv.groupby(['DeliveryType','Material']).sum()['Status Qty']
        generaciondlv = generaciondlv.swaplevel()
        generaciondlv = generaciondlv.unstack()
        #generaciondlv = generaciondlv.to_frame()
        generaciondlv = generaciondlv.fillna(0)

        generacionsinbloqueo = pd.read_excel(self.listcharlie)
        generacionsinbloqueo = generacionsinbloqueo.groupby('Material').sum()['ConfirmedQty']
        generacionsinbloqueo = generacionsinbloqueo.to_frame()

        filtered = filtered.merge(generaciondlv,how='left',on='Material')
        filtered.fillna(0)

        filtered['Genera?'] = filtered['StockDisponible'] >= filtered['Ship as available']
        filtered = filtered.merge(generacionsinbloqueo, how='left',on='Material')
        return filtered
        

    def outputresult(self,filtered):
        filtered.to_excel(self.output)

if __name__ == '__main__':
    app = DlvGeneration()
    s = app.prep_filteredlist()
    s = app.calculatestock(s)
    s = app.dlvgenerationpred(s)
    app.outputresult(s)