from fastapi import FastAPI

app = FastAPI(title="MyTowerOfHanoi")


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"status": "ok", "message": "MyTowerOfHanoi API is open"}
