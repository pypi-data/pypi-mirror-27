import time

from amino import List, __, do, Do
from amino.dat import Dat

from ribosome.plugin import Config
from ribosome.config import RequestHandler, Data
from ribosome.trans.api import trans
from ribosome.nvim.io import NS
from ribosome import ribo_log


class EsData(Dat['EsData'], Data):

    def __init__(self, config: Config, counter: int=7) -> None:
        super().__init__(config)
        self.counter = counter


@trans.free.unit(trans.st)
@do(NS[EsData, None])
def inc() -> Do:
    s = yield NS.get()
    time.sleep(2)
    yield NS.modify(__.copy(counter=s.counter + 1))


@trans.free.result()
def fun() -> str:
    return 'esfun'


config = Config.cons(
    name='es',
    state_ctor=EsData,
    request_handlers=List(
        RequestHandler.trans_cmd(inc)(),
        RequestHandler.trans_function(fun)(sync=True),
    ),
)

__all__ = ('config',)
