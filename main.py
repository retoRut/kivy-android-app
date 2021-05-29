import json
from datetime import datetime, time
from html.parser import HTMLParser

from kivy.app import App
from kivy.core.text import Label
from kivy.factory import Factory
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel
# library for html parsing:
import lxml
import re
import pandas as pd
from lxml import etree

import connector

# Enable logging
#from kivy.logger import Logger
#import logging
#Logger.setLevel(logging.TRACE)

class MainApp(App):

    def build(self):
        """
            Application for API calls

        :return:
        """
        print('build methode run at Main APP')
        main_layout = MainLayout(self)

        backend = 'https://rutishauser-ag.ch'
        apikey = 'c2hhMjU2OjM1OjI1N2RmNjRmY2UxYTFiMDE2ODcxMmY0YWE5NGYyYWQ4MzkwM2JkZjA2YTNkZmM3NzAwNGExZmE3MmUyYThmZTY='
        self.clientService = connector.JoomlaConnectorService(backend, apikey, self, main_layout)
        self.logger = Logger()
       # main_layout.setMainApp(self)
        return main_layout


class MainLayout(TabbedPanel):
    screen = StringProperty(' ')

    def __init__(self,mainApp):
        TabbedPanel.__init__(self)
        print('init run at MainLayout ')
        self.MainApp = mainApp
        self.mieter = 0
        self.catid = 0
        # init gui scroll screens
        self.data_screen = Scroll(self.MainApp)


    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")

    @staticmethod
    def kassabuch_year_spinner_default_value():
        """
            set the default value at kassabuch on actual year
        :return:
        """
        return datetime.now().strftime('%Y')

    @staticmethod
    def kassabuch_year_spinner_values():
        """
         set spinner values of kassabuch for three years
        :return:list of years
        """
        list= [str(datetime.now().year),str(datetime.now().year+1),str(datetime.now().year+2)]
        # print(list)
        return list

    @staticmethod
    def kassabuch_ea_spinner_default_value():
        """

        :return:
        """
        return 'Einnahmen'

    @staticmethod
    def kassabuch_ea_spinner_values():
        """

        :return:
        """
        list= ['Einnahmen','Ausgaben']
        return list

    def kassabuch_ea_select(self, text):
        pass

    @staticmethod
    def kassabuch_fuer_spinner_values():
        list= ['Waschgeld','Ausgaben']
        return list

    @staticmethod
    def kassabuch_fuer_spinner_select(text):
        pass

    def kassabuch_prev_kassabuch_button_on_click(self):
        """
                get the actual kassabuch
        :return:
        """
        # connector

       # self.data_screen.set_label(self.MainApp.root.ids.dataScreen_Label)
        #TODO: Auslesen Jahr kassabuch
        resp = self.MainApp.clientService.get_article('kassabuch-2021' )

   # self.communication_screen.add_text_to_screen(i['attributes'], 'data')
        print(json.dumps(resp, indent=4, sort_keys=True))
        # print(json.dumps(resp['text'], indent=4, sort_keys=True))
        self.data_screen.add_text_to_screen(str(resp),'data')

        self.data = DataStore(resp['text'])
        text = self.data.get_html_text()
        # get cat ID missing on article..
        #TODO: catID Name should be not constant
        catid = self.MainApp.clientService.get_categorie_id("Waschen")
        self.MainApp.clientService.delete_article(resp['id'])
        self.MainApp.clientService.create_new_article( 'kassabuch-2021', resp['title'], text, catid )
        # self.MainApp.clientService.update_article(resp['id'],catid,resp['title'], text)
        #print(table[1])
        #e = df[df.Monat == 'januar']
        #print(e)
        # self.data_screen.add_text_to_screen(str(dfs), 'data')

    def kassabuch_category_Spinner_values(self):
        """

        :return:
        """
        list= ['Hörnlistrasse 3','Hörnlistrasse 5']
        # print(list)
        return list

    def kassabuch_get_contacts_on_click(self):
        """

        :return:
        """
        if(self.catid ==0 ):
            PopupApp().build("Please select a category first")
        else:
            list = self.MainApp.clientService.get_all_contacts_by_name_and_building(self.catid)
            print(list)
            self.MainApp.logger.set_log(self.MainApp.root.ids.communicationScreen_Label, ' connect homepage' + '\n')
            self.MainApp.logger.set_log(self.MainApp.root.ids.communicationScreen_Label,
                                     ' get all contacts of category '+str(self.catid)+ '\n' )
            self.ids.contacts_Spinner.values = list
            self.MainApp.root.ids.contacts_Spinner.disabled = False

    def kassabuch_contacts_spinner_values(self):
        """
            set default value of contacts
        :return:
        """
        # list = self.clientService.get_all_contacts_by_name()
        list= ['1','2']
        # print(list)
        return list

    def kassabuch_year_select(self, text):
        pass

    def on_init_click(self):
        """
        NOT NEEDED
         initialize the drop down menus
        :return:
        """
        if(self.building ==0 ):
            PopupApp().build("Please select a building first")
        else:
            list = self.MainApp.clientService.get_all_contacts_by_name_and_building(self.building)
            self.MainApp.logger.set_log(self.MainApp.root.ids.communicationScreen_Label, ' connect homepage' + '\n')
            self.MainApp.logger.set_log(self.MainApp.root.ids.communicationScreen_Label,
                                     ' get all contacts of building '+self.building+ '\n' )
            self.ids.mieter_Spinner.values = list

    def on_get_click(self):
        """
             get Articel
            :param instance:
            :return:
        """
        print(" button_get")
        tmp = json.dumps(self.clientService.get_all_contacts(), sort_keys=True, indent=4)
        #print(tmp)
        self.textCSc = tmp
     #   self.text = tmp

    def on_send_click(self):
        """
         get Articel
        :param instance:
        :return:
        """
        #date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        catID = self.MainApp.clientService.get_categorie_id('Waschen')
        print(catID)
        #TODO: Check inf the file already exist, if yes expand the file
        self.MainApp.clientService.create_new_article('APP-' + self.MainApp.root.ids.mieter_Spinner.text , 'APP-' + self.MainApp.root.ids.mieter_Spinner.text , self.MainApp.root.ids.dataScreen_Label.text, catID, self.MainApp)
        #pops=CreatePopup()

        #pops.open()

    @staticmethod
    def kassabuch_preview_entry_button_on_click():
        """
        add an entry to list
        :return:
        """
        # creating entry with the following:

        #create the new one:
        tmp = MainApp.root.ids.periode_Spinner.text+','\
                      +MainApp.root.ids.building_Spinner.text+',' \
                      + MainApp.root.ids.mieter_Spinner.text + ',' \
                       +MainApp.root.ids.date.text+', '\
                        +MainApp.root.ids.cost_TextInput.text+';\n'
        # read the exsisting Text
        MainApp.root.ids.dataScreen_Label.text = self.MainApp.root.ids.dataScreen_Label.text + tmp
        #print(image_to_string(Image.open('20180414_104309.jpg')))
 #       pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tessdata'
     #   pytesseract.pytesseract.tesseract_cmd = "C:\\Temp\\kivy-android-app\\venv\\Lib\\site-packages\\tesseract"
      #  print(pytesseract.image_to_string(Image.open(r'C:\Temp\kivy-android-app\20180414_104309.jpg')))
 #       print(pytesseract.image_to_string(Image.open('20180414_104309.jpg')))
        MainApp.root.ids.cl.disabled = False

    def on_clear_click(self):
        '''

        :return:
        '''
        self.MainApp.root.ids.dataScreen_Label.text =''
        # Calendar()

    def kassabuch_get_categories_on_click(self):
        """

        :return:
        """
        self.contact_categories = self.MainApp.clientService.get_all_contact_categories()
        tmp_cat = []
        for cat in self.contact_categories :
            if not cat['attributes']['title'] == "Uncategorised":
                tmp_cat.append(cat['attributes']['title'])

        self.MainApp.logger.set_log(self.MainApp.root.ids.communicationScreen_Label, ' connect homepage' + '\n')
        self.MainApp.logger.set_log(self.MainApp.root.ids.communicationScreen_Label,
                                     ' get all categories of building '+ '\n' )

        self.MainApp.root.ids.category_Spinner.values = tmp_cat
        self.MainApp.root.ids.category_Spinner.disabled = False
        self.MainApp.root.ids.get_contacts.disabled = False

    def kassabuch_contacts_spinner_select(self, text):
        """

        :param text:
        :return:
        """
        print("text: "+text)
        self.mieter = text
        # enable all fields
        self.MainApp.root.ids.cost_TextInput.disabled = False
        self.MainApp.root.ids.cost_label.disabled = False
        self.MainApp.root.ids.date.disabled = False
        self.MainApp.root.ids.date_label.disabled = False
        # Button
        self.MainApp.root.ids.preview.disabled = False
       # self.MainApp.root.ids.cl.disabled = False
        self.MainApp.root.ids.send.disabled = False

    def kassabuch_category_spinner_select(self, text):
        """

        :param text:
        :return:
        """
        for cat in self.contact_categories :
            if not cat['attributes']['title'] == text:
                self.catid = cat['attributes']['id']
                return True

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



