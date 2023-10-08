## UseCase

import inject

from ..services.uow import UnitOfWork


class BaseService:
    @inject.autoparams()
    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.uow = uow