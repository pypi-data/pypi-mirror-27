import os
import pymongo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SQLAlchemyConnection(object):
    """
        Provide access to PostgreSQL database created via SQLAlchemy
    """
    _config = None
    _engine = None
    _session = None

    def __init__(self, config):
        self._config = config
        if self._engine is None:
            self._engine = create_engine("{0}://{1}:{2}@{3}:{4}/{5}".format(
                self._config.get("GREASE_DB_ENGINE", "postgresql"),
                self._config.get("GREASE_DB_USER", "dev"),
                self._config.get("GREASE_DB_PASSWORD", "dev"),
                self._config.get("GREASE_DB_HOST", "localhost"),
                self._config.get("GREASE_DB_PORT", "5432"),
                self._config.get("GREASE_DB_DB", "")
            ))

    def get_engine(self):
        return self._engine

    def get_session(self):
        if not self._session:
            session = sessionmaker(bind=self.get_engine())
            self._session = session()
        return self._session


class MongoConnection(object):
    def __init__(self):
        if not os.getenv('GREASE_MONGO_USER') and not os.getenv('GREASE_MONGO_PASSWORD'):
            self._client = pymongo.MongoClient(
                host=os.getenv('GREASE_MONGO_HOST', 'localhost'),
                port=int(os.getenv('GREASE_MONGO_PORT', 27017))
            )
        else:
            self._client = pymongo.MongoClient(
                "mongodb://{0}:{1}@{2}:{3}/{4}".format(
                    os.getenv('GREASE_MONGO_USER', ''),
                    os.getenv('GREASE_MONGO_PASSWORD', ''),
                    os.getenv('GREASE_MONGO_HOST', 'localhost'),
                    os.getenv('GREASE_MONGO_PORT', 27017),
                    os.getenv('GREASE_MONGO_DB', 'grease')
                )
            )

    def client(self):
        # type: () -> pymongo.MongoClient
        return self._client
