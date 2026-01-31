# Imagen base con PHP y Apache
FROM php:8.2-apache

# Habilitar mod_rewrite (para APIs / frameworks)
RUN a2enmod rewrite

# Instalar dependencias del sistema necesarias para PHP
RUN apt-get update && apt-get install -y \
    git \
    unzip \
    libzip-dev \
    && docker-php-ext-install zip pdo pdo_mysql \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Directorio de trabajo
WORKDIR /var/www/html

# Copiar composer primero (mejora cache)
COPY backend/composer.json backend/composer.lock ./

# Instalar dependencias PHP (sin dev, optimizado)
RUN composer install --no-dev --optimize-autoloader --no-interaction

# Copiar el resto del código del backend
COPY backend/ ./

# Permisos (importante en Linux)
RUN chown -R www-data:www-data /var/www/html

# Exponer puerto 80
EXPOSE 80

# Apache en primer plano
CMD ["apache2-foreground"]
