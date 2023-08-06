from kallikrein import Expectation, kf

from ribosome.plugin import PluginSettings
from ribosome.test.integration.klk import AutoPluginIntegrationKlkSpec, later

from integration._support.execute import EsData


class ExecuteSpec(AutoPluginIntegrationKlkSpec[PluginSettings, EsData]):
    '''
    execute multiple async requests in order $async_request
    sync function call $sync_function
    '''

    @property
    def plugin_prefix(self) -> str:
        return 'Es'

    def module(self) -> str:
        return 'integration._support.execute'

    def async_request(self) -> Expectation:
        self.vim.cmd_once_defined('EsInc')
        # self.vim.cmd('EsInc')
        # self.vim.cmd('EsInc')
        return later(kf(lambda: self.state.counter) == 10)

    def sync_function(self) -> Expectation:
        return kf(self.vim.call_once_defined, 'EsRpcHandlers') == 'esfun'

__all__ = ('ExecuteSpec',)
