import uvicorn
from app import app  # This imports the app from app/__init__.py

if __name__ == "__main__":
    # Start the server using the modular app instance
    uvicorn.run(app, host="127.0.0.1", port=8000)