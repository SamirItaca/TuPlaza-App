FROM node:20-alpine AS build
WORKDIR /app

# Copiar package.json y package-lock.json (mejor que solo package.json)
COPY frontend/tuplaza-angular/package*.json ./

# Instalar dependencias de forma limpia
RUN npm ci

# Copiar todo el proyecto
COPY frontend/tuplaza-angular/ ./

# Compilar Angular para producción
RUN npm run build --prod

FROM nginx:alpine

# Copiar configuración de nginx
COPY deployment/frontend/nginx.conf /etc/nginx/nginx.conf

# Copiar el build de Angular
COPY --from=build /app/dist/tuplaza-angular /usr/share/nginx/html

# Exponer el puerto 80
EXPOSE 80

# Comando por defecto
CMD ["nginx", "-g", "daemon off;"]