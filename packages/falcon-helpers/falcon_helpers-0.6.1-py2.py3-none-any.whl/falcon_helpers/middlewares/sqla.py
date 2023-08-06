from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from falcon_helpers.sqla.db import session


class SQLAlchemySessionMiddleware:
    def __init__(self, session):
        self.session = session

    def process_resource(self, req, resp, resource, params):
        resource.session = self.session()

    def process_response(self, req, resp, resource, req_succeeded):
        if not hasattr(resource, 'session'):
            return

        if not req_succeeded:
            resource.session.rollback()
        else:
            resource.session.commit()
            resource.session.close()
