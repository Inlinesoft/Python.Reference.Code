import abc
from typing import cast

import inject

from .. import repositories


class UnitOfWork(metaclass=abc.ABCMeta):
  
    configs_repo = cast(
        repositories.ConfigsRepository,
        inject.attr(repositories.ConfigsRepository),
    )
  
    @property
    def repos(self):
        res = [getattr(self, x) for x in dir(self) if x.endswith("repo")]
        return res

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

