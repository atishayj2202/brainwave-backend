from src.client.database import DBClient
from src.client.firebase import FirebaseClient

cockroachClient = None
firebaseClient = None


def getDBClient() -> DBClient:
    global cockroachClient
    if cockroachClient is None:
        cockroachClient = DBClient()
    return cockroachClient


def getFirebaseClient() -> FirebaseClient:
    global firebaseClient
    if firebaseClient is None:
        firebaseClient = FirebaseClient()
    return firebaseClient
