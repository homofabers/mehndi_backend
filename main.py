from typing import Optional

from fastapi import FastAPI, UploadFile , File
from fastapi.responses import FileResponse
import json
import os

app = FastAPI()
app.debug = True

@app.get("/")
async def root():
    return {"message": "Server Running"}

#--------------------------------get image_id and category then return the image-------------------
@app.get("/image/{category}/{image_id}")
async def get_image(category: str, image_id: str):
    #images/{category}/{image_id}
    image_path = os.path.join("images", category, image_id+".jpg")
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        return {"message": "Image not found"}

#--------------------------------get list of all categories-------------------
@app.get("/categories")
def get_categories():
    return json.loads(open('categories.json').read())

#--------------------------------add a new category name-------------------
@app.post("/add/category")
def add_category(name: str):
    #create file with image_id and add json
    id = len(json.loads(open('categories.json').read())) + 1
    print("id is " , id)

    os.makedirs(f'images/{id}', exist_ok=True)

    # add category to categories.json
    with open('categories.json', 'r') as f:
        data = json.load(f)
    data[id] = {'name': name , 'no_of_images': 0}
    f = open('categories.json', 'w')
    f.write(json.dumps(data))
    f.close()

    return {"message": "Category added"}


#--------------------------------add a new image to a category-------------------
@app.post("/add/image/{category}")
def add_image(category: str, image: UploadFile = File(...)):
    #create file with image_id and add json
    image_id = int(json.loads(open('categories.json').read())[(category)]['no_of_images']) + 1
    print("image_id is " , image_id)

    # add image to images/{category}/{image_id}
    image_path = os.path.join("images", category, str(image_id)+".jpg")
    with open(image_path, "wb") as f:
        f.write(image.file.read())
    
    # add image to categories.json
    with open('categories.json', 'r') as f:
        data = json.load(f)
    data[str(category)]['no_of_images'] = image_id
    f = open('categories.json', 'w')
    f.write(json.dumps(data))
    f.close()

    return {"message": "Image added"}
