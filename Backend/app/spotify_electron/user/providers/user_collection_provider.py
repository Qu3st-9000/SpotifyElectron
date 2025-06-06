"""User collections provider"""

from motor.motor_asyncio import AsyncIOMotorCollection

import app.spotify_electron.user.base_user_service as base_user_service
from app.database.database_schema import DatabaseCollection
from app.database.DatabaseConnectionManager import DatabaseConnectionManager
from app.logging.logging_constants import LOGGING_USER_COLLECTION_PROVIDER
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.user.artist.artist_schema import ArtistDocument
from app.spotify_electron.user.base_user_schema import BaseUserDocument
from app.spotify_electron.user.user.user_schema import UserDocument, UserType

users_collection_provider_logger = SpotifyElectronLogger(
    LOGGING_USER_COLLECTION_PROVIDER
).get_logger()


async def get_user_associated_collection(
    user_name: str,
) -> AsyncIOMotorCollection[BaseUserDocument]:
    """Returns the user collection according to the user role

    Returns:
        the user collection
    """
    collection_map: dict[UserType, AsyncIOMotorCollection] = {
        UserType.USER: DatabaseConnectionManager.get_collection_connection(
            DatabaseCollection.USER
        ),
        UserType.ARTIST: DatabaseConnectionManager.get_collection_connection(
            DatabaseCollection.ARTIST
        ),
    }

    user_type = await base_user_service.get_user_type(user_name)
    if user_type not in collection_map:
        users_collection_provider_logger.warning(
            f"User {user_name} doesn't have a valid user type "
            f"using {UserType.USER} type instead"
        )
        return collection_map[UserType.USER]
    return collection_map[user_type]


def get_artist_collection() -> AsyncIOMotorCollection[ArtistDocument]:
    """Get artist collection

    Returns:
        the artist collection
    """
    return DatabaseConnectionManager.get_collection_connection(DatabaseCollection.ARTIST)


def get_user_collection() -> AsyncIOMotorCollection[UserDocument]:
    """Get user collection

    Returns:
        the user collection
    """
    return DatabaseConnectionManager.get_collection_connection(DatabaseCollection.USER)


def get_all_collections() -> list[AsyncIOMotorCollection]:
    """Get all user collections

    Returns:
        all the users collections
    """
    collection_map = {
        UserType.USER: DatabaseConnectionManager.get_collection_connection(
            DatabaseCollection.USER
        ),
        UserType.ARTIST: DatabaseConnectionManager.get_collection_connection(
            DatabaseCollection.ARTIST
        ),
    }
    return list(collection_map.values())
