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

note-for future use, use SQLalchemy2.X, in the requirments file for ingenstion 

#to run the ingestion process go to the folder services/extractor
python3.12 -m app.main process

# Process specific folder (override config)
python -m app.main process --input-dir /path/to/your/documents

# Process single file
python -m app.main process-file /path/to/specific/document.pdf

# Check for errors
python -m app.main show-errors

# Health check
python -m app.main health

# requirments initaial phase 
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

Found 298 supported files
Supported formats: ['.pptx', '.pdf', '.png', '.docx', '.jpg', '.txt', '.jpeg']