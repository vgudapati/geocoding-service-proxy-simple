import requests
import json


class HTTPClient():

    def __init__(self):
        self.request  = None
        self.response = None
        self.headers  = {'Content-Type':'application/json',
                         'Accept':'application/json'}
        self.userid   = None
        self.error    = None
        self.status   = None
        self.token    = None

    def setExtras(self, **extra):
        if extra:
            if "token" in extra:
                self.token=extra["token"]
                self.headers.update({'X-Auth-Token':self.token})


    def http_request(self, method='GET', url=None, **extra):
        r = None

        if not url:
             print ("Url has to be provided")
             return None
        if extra:
            self.setExtras(**extra)
        try:
            if "GET" in method:
                print("Inside get reuqest")
                r = requests.request('get', url)
                print("Got resp :", r.json(), "\n", r.status_code)

        except Exception as e:
            print ("Error code received %s " % str(e))
            return None
        except requests.ConnectionError:
            print ("Not able to connect to the server")
            return None
        else:
            resp_code= r.status_code
            if resp_code != 200:
                print ("Status code: ", r.status_code)
                self.response = r.json()
                return self.response
            else:
                self.response = json.dumps(r.json())
                self.response = json.loads(self.response)
                return self.response


class GCSProxy(object):
   """
   Backend proxy towards the Geo Decoding Servers.

   The proxy will process the request towards the
   GDS server. Uses couple of servers 'active' and
   'backup'. If 'active' fails will choose 'backup'
   to request for the location.
   """
   INIT = 0
   READY = 1

   def __init__(self):
       self.current_active = 1
       self.current_address = ''
       self.servers = ['https://backup.com/',
                       'https://geocoder.api.here.com/',
                       'https://maps.googleapis.com/'
                       ]
       self.handle = [None] * len(self.servers)
   def start(self):
       """
       Initialize with the backend servers.

       Servers might need authentication to process
       multiple requests.
       Marks the active server to request for.
       """
       for index, serverroot in enumerate(self.servers):
           if not serverroot:
               continue
           self.handle[index] = HTTPClient()

   def get_active_server(self):
       """
       Check for liveliness of the backend servers.
       Mark the current active one.
       """
       if self.current_active == 1:
           res = self.request_location(self.current_address)
           if not res:
               current_active = 2
           else:
               current_active = 0
       elif self.current_active == 2:
           res = self.request_location(self.current_address)
           if not res:
               current_active = 1
           else:
               current_active = 0

   def format_address(self, address):
       """
       Format the address string to url parameters

       :param address: address string in string format
       """

       r = address.split()

       r = "+".join(r)

       if self.current_active == 0:
           r = 'v1/search_sandbox.php?format=json&q=' + r + '&accept-language=en'
       elif self.current_active == 1:
           r = '6.2/geocode.json?searchtext=' + r + '&app_id=gQjAbSdrJjFlgeKGY9X1' + \
                '&app_code=7wdByIc_ZAvv_st1b_Gtyg'
       elif self.current_active == 2:
           r = 'maps/api/geocode/json?address=' + r + '&key=AIzaSyA2l-d3TmWW3exoaz_Bg6WkCQYjRtO9gXw'
                  
       return self.servers[self.current_active] + r

   def request_location(self, address):
        """
        Request the location for a give address.

        :param address: address in a string form
        """
       
        number_of_servers = len(self.servers)
        res = []
        i = 0
        #self.current_active =  self.servers[i]
        while not res and i < number_of_servers:
            self.current_active =  i
            
            requrl = self.format_address(address)
            print("requrl :", requrl)
            print("active server :", self.current_active)
            print("handle :", self.handle[self.current_active])
            
            try:
                res = self.handle[self.current_active].http_request(url=requrl)
                print ("result is :", res)
            except Exception as e:
                print("Got exception", e)
            
            i += 1
            
            if res:
                break
                
        return res, self.current_active
       
       
       
       
       
       
       
       #https://geocoder.api.here.com/6.2/geocode.json?searchtext=1440%20Stone%20Pine%20Terrace%20Fremont%20CA&app_id=gQjAbSdrJjFlgeKGY9X1&app_code=7wdByIc_ZAvv_st1b_Gtyg
       
       
       #https://maps.googleapis.com/maps/api/geocode/json?address=1440%20Stone%20Pine%20Terrace%20Fremont%20CA&key=AIzaSyA2l-d3TmWW3exoaz_Bg6WkCQYjRtO9gXw
       
       
       
