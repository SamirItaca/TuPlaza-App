Control de versiones: git flow

Front: 
	Nodejs 20.19.0, npm 10.x.x, Angular 20.x.x
	Instalar NVM
	NVM instala Nodejs 20.19.0 (nvm install 20.19.0)
	nvm use 20.19.0
	Verificar versiones (node -v, npm -v)
	Instalar Angular Cli (npm install -g @angular/cli@latest)

Backend:
	Laravel 

Deployment: 
	Dockerfile para crear imagenes del proyecto Frontend y Backend.
	2 Docker-compose (MySQL con PhpMyAdmin)
		mysql-prod: tuplaza.ddns.net:1011
		mysql-dev: tuplaza.ddns.net:1010

Servidor:
	user: tuplaza
	pass: tuplazapass