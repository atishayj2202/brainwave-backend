from uuid import UUID

from fastapi import Depends, Header, HTTPException
from pydantic import BaseModel
from starlette import status

from src.auth.base import _get_requesting_user
from src.client.database import DBClient
from src.client.firebase import FirebaseClient
from src.db.game import Game
from src.db.user import User
from src.utils.client import getDBClient, getFirebaseClient


class VerifiedUser(BaseModel):
    requesting_user: User


class VerifiedGame(BaseModel):
    requesting_user: User
    requesting_game: Game


def verify_user(
    authorization: str = Header(...),
    cockroach_client: DBClient = Depends(getDBClient),
    firebase_client: FirebaseClient = Depends(getFirebaseClient),
) -> VerifiedUser:
    user: User = _get_requesting_user(authorization, cockroach_client, firebase_client)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return VerifiedUser(requesting_user=user)


def verify_game(
    game_id: UUID,
    authorization: str = Header(...),
    cockroach_client: DBClient = Depends(getDBClient),
    firebase_client: FirebaseClient = Depends(getFirebaseClient),
) -> VerifiedGame:
    user: User = _get_requesting_user(authorization, cockroach_client, firebase_client)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    game = cockroach_client.query(
        Game.get_id,
        id=game_id,
        error_not_exist=False,
    )
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found",
        )
    if game.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to access this game",
        )
    if game.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game already ended",
        )
    return VerifiedGame(requesting_user=user, requesting_game=game)
