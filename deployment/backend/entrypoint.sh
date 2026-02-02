#!/bin/bash
set -e

# 1. Dar permisos
chown -R www-data:www-data /var/www/html
chmod -R 775 /var/www/html

# 2. Generar APP_KEY si no existe
if ! grep -q 'APP_KEY=' /var/www/html/.env; then
    php /var/www/html/artisan key:generate
fi

# 3. Ejecutar migraciones (solo pendientes)
php /var/www/html/artisan migrate --force

# 4. Arrancar Apache en primer plano
apache2-foreground
