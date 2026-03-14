#!/bin/bash
set -e

echo "Entrypoint iniciado"

echo "🔧 Ajustando permisos..."
chown -R www-data:www-data /var/www/html
chmod -R 775 /var/www/html

# 2️⃣ Instalar dependencias si no existen
if [ ! -d "/var/www/html/vendor" ] || [ ! -f "/var/www/html/vendor/autoload.php" ]; then
    echo "📦 Instalando dependencias Composer..."
    composer install --no-interaction --prefer-dist --optimize-autoloader
fi

echo "⏳ Esperando a MySQL..."
until mysqladmin ping -h "$DB_HOST" -P "$DB_PORT" --silent; do
  sleep 3
done
echo "✅ MySQL disponible"

# Generar APP_KEY solo si no existe
if [ -z "$APP_KEY" ]; then
  echo "🔑 Generando APP_KEY..."
  php /var/www/html/artisan key:generate --force
fi

echo "🗄️ Ejecutando migraciones..."
php /var/www/html/artisan migrate --force

echo "🚀 Arrancando Apache..."
exec apache2-foreground
