from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from model import Item


Base.metadata.create_all(bind=engine)
app = FastAPI()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def read_root():
    return {"Name" : "Danish"}


@app.post('/items')
def create_items(item: dict, db: Session = Depends(get_db)):
    db_item = Item(name=item['name'], description=item['description'])
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Item created", "item": db_item}


@app.get('/items/{item_id}')
def read_items(item_id : int, db : Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_item


@app.get('/items/')
def read_items(db:Session = Depends(get_db)):
    db_items = db.query(Item).all()
    return db_items



@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict, db: Session = Depends(get_db)):
    db_item = db.query(Item.Item).filter(Item.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.name = item['name']
    db_item.description = item['description']
    db.commit()
    db.refresh(db_item)
    return {"message": f"Item {item_id} updated", "item": db_item}


# Delete an item by ID
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": f"Item {item_id} deleted"}