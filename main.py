from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import api  # Import your router

app = FastAPI(title="Voice Chatbot API", version="1.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api.router, prefix="/api", tags=["Voice API"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Voice Chatbot API!"}

# Run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
