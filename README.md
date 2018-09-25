# geocoding-service-proxy-simple

A simple geo coding proxy service to resolve the latitude and longitude of a given address using third party geo coding services. Should a third party service fail to respond or a network error occur, the proxy should fallback to another one.


## Requirements Satisfaction

* Implemented in Python

  The code is implemented using python 3

* Support Multiple Geocoding Services

  I used Here and google maps geo coding services. Initially tried out with cusum services like, locationiq.com as well. But   then         limited to google and HERE finally. A list of 3 servers were maintainted, the first one backup.com being invalid one,  so that every     time the test is done, there is a failure and the proxy is falling back to another one.

* Implements Fallback To Backup Geocoding Services

  I had thought about a 3-4 altenatives of fall back mechanisms and was working on all of them. But finally just limited to a sequntial     fall back for simplicity purposes. The other fall back mechanisms  i was trying worth mentioneing are random, everytime we give an       address, the service tried a service at random. A third alternative was to have the geocoding servers at differene priorities based on   the costs. But i have converted this scenario to a sequential one, which is why i preferred to implement the sequential option in the     end.

* RESTful HTTP Interface

  A HTTP Client class is defined to handle the requests.

* JSON for Data Serialization

  Used Json to return the data via the interface.

* Provides Documentation - How To Run The Service

  Provided below how to run.

* Provides Documentation - How To Use The Services API

  The gcsproxy module needs to be imported and using the GCSProxy class the request_location method needsto be called.

* Uses git and github for for revision control

  The code is uploaded to github under this repo.

## Running the Application

* A Python environment is created with requirements listed in requirements.txt 
* Run gcsapp.py as 'python gcsapp.py'
* Point the browser to http://localhost:5000/api/v1/location?addr= followed by addres string.
* The browser displays the latitude and longitude for the address in json format.

  For example, if the address string is 'San Franciso', the browser displays, 

  {"Latitude":37.77713,"Longitude":-122.41964} 

## Running the Application (via Cli)

* The API can be tested using cli using curl.

  gvenkat@PT7910:~$ curl -i http://localhost:5000/api/v1/location?addr=San+Francisco

  HTTP/1.0 200 OK

  Content-Type: application/json

  Content-Length: 45

  Server: Werkzeug/0.14.1 Python/3.6.6

  Date: Tue, 25 Sep 2018 05:43:07 GMT


  {"Latitude":37.77713,"Longitude":-122.41964}

  gvenkat@PT7910:~$ 



  Note: While using curl, we need to make sure the address string is not seaparated by spaces. Otherwise curl thinks it's a separate       host.



  gvenkat@PT7910:~$ curl -i http://localhost:5000/api/v1/location?addr=San Francisco

  HTTP/1.0 200 OK

  Content-Type: application/json

  Content-Length: 43

  Server: Werkzeug/0.14.1 Python/3.6.6

  Date: Tue, 25 Sep 2018 05:39:54 GMT


  {"Latitude":41.68663,"Longitude":15.37752}

  curl: (6) Could not resolve host: Francisco




