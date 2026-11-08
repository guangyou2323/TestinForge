from fastapi import FastAPI

app = FastAPI()

# Your API endpoint
@app.get("/api/hello")
def get_hello():
    return {"status": "success", "message": "Hello from your backend API!"}
