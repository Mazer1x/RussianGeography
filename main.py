from PyQt6.QtWidgets import QApplication, QWidget,QMainWindow
from PyQt6 import QtCore, QtWebChannel,QtGui
from src.form import Ui_MainWindow
import io,os,sys,json,folium
import pandas as pd

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Backend(QtCore.QObject):
    valueChanged = QtCore.pyqtSignal(str)
    

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = ""

    @QtCore.pyqtProperty(str)
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
        self.valueChanged.emit(v)


class Login(QWidget):
    def __init__(self):
        super().__init__()
        

        # use the Ui_login_form
        self.ui = Ui_MainWindow()    
        self.w = QMainWindow()  
        self.ui.setupUi(self.w) 
        self.w.show()
        self.w.setWindowTitle("RussianGeography")
        self.w.setWindowIcon(QtGui.QIcon(resource_path("src/industry-windows.ico")))
        
        self.icon = folium.Icon(icon="industry-window",prefix="fa")
        
        
        with open("src/russia.json", encoding="utf-8",) as f:
            self.state_geo = f.read()
        
        with open("src/russia.csv", encoding="utf-8",) as f:
            state_data = pd.read_csv(io.StringIO(f.read()))
        print(state_data["State"][0],state_data["Unemployment"][0])
        
        m = folium.Map(
            zoom_start=17
        )
        
        folium.Choropleth(
            geo_data=self.state_geo,
            name="Regions",
            data=state_data,
            columns=["State", "Unemployment"],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=.3,
        ).add_to(m)
        self.iconMarker = folium.features.CustomIcon(icon_image=open("src/industry-windows.png"),icon_size=(50,50))
        
        
        self.marcerlist = [[20,31,"xyina","Это полная хуйня"],[40,15,"","Просто маркер"]]
        self.Marcers_create(m,self.marcerlist)
        
        data = io.BytesIO()
        
        m.save(data,close_file=False)
        b = data.getvalue().decode().splitlines()
        head, body = 0,0
        for i,j in enumerate(b):
            if "<body>" in j:
                body = i
            if "<head>" in j:
                head = i
        with open("src/mapfunctions.js", encoding="utf-8",) as f:
            self.mapfunctions = f.read()
        
        b[head] = """<head>\n<script src="qrc:///qtwebchannel/qwebchannel.js"></script>"""+"""
    <style>
        body{
      opacity:0;
   }
   </style>"""+f"""\n<script>\n{self.mapfunctions}\n</script>\n"""
                    
                    
        b[body] = """<body onload="del();">"""
        
        
        
        with open("test.html", 'w',encoding="utf-8",) as f:
                f.write('\n'.join(b))
        
        backend = Backend(self)
        backend.valueChanged.connect(self.onclickelement)
        
        self.channel = QtWebChannel.QWebChannel()
        self.channel.registerObject("backend", backend)
        self.ui.webEngineView.page().setWebChannel(self.channel)    
        self.ui.webEngineView.setHtml('\n'.join(b))
        
        
    def Marcers_create(self,m,data):
        for i in data:
            if len(i)>2 and len(i[2]) >0:
                folium.Marker(location=(i[0],i[1]),tooltip=i[2],icon=self.iconMarker).add_to(m)
            else:
                folium.Marker(location=(i[0],i[1]),icon=self.iconMarker).add_to(m)
            
            
    @QtCore.pyqtSlot(str)
    def onclickelement(self, value):
        if value[0] != 'A':
            if len(self.marcerlist[int(value)])>3:
                self.ui.label_2.setText(self.marcerlist[int(value)][3])
        else:
            for i in json.loads(self.state_geo)["features"]:
                if i["id"] == value:
                    print(i["properties"]["name"],i["id"])


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    login_window = Login()
    sys.exit(app.exec())