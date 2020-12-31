import requests
import json



class ClientService:
   # backend = None
   # username = 'reto'
    # password = 'api-rutag-api'
    #password = 'retorutishauser1976'

    def __init__(self, backend, apikey):
        self.backend = backend
        #self.key = apikey
        self.headers = {
            'Authorization': 'Bearer ' + str(apikey),
            'Content-Type': 'application/json',
        }
        #self.jprint = jsonprint()



class JoomlaConnectorService(ClientService):

    def __init__(self, backend, apikey):
        super().__init__(backend, apikey)


    def getAllArticles(self):
        url = self.backend+'/api/index.php/v1/content/article'
        response = requests.request('GET', url, headers=self.headers)
        return response.json()


    def getArticle(self,alias):
        url = self.backend+'/api/index.php/v1/content/article'
        response = requests.request('GET', url, headers=self.headers)
        #jprint(response.json())
        res = response.json()
        for i in res['data']:
            if i['attributes']['alias'] == alias:
                return i['attributes']
        return False

    def getAllCategories(self):
        """

        :rtype: object
        """
        url = self.backend+'/api/index.php/v1/banners/categories'
        response = requests.request('GET', url, headers=self.headers)
        return response.json()

    def getCategorieID(self,name):
        url = self.backend+'/api/index.php/v1/content/categories'
        response = requests.request('GET', url, headers=self.headers)
        #self.jprint(response.json())
        res = response.json()
        for i in res['data']:
            if i['attributes']['title'] == name:
                return str(i['attributes']['id'])
        return False

    def createNewArticle(self,alias,title,text, catID, mainLayout):
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


    def getAllUsersByName(self):
        userlist = []
        url = self.backend+'/api/index.php/v1/users'
        response = requests.request('GET', url, headers=self.headers)
        res = response.json()
        for user in res['data'] :
            userlist.append(user['attributes']['name'])
        return userlist


    def getAllUsers(self):
        url = self.backend+'/api/index.php/v1/users'
        response = requests.request('GET', url, headers=self.headers)
        return response.json()

    def getAllContactsByName(self):
        userlist = []
        url = self.backend+'/api/index.php/v1/contact'
        response = requests.request('GET', url, headers=self.headers)
        res = response.json()
        for user in res['data'] :
            userlist.append(user['attributes']['name'])
            #self.jprint.jprint(user['attributes'])
        return userlist


    def getAllContacts(self):
        """
            get all contacts from the homepage
        :return: json of all contacts
        """
        url = self.backend+'/api/index.php/v1/contact'
        response = requests.request('GET', url, headers=self.headers)
        #self.jprint.jprint(response.json()['data'])
        return response.json()['data']

