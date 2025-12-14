# Stage 1: Build Angular App
FROM node:20-alpine AS build
WORKDIR /app

# Copiar package.json y package-lock.json
COPY ../../frontend/tuplaza-angular/package*.json ./

# Instalar dependencias
RUN npm ci

# Copiar todo el proyecto Angular
COPY ../../frontend/tuplaza-angular/ ./

# Compilar Angular para producción
RUN npm run build --prod

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copiar configuración personalizada de nginx
COPY deployment/frontend/nginx.conf /etc/nginx/nginx.conf

# Copiar build de Angular
COPY --from=build /app/dist/tuplaza-angular /usr/share/nginx/html

# Exponer el puerto 80
EXPOSE 80

# Comando por defecto
CMD ["nginx", "-g", "daemon off;"]
