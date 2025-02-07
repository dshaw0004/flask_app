import hashlib
import datetime
import json
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, storage
from google.cloud.firestore import CollectionReference, DocumentReference, FieldFilter, Query

# with open('./newkey.json', 'r') as file:
#     creds = json.load(file)
#     print(creds)
creds_json = json.loads(os.environ['FIREBASE_CREDS_JSON'])
cred = credentials.Certificate(creds_json)
# cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), 'newkey.json'))
firebase_admin.initialize_app(cred, {'storageBucket': 'pussypics.appspot.com'})

db = firestore.client()
bucket = storage.bucket()


def add_user(username: str, password: str) -> dict[str, str]:
    '''
    If username already exists then it will return a dictionary with success = False and a message
    If username is new then it will return a dictionary with success = True and id
    '''

    # is_unique_name = check_unique_username(username=username)
    # if not is_unique_name:
    #     return {
    #             'success': False,
    #             'message': 'username already exists'
    #             }
    doc_ref = db.collection('users').document()
    doc_ref.set({
        'username': username,
        'password': password,
        })

    return {
            'id': doc_ref.id
            }

def get_user_id(username: str, password: str) -> tuple[int, str]:
    user_ref = db.collection('users')
    query_ref = user_ref.where(filter=FieldFilter('username', '==', username)).where(filter=FieldFilter('password', '==', password))

    query_ref_list = list(query_ref.stream())

    if not query_ref_list:
        return 404, 'user not found'
    id: str =  query_ref_list[0].id
    return 200, id

def check_unique_username(username: str) -> bool:
    user_ref = db.collection('users')
    query_ref = user_ref.where(filter=FieldFilter('username', '==', username))
    query_ref_list = list(query_ref.stream())
    
    return not len(query_ref_list)

def upload_image(filename:str):
    file_blob = bucket.blob('key.json')
    file_blob.upload_from_filename('key.json')
    
    file_blob.make_public()
    print(file_blob.public_url)
    print(file_blob.id)
    file_blob.delete()

def upload_image_from_byte(filename: str, file_obj) -> dict:
    '''
    This is how to use it.
    with open('path/to/file', 'rb') as file:
        data = upload_image_from_byte(filename='filename', file_obj=file)
    '''
    file_blob = bucket.blob(filename)
    file_blob.upload_from_file(file_obj=file_obj)
    file_blob.make_public()
    return {
            'id': file_blob.id,
            'url': file_blob.public_url
            }

def delete_file(filename: str):
    blob = bucket.get_blob(filename)
    if blob:
        blob.delete()

def check_unique_file(file_hash: str) -> bool:
    post_ref = db.collection('posts')
    query_ref: Query = post_ref.where(filter=FieldFilter('fileHash', '==', file_hash))
    query_ref_list = list(query_ref.stream())
    return not len(query_ref_list)

def add_new_post_record(username: str, user_id: str, filename: str, file_binary) -> tuple[int, str] :
    hash: str = hashlib.md5(file_binary.read()).hexdigest()
    is_unique_file: bool = check_unique_file(file_hash=hash)
    if not is_unique_file:
        return 400, 'this file already exists'
    file_binary.seek(0)
    res: dict[str, str] = upload_image_from_byte(filename=filename, file_obj=file_binary)
    file_url: str|None = res.get('url')
    file_id: str = res.get('id', '')

    if not file_url:
        return 400, 'unable to upload the image now'

    post_ref: CollectionReference = db.collection('posts')
    post_ref_document: DocumentReference = post_ref.document()
    post_entry: dict[str, str] = {
            'username': username,
            'userId': user_id,
            'fileHash': hash,
            'url': file_url,
            'fileID': file_id,
            'uploadedOn': datetime.datetime.now(datetime.UTC).timestamp()
            }
    post_ref_document.set(post_entry)

    return 200, 'image uploaded successfully'

def get_all_posts_record():
    posts_ref = db.collection("posts")
    docs = posts_ref.stream()

    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")

def get_n_posts_record(n: int):
    posts_ref = db.collection("posts")
    query = posts_ref.order_by("uploadedOn", direction=firestore.Query.DESCENDING).limit(n)
    results = query.stream()
    results = [ res.to_dict() for res in results ]
    if not len(results):
        return []
    def post_processing(x: dict) -> dict:
        del x['userId']
        del x['fileID']
        x['uploadedOn'] = datetime.datetime.utcfromtimestamp(x['uploadedOn']).strftime("%b %d, %Y")
        return x
    results = map(post_processing, results)
    return list(results)


