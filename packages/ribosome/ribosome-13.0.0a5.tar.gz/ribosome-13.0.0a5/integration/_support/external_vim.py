from amino import do, Do, List, _, __

from ribosome.config import Config, Data, PluginSettings
from ribosome.nvim.io import NS
from ribosome.trans.api import trans
from ribosome.config.settings import str_setting
from ribosome.request.handler.handler import RequestHandler


default = 'default'
done = 'done'


@do(NS[Data, None])
def wait1() -> NS[Data, None]:
    val = yield NS.inspect(_.settings.var.value_or_default)
    yield NS.pure(None) if val == done else wait1()


@trans.free.unit(trans.st)
def wait() -> Do:
    return wait1()


@trans.free.result(trans.st)
@do(NS[Data, None])
def check() -> Do:
    yield NS.inspect(__.settings.var.update(done))
    yield NS.pure(1)


class Se(PluginSettings):

    def __init__(self) -> None:
        super().__init__('ev')
        self.var = str_setting('var', 'var', default, True)


config = Config.cons(
    'ev',
    settings=Se(),
    request_handlers=List(
        RequestHandler.trans_function(wait)(sync=False),
        RequestHandler.trans_function(check)(sync=True),
    )
)

__all__ = ('config',)