class PopupApp():

    def build(self, text, title = None):
        popup = Factory.ErrorPopup()
        popup.message.text = text
        if title:
            popup.title = title
        popup.open()

class Test(TabbedPanel):
    pass


class Logger:
    def __init__(self):
        pass

    def set_log(self,logger_label, text):
        tmp = self.get_time()+text
        logger_label.text = logger_label.text + tmp

    def get_time(self):
        """

        :rtype: object
        """
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Scroll:
    def __init__(self, main_app):
        """
          constructor
        :param main_app:  reference to root
        :param screen_label: label to be modified
        """
        self.main_app = main_app

    def add_text_to_screen(self, t, screen):
        """
          add a text to the screen
        :param text: text to be added
        :return:
        """

        if screen == 'communication':
            self.main_app.root.ids.communicationScreen_Label.text = self.main_app.root.ids.communicationScreen_Label.text + '\n' + str(
                    t)
        elif screen == 'data':
            te = json.dumps(t, sort_keys=True, indent=4)
            self.main_app.root.ids.dataScreen_Label.text = self.main_app.root.ids.dataScreen_Label.text + '\n' + str(
                    te)


class DataStore:
    def __init__(self, html_text):
        """

        """
        self.header_p = re.findall(r'<p>.*?</p>',html_text, re.DOTALL)
        self.body_t = re.findall(r'<table.*?</table>',html_text, re.DOTALL)
        # print("+++++++++++++++" + str(self.header_p)
        # print("+++++++++++++++" + str(self.body_t))
        #TODO: falls mehrere Tabelle übergeben wer
        self.html_table = pd.read_html(self.body_t[0], header=0)[0]
        print(self.html_table)
        #df = dfs[0]

    def modify_html_table(self, x_coord, y_coord, value):
        """
            modify an element of a table
        :param x_coord: coordination x
        :param y_coord: coordination y
        :param value: new value
        :return:
        """
        #print(dfs.loc[2,'Monat'])
        # dfs.loc[2,'Monat'] = 'Februar'
        self.dfs.loc[y_coord, x_coord] = value
        print(self.dfs)

    def add_entry(self,entry):
        """

        :param entry: list of string
        :return:
        """
        print(self.dfs.index)
        # hinzufuegen eines Elementes
        # self.dfs.loc[len(self.dfs.index)] = ['März', '12.', 'reto', 'Waschgeld', '20', '20', '0']
        #TODO: try catch? implementieren
        if entry is list:
            self.dfs.loc[len(self.dfs.index)] = entry
            print(self.dfs)
        else:
            return None

    def get_html_text(self):
        """

        :return:
        """
        table = self.html_table.to_html(index=False)
        header = ''
        for h in self.header_p:
            header = header + h
        text = header + table
        print(text)
        return text

    def __repr__(self):
        """
            get all Data as string NOT html formated
        :rtype: object
        """
        return "\n {0}  ".format(self.dataEntries)


    def getAllEntriesByArg(self, arg ):
        """

        :param arg:
        :return:
        """
        list = []
        for entry in self.dataEntries:
            if(arg =='name'):
                list.append(entry.jsonObject['attributes']['name'])
                print(entry.jsonObject['attributes']['name'])
        return list


if __name__ == "__main__":
    app = MainApp()
    app.run()