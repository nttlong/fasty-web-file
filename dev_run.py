# from webapp.application import app
import uvicorn
import application
if __name__ == "__main__":
    uvicorn.run(
        f"{application.__name__}:app",
        host='172.16.7.25',
        port=8012,
        workers=2,
        debug=True,
        reload=True,

    )