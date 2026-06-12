# nixnox-api

The NinNox HTTP API layer exposing REST services and authenticated by an apy key.

# HTTP API

POST /v1/persons - Create a new Observer (person). Returns api_key + obs_id
POST /v1/organizations - Create a new Observer (Organization). returns api_key + obs_id

GET /v1/persons - List all persons [authenticated] [admin]
GET /v1/organizations - List all organizations

PUT /v1/person/<id> - Modify Person data [authenticated] 
POST /v1/person/<id>/clone - Clone person data entry [authenticated]