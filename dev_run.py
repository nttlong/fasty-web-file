# from webapp.application import app
import uvicorn
import application
import application
if __name__ == "__main__":
    uvicorn.run(
        f"{application.__name__}:app",
        host=application.bind_ip,
        port=application.bind_port,
        # workers=2,
        debug=True,
        reload=True,

    )