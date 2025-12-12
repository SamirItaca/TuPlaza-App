FLUJO DEL DESPLIEGUE AUTOMATICO DEL FRONT (Proyecto Angular)

- Push a master: 
    Cada vez que se haga push a la rama master, GitHub Actions dispara el workflow (pipeline) de .github/workflows/deploy-frontend.yml.

- Checkout del código y setup de Node: 
    Clona el repo. 
    Instala Node.js 20 y configura caché de npm para acelerar futuras ejecuciones.

- Instalar dependencias y compilar Angular: 
    npm ci instala dependencias reproducibles. 
    npm run build --prod genera los archivos de producción de Angular en dist/tuplaza-angular/.

- Docker build: 
    El Dockerfile de "frontend/Dockerfile" toma esos archivos compilados y los sirve con Nginx. 
    La configuración de nginx.conf asegura que Angular SPA funcione correctamente (rutas gestionadas por Angular, cache de assets, etc.). 
    Se genera la imagen Docker "tuplaza-frontend".

- Login y push a Docker Hub: 
    La imagen se etiqueta y se sube a un repositorio de Docker Hub usando unas credenciales (secretos).

- Despliegue en el servidor: 
    GitHub Actions se conecta vía SSH al servidor. 
    Descarga la última versión de la imagen (docker pull).
    Detiene y elimina cualquier contenedor anterior.
    Levanta un nuevo contenedor en el puerto 80 (docker run -d -p 80:80).

- Acceso a la web
    Angular estará disponible desde cualquier navegador en: http://79.116.49.226/

    
