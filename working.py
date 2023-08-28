from fastapi import FastAPI, Query, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price : float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str]
    price : Optional[float]
    brand: Optional[str] = None

inventory = {}


@app.get("/")
def home():
    return {"data":"test"}

@app.get("/about")
def about():
    return {"data":"about test"}


@app.get("/get_item_info/{item_id}")
def get_item_info(item_id: int =  Path(..., description="the id of inventory", gt=-1)):
    return inventory[item_id]

# path parameter = parameters in path ; query parameter = parameter not in path
#http://127.0.0.1:8000/get_item/1?price=80
@app.get("/get_item/{item_id}")
def get_item(item_id: int =  Path(..., description="the id of inventory", gt=-1), price: Optional[int] = Query(..., gt=-1)):
    print(price)
    return inventory[item_id]

# http://127.0.0.1:8000/get_by_name?name=milk&test=2
@app.get("/get_by_name")
def get_item_name(*, name: Optional[str] = None, test:int):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
        return {"data": "inventory not found"}

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"error: item already exists"}
    inventory[item_id] = item
    return inventory[item_id]

@app.put("/update_item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return {"error: item doesnt exist"}

    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand
    return inventory[item_id]

@app.delete("/delete_item")
def update_item(*,item_id: int = Query(..., description="the id of the item to delete", gt=0), item: UpdateItem):
    if item_id not in inventory:
        return {"error: item doesnt exist"}

    del inventory[item_id]
    return {"message": "item deleted"}