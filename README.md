# GBFS Feed API
API to ingest and query station data from bike share systems from across the world.
## Run the Project
Before starting doing the steps below, make sure you are running docker on your machine.


1. Clone the project

```bash
git clone git@github.com:dewynl/gbfs_feeds_api.git
```

2. Go to the project directory

```bash
cd gbfs_feeds_api
```

3. Run the docker compose
```bash
docker-compose up
```

Now the database should be up and running and you should be able to access the API in http://127.0.0.1:8001. On the first run, the API will create the tables we will use and its gonna be empty. Before being able to query for any data make sure to ingest it by posting it to http://127.0.0.1:8001/ingest using the format used [here](https://gbfs.bcycle.com/bcycle_madison/gbfs.json) as a JSON.

To access the Database Console, you can access http://127.0.0.1:8080 in your browser.


## Tech Stack

CockroachDB, Flask, Python, Docker, SQLAlchemy
