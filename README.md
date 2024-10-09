Instructions
1. Place all the files (Dockerfile, docker-compose.yml, requirements.txt, and ingest_data.py) in the same directory.
2. Place your prayer-times.csv file in the same directory.
3. Build and run the Docker container using docker-compose: 

docker-compose up --build

Whenever the prayer-times.csv file changes, you don’t need to rebuild the Docker image. Just modify the file on your host machine, and the container will access the updated file immediately.

docker-compose up


Change Logs

VERSION     DATE            AUTHOR          DETAILS
1.0         2024-10-09      Hasan Ahmed     Initial Creation