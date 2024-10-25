from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from src.auth.user_auth import VerifiedGame, VerifiedUser, verify_game, verify_user
from src.client.database import DBClient
from src.schema.game import AnswerRequest, UpdateGameRequest
from src.service.game import GameService
from src.utils.client import getDBClient

GAME_PREFIX = "/game"
game_router = APIRouter(prefix=GAME_PREFIX)

GET_GAME = "/{game_id}/get-game/"
START_GAME = "/start-game/"
GET_GAMES = "/get-games/"
CLOSE_GAME = "/{game_id}/close-game/"
UPDATE_GAME = "/{game_id}/update-game/"
CURRENT_QUESTION = "/{game_id}/current-question/"
CHECK_ANSWER = "/{game_id}/check-answer/"


@game_router.get(GET_GAME)
async def get_game(
    verified_game: VerifiedGame = Depends(verify_game),
    db_client: DBClient = Depends(getDBClient),
):
    return GameService.getGame(verified_game.requesting_game, db_client)


@game_router.post(START_GAME)
async def start_game(
    verified_user: VerifiedUser = Depends(verify_user),
    db_client: DBClient = Depends(getDBClient),
):
    return GameService.createGame(verified_user.requesting_user, db_client)


@game_router.get(GET_GAMES)
async def get_games(
    verified_user: VerifiedUser = Depends(verify_user),
    db_client: DBClient = Depends(getDBClient),
):
    return GameService.getGames(verified_user.requesting_user, db_client)


@game_router.delete(CLOSE_GAME)
async def close_game(
    verified_game: VerifiedGame = Depends(verify_game),
    db_client: DBClient = Depends(getDBClient),
):
    GameService.closeGame(verified_game.requesting_game, db_client)
    return Response(status_code=status.HTTP_200_OK)


@game_router.post(UPDATE_GAME)
async def update_game(
    request: UpdateGameRequest,
    verified_game: VerifiedGame = Depends(verify_game),
    db_client: DBClient = Depends(getDBClient),
):
    return GameService.updateGame(verified_game.requesting_game, db_client, request)


@game_router.get(CURRENT_QUESTION)
async def current_question(
    verified_game: VerifiedGame = Depends(verify_game),
    db_client: DBClient = Depends(getDBClient),
):
    return GameService.getQuestion(verified_game.requesting_game, db_client)


@game_router.post(CHECK_ANSWER)
async def check_answer(
    request: AnswerRequest,
    verified_game: VerifiedGame = Depends(verify_game),
    db_client: DBClient = Depends(getDBClient),
):
    return GameService.checkAnswer(verified_game.requesting_game, db_client, request)
