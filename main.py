from fastapi import FastAPI

from database import Base, engine

# Create the SQLite database tables on startup
Base.metadata.create_all(bind=engine)


app = FastAPI(title="MyTowerOfHanoi")


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"status": "ok", "message": "MyTowerOfHanoi API is open"}
