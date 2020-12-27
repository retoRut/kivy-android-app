import json
from datetime import datetime

import requests
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup


Builder.load_string('''
<MainLayout>
    orientation:"vertical"
    textCSc: 'communication to website..'
    textDSc:'data to sent ..'
    ScrollView:
        id: scroll
        Label:
            id:communication-screen
            text:root.textCSc
            size_hint: 1, None
            height: self.texture_size[1]
            halign:'left'
            font_size:'40' 
    ScrollView:
        id: scroll2
        Label:
            id:data-screen
            text:root.textDSc
            size_hint: 1, None
            height: self.texture_size[1]
            halign:'left'
            font_size:'40'    
    BoxLayout: 
        orientation:"vertical" 
        BoxLayout:
            orientation:"horizontal"
            Label:
                id:mieter_label
                text:'MIETER'
                size_hint_x: 20 
            Spinner:
                id: mieter
                text: "Mieter"                   #default value showed
                values: root.getSpinnerValues()      #list of values to show
                on_text:  root.on_mieter_select(self.text)
                size_hint_x: 20 
        BoxLayout:
            orientation:"horizontal"
            Label:
                id:date_label
                text:'DATUM'
                size_hint_x: 20                
            TextInput:
                id:date
                text:root.on_date_text()
                size_hint_x: 20
        BoxLayout:
            orientation:"horizontal"
            Label:
                id:duration_label
                text:'DAUER'
                size_hint_x: 20  
            TextInput:
                id:duration_textInput
                text:'5h'
                size_hint_x: 20
        BoxLayout:
            orientation:"horizontal"
            Label:
                id:typ_label
                text:'TYP'
                size_hint_x: 20
            Spinner:
                id: typ
                #text: " "                   #default value showed
                values: ['Waschmaschiene','Tumbler']    #list of values to show
                on_text:  root.on_typ_select(self.text)
                size_hint_x: 20 
        BoxLayout:
            orientation:"horizontal"
            Label:
                id:cost_label
                text:'KOSTEN'
                size_hint_x: 20
            TextInput:
                id:kosten
                text:'SFR 2.50'
                size_hint_x: 20
        BoxLayout: 
            orientation:"horizontal"
            Button:
                id:add
                text: "ADD"
                on_press: root.on_add_click()
            Button:
                id:clear
                text: "CLEAR"
                on_press: root.on_clear_click() 
            Button:
                id:send   
                text: "SEND"
                on_press: root.on_send_click()  
<CreatePopup>:
    id:pop
    size_hint: .4, .4
    auto_dismiss: False
    title: 'Create new Machine usage'
    Button:
        text: 'Click here to dismiss'
        on_press: pop.dismiss()
   
        
''')


class MainApp(App):
    clientService = None
    def build(self):
        """
            Application for API calls

        :return:
        """
        main_layout = MainLayout()
     #   main_layout.setClientService(self.clientService)
    #    self.dropdown = CustomDropDown()
        return main_layout

    def jprint(self, obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)




class MainLayout(BoxLayout):
    screen = StringProperty(' ')
    state = True

    def getSpinnerValues(self):
        self.clientService = ClientService()
        list = self.clientService.getAllContactsByName()
        print(list)
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

    def on_create_click(self):
        """
         get Articel
        :param instance:
        :return:
        """
        pops=CreatePopup()
        pops.open()

    def on_put_click(self):
        """
         get Articel
        :param instance:
        :return:
        """
    def on_clear_click(self):
        '''

        :return:
        '''
       # self.text = ' '

    def on_mieter_select(self, text):
    # do whatever you want to do, note that the "text" value will be the one that user selected
        print("text: "+text)

    def on_date_text(self):
        return datetime.now().strftime('%d.%m.%Y')


    def on_typ_select(self, text):
        print(text)

 #   def setDate(self):
 #       self.cal = CalendarWidget(as_popup=True)
 #       self.popup = Popup(title='Calendar', content=self.cal, size_hint=(1, 1))
 #       self.popup.open()




class CreatePopup(Popup):
    pass


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

    def getAllContactsByName(self):
        '''

        :return:
        '''
        userlist = []
        url = self.backend+'/api/index.php/v1/contact'
        response = requests.request('GET', url, headers=self.headers)
        res = response.json()
        for user in res['data'] :
            userlist.append(user['attributes']['name'])
            #self.jprint.jprint(user['attributes'])
        return userlist

if __name__ == "__main__":

    app = MainApp()
    app.run()


