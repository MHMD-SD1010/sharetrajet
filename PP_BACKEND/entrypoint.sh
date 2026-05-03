set -e

echo "Waiting for PostgreSQL..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  sleep 1
done
echo "PostgreSQL started"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating cache table..."
python manage.py createcachetable || true

echo "Starting server..."
exec "$@"