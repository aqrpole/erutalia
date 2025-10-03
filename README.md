# erutalia
student project connecting AWS services

go to the directory /services/server
to build 
docker compose up --build postgres
to run 
docker compose up -d postgres

for building server
go to services/server
docker compose up --build server


# build overall from root dir all services up detached and contianerized
docker compose up --build -d

# run in interactive mode without storing
docker compose up --build

# stops and removes containers + volumes (drops DB!)
docker-compose down -v
