import os
from datetime import datetime

import uvicorn
import pyrebase
import json
from fastapi import FastAPI
from models import LoginSchema, SignUpSchema #UserProfileSchema
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi import Form, File, UploadFile
from google.cloud import storage, secretmanager

def access_secret_version(project_id, secret_id, version_id):
    client = secretmanager.SecretManagerServiceClient()

    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")

    return json.loads(payload)

app: FastAPI = FastAPI(
    description="User Auth & User Profile",
    title="Firebase Auth"
)
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore

if not firebase_admin._apps:
    firebaseSak = access_secret_version('capstone-scancare-406911', 'firebase_sak','1')
    cred = credentials.Certificate(firebaseSak)
    firebase_admin.initialize_app(cred)

firebaseConfig = access_secret_version('capstone-scancare-406911', 'firebase_config','1')

firebase = pyrebase.initialize_app(firebaseConfig)
db = firestore.client()


key = access_secret_version('capstone-scancare-406911', 'scancare-user-profile_bucket_sak','1')


storage_client = storage.Client.from_service_account_info(key)
# firebase = firebase.FirebaseApplication("https://scancare-capstone.firebaseio.com", None)


import logging
from datetime import datetime


@app.post('/signup')
async def create_an_account(user_data: SignUpSchema):
    email = user_data.email
    password = user_data.password
    username = user_data.username
    address = user_data.address

    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        today = datetime.now()
        db.collection('userProfile').document(user.uid).set(
            {
                "user_id": user.uid,
                "email": email,
                'creationDate': today,
                "username": username,
                "address": address,
                "photo": "null"
            }
        )
        return JSONResponse(content={"user_id": user.uid,
                                     "message": f"Akun berhasil dibuat {user.uid}"}, status_code=201)
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail=f"Email {email} telah digunakan")
    except Exception as e:
        logging.error(f"Error creating account for email {email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post('/login')
async def create_access_token(user_data: LoginSchema):
    email = user_data.email
    password = user_data.password

    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email=email,
            password=password
        )

        token = user['idToken']
        user_id = user['localId']
        return JSONResponse(
            content={
                "token": token,
                "user_id": user_id
            }, status_code=200
        )
    except:
        raise HTTPException(
            status_code=400, detail="invalid"
        )


@app.post('/ping')
async def validate_token(request: Request):
    headers = request.headers
    jwt = headers.get('authorization')

    user = auth.verify_id_token(jwt)

    return user


@app.get('/userProfile/{user_id}')
async def get_user_profile(user_id: str):
    try:
        user_doc_ref = db.collection('userProfile').document(user_id)
        user_profile = user_doc_ref.get()

        if user_profile.exists:
            return user_profile.to_dict()
        else:
            raise HTTPException(
                status_code=404,
                detail="Profil User tidak ditemukan"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gagal menampilkan profil user : {str(e)}"
        )


@app.put('/userProfile/{user_id}')
async def update_user_profile(
        user_id: str,
        username: str = Form(None),
        address: str = Form(None),
        file: UploadFile = File(None)
):
    try:
        user_doc_ref = db.collection('userProfile').document(user_id)
        user_profile = user_doc_ref.get()

        if user_profile.exists:
            updated_profile = {}

            if username is not None:
                updated_profile['username'] = username

            if address is not None:
                updated_profile['address'] = address

            if file:
                # Upload foto ke Google Cloud Storage
                bucket_name = 'scancare_user_profile'
                # Menggunakan storage_client dari baris 47
                bucket = storage_client.get_bucket(bucket_name)
                file_path = f"{file.filename}"
                blob = bucket.blob(file_path)
                blob.upload_from_file(file.file, content_type='image/jpeg')

                # Dapatkan URL foto dari Google Cloud Storage
                photo_url = f'https://storage.googleapis.com/{bucket_name}/{file_path}'
                updated_profile['photo'] = photo_url  # Tambahkan URL foto ke profil pengguna

            # Update data profil pengguna di Firestore jika ada yang diubah
            if updated_profile:
                user_doc_ref.update(updated_profile)

            return JSONResponse(
                content={"message": "Profil pengguna berhasil diperbarui"},
                status_code=200
            )
        else:
            raise HTTPException(
                status_code=404,
                detail="Profil pengguna tidak ditemukan"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Terjadi kesalahan: {str(e)}"
        )

def upload_file(file):
    try:
        bucket_name = 'scancare_user_profile'
        # Menggunakan storage_client dari baris 47
        bucket = storage_client.get_bucket(bucket_name)
        file_path = f"{file.filename}"
        blob = bucket.blob(file_path)
        blob.upload_from_file(file.file, content_type='image/jpeg')
        haha = f'https://storage.googleapis.com/{bucket_name}/{file_path}'
        return haha
    except Exception as e:
        return f"Error: {str(e)}"


#buat test upload GCS
@app.post('/upload')
async def upload_image(photo: UploadFile = File(...)):
    file_path = upload_file(photo)
    return {"file_path": file_path}


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    print(f"Listening to http://0.0.0.0:{port}")
    uvicorn.run(app, host='0.0.0.0', port=port)
