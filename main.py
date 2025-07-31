

#Q1
import base64
from pdb import post_mortem
from typing import List
from fastapi import Body, FastAPI, Header
app = FastAPI()

@app.get("/ping")
async def ping():
    return "pong"   


#Q2
from fastapi.responses import HTMLResponse, PlainTextResponse
@app.get("/home", response_class=HTMLResponse)
async def home():
    return "<h1>Welcome home!</h1>"


#Q3


from fastapi.responses import HTMLResponse
from fastapi import Request, HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return HTMLResponse(content="<h1>404 NOT FOUND</h1>", status_code=404)
    return await request.app.default_exception_handler(request, exc)

#Q4


    
from flask import Flask, request, jsonify
from datetime import datetime
from http import HTTPStatus

app = Flask(__name__)


posts_storage = []

@app.route('/posts', methods=['POST'])
def create_posts():
    try:
       
        new_posts = request.get_json()
        
       
        if not isinstance(new_posts, list):
            return jsonify({"error": "Le corps de la requête doit être une liste de posts"}), HTTPStatus.BAD_REQUEST
            
        for post in new_posts:
           
            required_fields = ['author', 'title', 'content', 'creation_datetime']
            if not all(field in post for field in required_fields):
                return jsonify({"error": f"Un post ne contient pas tous les champs requis: {required_fields}"}), HTTPStatus.BAD_REQUEST
                
            try:
                datetime.fromisoformat(post['creation_datetime'])
            except ValueError:
                return jsonify({"error": "Le format de date doit être ISO format (YYYY-MM-DDTHH:MM:SS)"}), HTTPStatus.BAD_REQUEST
        
       
        posts_storage.extend(new_posts)
        
       
        return jsonify(posts_storage), HTTPStatus.CREATED
        
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == '__main__':
    app.run(debug=True)




#Q5  

posts = []
@app.post("/posts", status_code=201)
async def create_posts(posts_list: List[post_mortem] = Body(...)):
    global posts
    posts.extend(posts_list)
    return posts



#Q6 .

@app.put("/posts", status_code=200)
async def update_posts(posts_list: List[Post] = Body(...)):
    global posts
    for new_post in posts_list:
        for i, existing_post in enumerate(posts):
            if existing_post.title == new_post.title:
                posts[i] = new_post
                break
        else:
            posts.append(new_post)
    return posts




#BONUS

from flask import Flask, request, jsonify, make_response 
from http import HTTPStatus
import base64

app = Flask(__name__)


VALID_USERNAME = "admin"
VALID_PASSWORD = "123456"

@app.route('/ping/auth', methods=['GET'])
def ping_auth():
    
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Basic '):
      
        return make_response(
            jsonify({"error": "Authentification requise"}),
            HTTPStatus.UNAUTHORIZED,
            {'WWW-Authenticate': 'Basic realm="Authentication Required"'}
        )
    
    try:
        
        encoded_credentials = auth_header.split(' ')[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':', 1)
        
        
        
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            return "pong", HTTPStatus.OK
        else:
            return make_response(
                jsonify({"error": "Identifiants incorrects"}),
                HTTPStatus.FORBIDDEN
            )
            
    except Exception as e:
       
        return make_response(
            jsonify({"error": "Authentification invalide"}),
            HTTPStatus.BAD_REQUEST
        )

if __name__ == '__main__':
    app.run(debug=True)
