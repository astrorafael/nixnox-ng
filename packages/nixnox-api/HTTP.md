# FastAPI Codes

Los más usados en APIs REST:

| Código                                                      | Nombre                                                               | Uso en FastAPI / API REST                                                                   |
| ----------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| HTTP_400_BAD_REQUEST                                        | Bad Request                                                          | Error genérico del cliente: datos inválidos, solicitud malformada fastapi.tiangolo+1        |
| HTTP_401_UNAUTHORIZED\| Unauthorized                        | Usuario no autenticado: falta token, cookie o credenciales inválidas |                                                                                             |
| HTTP_403_FORBIDDEN                                          | Forbidden                                                            | Usuario autenticado pero no tiene permiso para acceder al recurso                           |
| HTTP_404_NOT_FOUND                                          | Not Found                                                            | Recurso no existe (usuario, organización, item) o ruta no válida fastapi.tiangolo+1         |
| HTTP_405_METHOD_NOT_ALLOWED                                 | Method Not Allowed                                                   | Método HTTP no permitido en esa ruta (ej. POST en endpoint solo GET)                        |
| HTTP_409_CONFLICT                                           | Conflict                                                             | Recurso ya existe o estado conflictivo (ej. persona/organización duplicada) stackoverflow+1 |
| HTTP_410_GATEWAY_TIMEOUT ❌ (no es 410) → HTTP_410_NOT_FOUND | Not Found (permanente)                                               | Recurso eliminado permanentemente (a veces se usa 404 instead)                              |
| HTTP_422_UNPROCESSABLE_CONTENT                              | Unprocessable Content                                                | Error de validación semántica (datos válidos en formato pero inválidos en contenido)        |
| HTTP_429_TOO_MANY_REQUESTS                                  | Too Many Requests                                                    | Cliente excedió límite de rate limiting                                                     |

Códigos más específicos (menos comunes pero útiles):


| Código                                                     | Nombre                                                                  | Uso                                                                    |
| ---------------------------------------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| HTTP_400_BAD_REQUEST                                       | Bad Request                                                             | Solicitud malformada o parámetros inválidos genéricos fastapi.tiangolo |
| HTTP_401_UNAUTHORIZED                                      | Unauthorized                                                            | Autenticación fallida o ausente                                        |
| HTTP_403_FORBIDDEN                                         | Forbidden                                                               | Autenticado pero sin permiso (role-based access)                       |
| HTTP_405_METHOD_NOT_ALLOWED\| Method Not Allowed           | Método HTTP no permitido en esa ruta                                    |                                                                        |
| HTTP_406_NOT_ACCEPTABLE                                    | Not Acceptable                                                          | Formato de respuesta no aceptable (ej. Accept header)                  |
| HTTP_408_REQUEST_TIMEOUT                                   | Request Timeout                                                         | Cliente tardó demasiado en enviar la solicitud                         |
| HTTP_412_PRECONDITION_FAILED\| Precondition Failed         | If-Match, If-None-Match no se cumple (uso en operaciones condicionales) |                                                                        |
| HTTP_413_REQUEST_TOO_LARGE\| Request Too Large             | Body demasiado grande (excede límite del servidor)                      |                                                                        |
| HTTP_414_URI_TOO_LONG                                      | URI Too Long                                                            | URL demasiado larga                                                    |
| HTTP_415_UNSUPPORTED_MEDIA_TYPE\| Unsupported Media Type   | Content-Type no soportado (ej. enviar JSON como application/xml)        |                                                                        |
| HTTP_428_UNREPEATABLE_REQUEST\| Unrepeatable Request (rare) | Solicitud repetida demasiado rápido (rarely usado)                      |                                                                        |