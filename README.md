# geocoding-service-proxy-simple

A simple geo coding proxy service to resolve the latitude and longitude of a given address using third party geo coding services. Should a third party service fail to respond or a network error occur, the proxy should fallback to another one.

## Running the Application

* A Python cnvironment is created with requirements listed in requirements.txt 
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

Note: While using cure, we need to make sure the address string is not seaparated by spaces. Otherwise curl thinks it's a separate host.

gvenkat@PT7910:~$ curl -i http://localhost:5000/api/v1/location?addr=San Francisco
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 43
Server: Werkzeug/0.14.1 Python/3.6.6
Date: Tue, 25 Sep 2018 05:39:54 GMT

{"Latitude":41.68663,"Longitude":15.37752}
curl: (6) Could not resolve host: Francisco
gvenkat@PT7910:~/SDCND/CarND-MPC-Project/build$

