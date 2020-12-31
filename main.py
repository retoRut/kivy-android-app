import json
from datetime import datetime

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel

import connector


class MainApp(App):
    clientService = None
    def build(self):
        """
            Application for API calls

        :return:
        """
        main_layout = MainLayout(self)
       # main_layout.setMainApp(self)
        return main_layout


class MainLayout(TabbedPanel):
    screen = StringProperty(' ')

    def __init__(self,mainApp):
        TabbedPanel.__init__(self)
        self.MainApp = mainApp


    def getSpinnerValues(self):
        '''
         get all Clients (mieter from the homepage)
        :return:
        '''
        self.backend = 'https://rutishauser-ag.ch'
        self.apikey = 'c2hhMjU2OjM1OjI1N2RmNjRmY2UxYTFiMDE2ODcxMmY0YWE5NGYyYWQ4MzkwM2JkZjA2YTNkZmM3NzAwNGExZmE3MmUyYThmZTY='
        self.clientService = connector.JoomlaConnectorService(self.backend, self.apikey)
        list = self.clientService.getAllContactsByName( )
        #print(list)
        return list

    def on_get_click(self):
        """
             get Articel
            :param instance:
            :return:
        """
        print(" button_get")
        tmp = json.dumps(self.clientService.getAllContacts(), sort_keys=True, indent=4)
        #print(tmp)
        self.textCSc = tmp
     #   self.text = tmp

    def on_send_click(self):
        """
         get Articel
        :param instance:
        :return:
        """
        date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        catID = self.clientService.getCategorieID('Waschen')
        print(catID)
        self.clientService.createNewArticle('APP-'+date,'APP-'+date,self.MainApp.root.ids.dataScreen_Label.text,catID, self.MainApp)
        #pops=CreatePopup()
        #pops.open()

    def on_add_click(self):
        """
        add an entry to list
        :return:
        """
        #create the new one:
        tmp = self.MainApp.root.ids.mieter_Spinner.text+','+self.MainApp.root.ids.date.text+','\
                      +self.MainApp.root.ids.duration_textInput.text+',' \
                      + self.MainApp.root.ids.typ_Spinner.text + ',' \
                       +self.MainApp.root.ids.cost_TextInput.text+';\n'
        # read the exsisting Text
        self.MainApp.root.ids.dataScreen_Label.text = self.MainApp.root.ids.dataScreen_Label.text + tmp

    def on_clear_click(self):
        '''

        :return:
        '''
        self.MainApp.root.ids.dataScreen_Label.text =''

    def on_mieter_select(self, text):
    # do whatever you want to do, note that the "text" value will be the one that user selected
        print("text: "+text)
        self.mieter = text

    def on_date_text(self):
        return datetime.now().strftime('%d.%m.%Y')

    def on_typ_select(self, text):
        print(text)

    def on_text_date(self,text):
        self.datum = text
 #   def setDate(self):
 #       self.cal = CalendarWidget(as_popup=True)
 #       self.popup = Popup(title='Calendar', content=self.cal, size_hint=(1, 1))
 #       self.popup.open()


class CreatePopup(Popup):
    pass
class Test(TabbedPanel):
    pass

if __name__ == "__main__":
    app = MainApp()
    app.run()


