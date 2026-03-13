Seguridad y Autenticación
El sistema utiliza JWT (JSON Web Tokens) para la comunicación entre el Frontend y el Backend.

Endpoints de Autenticación:

POST /api/registro/: Registro de nuevos usuarios.

POST /api/token/: Login. Devuelve un access y un refresh token.

POST /api/token/refresh/: Renueva el token de acceso.

Permisos:

Se aplica la política IsAuthenticatedOrReadOnly.

Cualquier usuario puede ver los garajes disponibles.

Solo los usuarios autenticados pueden crear, editar o eliminar garajes.