import json

import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class MainApp(App):
    def build(self):
        """
            Application for API calls

        :return:
        """
        self.clientService = ClientService()
        main_layout = BoxLayout(orientation="vertical")
        self.solution = TextInput(
            multiline=True, readonly=True, halign="left", font_size=20
        )
        main_layout.add_widget(self.solution)
        get_button = Button(
            text="GET", pos_hint={"center_x": 0.5, "center_y": 0.2}
        )
        get_button.bind(on_press=self.on_solution)
        main_layout.add_widget(get_button)
        return main_layout

    def jprint(self, obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    def on_solution(self, instance):
        """
         get Articel
        :param instance:
        :return:
        """
        text = 'GET'
        #    solution = str(eval(self.solution.text))
        self.solution.text = json.dumps(self.clientService.getAllContacts(), sort_keys=True, indent=4)




class ClientService:

    def __init__(self):
        self.backend = 'https://rutishauser-ag.ch'
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