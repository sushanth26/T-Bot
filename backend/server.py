"""Main FastAPI application - Simplified and modular"""
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router, prefetch_popular_stocks, background_refresh_popular

# Initialize FastAPI app
app = FastAPI(title="Stock Data API", version="2.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.on_event("startup")
async def startup():
    """Startup tasks: Pre-fetch popular stocks and start background refresh"""
    # Pre-fetch all popular stocks for instant switching
    await prefetch_popular_stocks()
    
    # Start background refresh
    asyncio.create_task(background_refresh_popular())
    
    print("🚀 Stock Data API ready!")


if __name__ == "__main__":
    print("🚀 Starting Stock Data API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")

