import json
import chardet

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
        button_layout = BoxLayout(orientation="vertical")

        self.solution = TextInput(
            multiline=True, readonly=True, halign="left", font_size=40
        )
        main_layout.add_widget(self.solution)
        get_button = Button(
            text="GET", pos_hint={"center_x": 0.5, "center_y": 0.2}
        )
        get_button.bind(on_press=self.on_get_click)

        create_button = Button(
            text="CREATE", pos_hint={"center_x": 0.5, "center_y": 0.2}
        )
        create_button.bind(on_press=self.on_create_click)

        put_button = Button(
            text="PUT", pos_hint={"center_x": 0.5, "center_y": 0.2}
        )
        put_button.bind(on_press=self.on_put_click)

        button_layout.add_widget(get_button)
        button_layout.add_widget(create_button)
        button_layout.add_widget(put_button)
        main_layout.add_widget(button_layout)
        return main_layout

    def jprint(self, obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    def on_get_click(self, instance):
        """
         get Articel
        :param instance:
        :return:
        """
        self.solution.text = json.dumps(self.clientService.getAllContacts(), sort_keys=True, indent=4)

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