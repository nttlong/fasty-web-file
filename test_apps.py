from fastapi import FastAPI

app = FastAPI()

import pymongo
@app.get("/")
async def root():
    cnn= pymongo.mongo_client.MongoClient(
        host= 'localhost',
        port = 27017,
        username= 'root',
        password= '123456',
        authSource='admin',
        authMechanism= 'SCRAM-SHA-1'
    )
    try:
        version= cnn.server_info()["version"]
        return {"message": f"db connect ok version {version}"}
    except Exception as e:
        return {"message": f"error {version}"}
#uvicorn test_apps:app --reload