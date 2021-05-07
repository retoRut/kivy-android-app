import json
from datetime import datetime

from PIL.ImageShow import show
from kivy.app import App
from kivy.factory import Factory
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel
#import Image
#from tesseract import image_to_string
import connector
#import cv2



from PIL import Image

import pytesseract


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
        self.clientService = connector.JoomlaConnectorService(backend, apikey)
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
        self.building = 0

    def periode_Spinner_values(self):
        """
            set spinner values of Nebenkosten period
        :return: list of dates
        """
        list= ['1-7-2020-30-6-2021','1-7-2021-30-6-2022','1-7-2022-30-6-2023','1-7-2023-30-6-2024']
        # print(list)
        return list

    def building_Spinner_values(self):
        """

        :return:
        """
        list= ['Hörnlistrasse 3','Hörnlistrasse 5']
        # print(list)
        return list

    def get_mieter_click(self):
        """

        :return:
        """
        if(self.building ==0 ):
            PopupApp().build("Please select a building first")
        else:
            list = self.MainApp.clientService.get_all_contacts_by_name_and_building(self.building)
            print(list)
            self.MainApp.logger.set_log(self.MainApp.root.ids.communicationScreen_Label, ' connect homepage' + '\n')
            self.MainApp.logger.set_log(self.MainApp.root.ids.communicationScreen_Label,
                                     ' get all contacts of building '+str(self.building)+ '\n' )
            self.ids.mieter_Spinner.values = list
            self.MainApp.root.ids.mieter_Spinner.disabled = False

    def get_spinner_mieter_values(self):
        '''
         get all Clients (mieter from the homepage)
        :return:
        '''
        print('run get_spinner_mieter_values')

        # list = self.clientService.get_all_contacts_by_name()
        list= ['1','2']
        # print(list)
        return list

    def on_periode_select(self, text):
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

    def on_preview_click(self):
        """
        add an entry to list
        :return:
        """
        #create the new one:
        tmp = self.MainApp.root.ids.periode_Spinner.text+','\
                      +self.MainApp.root.ids.building_Spinner.text+',' \
                      + self.MainApp.root.ids.mieter_Spinner.text + ',' \
                       +self.MainApp.root.ids.date.text+', '\
                        +self.MainApp.root.ids.cost_TextInput.text+';\n'
        # read the exsisting Text
        self.MainApp.root.ids.dataScreen_Label.text = self.MainApp.root.ids.dataScreen_Label.text + tmp
        #print(image_to_string(Image.open('20180414_104309.jpg')))
 #       pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tessdata'
     #   pytesseract.pytesseract.tesseract_cmd = "C:\\Temp\\kivy-android-app\\venv\\Lib\\site-packages\\tesseract"
      #  print(pytesseract.image_to_string(Image.open(r'C:\Temp\kivy-android-app\20180414_104309.jpg')))
 #       print(pytesseract.image_to_string(Image.open('20180414_104309.jpg')))
        self.MainApp.root.ids.cl.disabled = False

    def on_clear_click(self):
        '''

        :return:
        '''
        self.MainApp.root.ids.dataScreen_Label.text =''

    def get_haus_click(self):

        self.contact_categories = self.MainApp.clientService.get_all_contact_categories()
        tmp_cat = []
        for cat in self.contact_categories :
            if not cat['attributes']['title'] == "Uncategorised":
                tmp_cat.append(cat['attributes']['title'])

        self.MainApp.logger.set_log(self.MainApp.root.ids.communicationScreen_Label, ' connect homepage' + '\n')
        self.MainApp.logger.set_log(self.MainApp.root.ids.communicationScreen_Label,
                                     ' get all categories of building '+ '\n' )
        self.ids.building_Spinner.values = tmp_cat
        self.MainApp.root.ids.building_Spinner.disabled = False

    def on_mieter_select(self, text):
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


    def on_building_select(self,cat_title):
        """

        :param id:
        :return:
        """
        print("cat Title: "+cat_title)
        for cat in self.contact_categories:
            print(cat)
            if cat['attributes']['title'] == cat_title:
                self.building = cat['attributes']['id']
                break

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

    def build(self, text):
        popup = Factory.ErrorPopup()
        popup.message.text = text
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

if __name__ == "__main__":
    app = MainApp()
    app.run()