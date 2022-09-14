## run database

docker run --name "postgresql1" -e POSTGRES_PASSWORD="password" -e POSTGRES_USER="user" -e POSTGRES_DB="mydata" -p 5432:5432 -d postgres:13.0-alpine
