# TODO

## next-generation
* utilidad local de gestion de usuarios (CRUD)

	* completar el modulo admin con las funciones parser(). ¿como parseamos el full name? ¿con _ ?

* consultar como se añade la api key en una peticon http
	curl https://api.example.com/endpoint \
  	-H "Authorization: Bearer YOUR_API_KEY"
  	o bien
  	curl https://api.example.com/endpoint \
  	-H "X-API-Key: YOUR_API_KEY"


* capa nueva nixnox-api con servidor https usando fastapi
	- No asyncio pq la bd puede ser LibSQL
	- validacion con pydantic

## Antiguo
* Deployment using docker
	- Enviroment variables, sql connection
	- External Volume
* Manual data entry
* Dockerfile para desarrollo con sqlite3 y para produccion (maria?)
* desplegar docker en la respberry
* cerfificado real de stars4all?
* Authorised users?
* LibSQL:
	- docker
	- consult error to forum (write an example with SQLAlchemy and capture errors in server)
* check geo coords consistency in TAS (mejorar lo hecho?)
