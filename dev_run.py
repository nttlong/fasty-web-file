# from webapp.application import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "webapp.application:app",
        host='172.16.13.72',
        port=8012,
        workers=2,
        debug=True,
        reload=True,

    )