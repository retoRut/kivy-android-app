import requests
import json



class ClientService:
   # backend = None
   # username = 'reto'
    # password = 'api-rutag-api'
    #password = 'retorutishauser1976'

    def __init__(self, backend, apikey):
        """
            init
        :param backend: url of backend
        :param apikey:  access key
        """
        self.backend = backend
        #self.key = apikey
        self.headers = {
            'Authorization': 'Bearer ' + str(apikey),
            'Content-Type': 'application/json',
        }




class JoomlaConnectorService(ClientService):

    def __init__(self, backend, apikey):
        """

        :param backend: url of backend
        :param apikey: access key
        """
        super().__init__(backend, apikey)

    def get_all_articles(self):
        """
            Get all articles from the joomla website
        :return:
        """
        url = self.backend+'/api/index.php/v1/content/article'
        response = requests.request('GET', url, headers=self.headers)
        return response.json()

    def get_article(self, alias):
        """

        :param alias:
        :return:
        """
        url = self.backend+'/api/index.php/v1/content/article'
        response = requests.request('GET', url, headers=self.headers)
        #jprint(response.json())
        res = response.json()
        for i in res['data']:
            if i['attributes']['alias'] == alias:
                return i['attributes']
        return False

    def get_all_categories(self):
        """

        :rtype: object
        """
        url = self.backend+'/api/index.php/v1/banners/categories'
        response = requests.request('GET', url, headers=self.headers)
        return response.json()

    def get_categorie_id(self, name):
        """

        :param name:
        :return:
        """
        url = self.backend+'/api/index.php/v1/content/categories'
        response = requests.request('GET', url, headers=self.headers)
        #self.jprint(response.json())
        res = response.json()
        for i in res['data']:
            if i['attributes']['title'] == name:
                return str(i['attributes']['id'])
        return False

    def create_new_article(self, alias, title, text, catID, mainLayout):
        """

        :param alias:
        :param title:
        :param text:
        :param catID:
        :param mainLayout:
        :return:
        """
        url = self.backend+'/api/index.php/v1/content/article'
        post = json.dumps({
        'alias': str(alias),
        'articletext': str(text),
        'catid': catID,
        'language':'*',
        'metadesc':'',
        'metakey':'',
        'title': str(title)
        })
        #self.jprint.jprint(post)
        response = requests.request('POST', url, headers=self.headers, data=post)
        mainLayout.root.ids.communicationScreen_Label.text = mainLayout.root.ids.communicationScreen_Label.text+ '\n' + 'received status Code:'+str(response.status_code)
        print(response.headers)
        print(response.text.encode('utf8'))

    def get_all_users_by_name(self):
        """
            get the name of all users
        :return: names as json
        """
        userlist = []
        url = self.backend+'/api/index.php/v1/users'
        response = requests.request('GET', url, headers=self.headers)
        res = response.json()
        for user in res['data'] :
            userlist.append(user['attributes']['name'])
        return userlist

    def get_all_users(self):
        """
            get all Users from the joomla website
        :return: users as json
        """
        url = self.backend+'/api/index.php/v1/users'
        response = requests.request('GET', url, headers=self.headers)
        return response.json()

    def get_all_contacts_by_name_and_building(self, building):
        """
            get all names from the contacts (not homepage user) of the joomla homepage
        :return: contact names as list
        """
        userlist = []
        url = self.backend+'/api/index.php/v1/contact'
        response = requests.request('GET', url, headers=self.headers)
        res = response.json()
        text = json.dumps(res, sort_keys=True, indent=4)
        print(text)
        for user in res['data'] :
            if building == user['attributes']['catid']:
                userlist.append(user['attributes']['name'])
            #self.jprint.jprint(user['attributes'])
        return userlist

    def get_all_contact_categories(self):
        """

        :return:
        """
        url = self.backend+'/api/index.php/v1/contact/categories'
        response = requests.request('GET', url, headers=self.headers)
        res = response.json()
        text = json.dumps(res, sort_keys=True, indent=4)
        print(text)
        return res['data']


    def get_all_contacts(self):
        """
            get all contacts from the homepage
        :return: contacts as json
        """
        url = self.backend+'/api/index.php/v1/contact'
        response = requests.request('GET', url, headers=self.headers)
        #self.jprint.jprint(response.json()['data'])
        return response.json()['data']

