import os
from flask import Flask, request
from sqlalchemy import create_engine
from utils.create_tables import create_tables

DB_URI = os.environ['DATABASE_URL'].replace("postgresql://", "cockroachdb://")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8001))
    try:
        engine = create_engine(DB_URI, connect_args={"application_name":"gbfs_api"})
        create_tables(engine)
    except Exception as e:
        print("Failed to connect to database.")
        print(f"{e}")
        raise e


    app.run(debug=True, host='0.0.0.0', port=port)