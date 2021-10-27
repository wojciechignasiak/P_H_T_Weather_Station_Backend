import uvicorn
from fastapi import FastAPI, Path

app = FastAPI()

inventory = {1: {"name": "Milk", "price": 3.99, "brand": "Regular"}}


@app.get("/db-models/{item_id}")
def get_item(item_id: int = Path(
    None, description="The id of item you would like to view")):
    return inventory[item_id]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
