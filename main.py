import json

import requests
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


Builder.load_string('''
<MainLayout>
    orientation:"vertical"
    text: 'communication to website..'
    ScrollView:
        id: scroll
        Label:
            id:screen
            text:root.text
            size_hint: 1, None
            height: self.texture_size[1]
            halign:'left'
            font_size:'40'    
    BoxLayout: 
        orientation:"vertical" 
        Button:
            id:get
            text: "GET"
            on_press: root.on_get_click()
        Button:
            id:create
            text: "CREATE"
            on_press: root.on_create_click() 
        Button:
            id:put   
            text: "PUT"
            on_press: root.on_put_click()
        Button:
            id:clear   
            text: "CLEAR"
            on_press: root.on_clear_click()
''')


class MainApp(App):
    def build(self):
        """
            Application for API calls

        :return:
        """
       # clientService = ClientService()
      #  main_layout = BoxLayout(orientation="vertical")
        self.clientService = ClientService()
        main_layout = MainLayout()
        main_layout.setClientServcie(self.clientService)
        return main_layout

    def jprint(self, obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)


class MainLayout(BoxLayout):
    screen = StringProperty(' ')

    def setClientServcie(self, clientService):
        '''
            set the CleitnService for connecting to the homepage
        :param clientService:
        :return:
        '''
        self.clientService = clientService


    def on_get_click(self):
        """
             get Articel
            :param instance:
            :return:
        """
        print(" button_get")
        tmp = json.dumps(self.clientService.getAllContacts(), sort_keys=True, indent=4)
        #print(tmp)
        self.text = tmp

    def on_create_click(self, instance):
        """
         get Articel
        :param instance:
        :return:
        """

    def on_put_click(self, instance):
        """
         get Articel
        :param instance:
        :return:
        """
    def on_clear_click(self):
        '''

        :return:
        '''
        self.text = ' '


class ClientService:

    def __init__(self):
        self.backend = 'https://rutishauser-ag.ch'
        #self.backend = 'https://193.246.38.195'
        self.apikey = 'c2hhMjU2OjM1OjI1N2RmNjRmY2UxYTFiMDE2ODcxMmY0YWE5NGYyYWQ4MzkwM2JkZjA2YTNkZmM3NzAwNGExZmE3MmUyYThmZTY='
        self.headers = {
            'Authorization': 'Bearer ' + str(self.apikey),
            'Content-Type': 'application/json',
        }

    def getAllContacts(self):
        """
            get all contacts from the homepage
        :return: json of all contacts
        """
        url = self.backend + '/api/index.php/v1/contact'
        response = requests.request('GET', url, headers=self.headers)
        # self.jprint.jprint(response.json()['data'])
        return response.json()['data']


if __name__ == "__main__":
    app = MainApp()
    app.run()


