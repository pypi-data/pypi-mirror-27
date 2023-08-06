from zope import interface
from zope.component.factory import Factory

import sqlalchemy
from . import ISAEngine

import logging
logger = logging.getLogger(__name__)

@interface.implementer(ISAEngine)
class SAEngineFromConfig(object):
    def __new__(cls, SQLAlchemyEngine):
        """Return a ISAEngine provider
        
        Kwargs:
            see SQLAlchemyEngine def in configure.yaml
        """
        logger.info("creating new sqlalchemy engine for dsn {} with kwargs {}".format(SQLAlchemyEngine['dsn'], SQLAlchemyEngine.get('kwargs', {})))
        return sqlalchemy.create_engine(SQLAlchemyEngine['dsn'], **SQLAlchemyEngine.get('kwargs', {}))
SAEngineFromConfigFactory = Factory(SAEngineFromConfig)