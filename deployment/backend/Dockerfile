FROM php:8.5-apache

# Habilitar mod_rewrite e instalar dependencias
RUN a2enmod rewrite \
    && apt-get update && apt-get install -y git unzip libzip-dev \
    && docker-php-ext-install zip pdo pdo_mysql \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Directorio de trabajo
WORKDIR /var/www/html

# Configurar DocumentRoot a public/ y permisos Apache
RUN sed -i 's|DocumentRoot /var/www/html|DocumentRoot /var/www/html/public|g' /etc/apache2/sites-available/000-default.conf \
    && echo "<Directory /var/www/html/public>" > /etc/apache2/conf-available/laravel.conf \
    && echo "    AllowOverride All" >> /etc/apache2/conf-available/laravel.conf \
    && echo "    Require all granted" >> /etc/apache2/conf-available/laravel.conf \
    && echo "</Directory>" >> /etc/apache2/conf-available/laravel.conf \
    && a2enconf laravel

# Copiar entrypoint y dar permisos
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Exponer puerto 80
EXPOSE 80

# CMD final: entrypoint
CMD ["entrypoint.sh"]
