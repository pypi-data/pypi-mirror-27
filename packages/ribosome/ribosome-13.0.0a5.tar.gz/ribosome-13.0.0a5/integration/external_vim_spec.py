from neovim.api import Nvim

from kallikrein import k, Expectation

from ribosome.test.integration.klk import AutoPluginIntegrationKlkSpec
from ribosome.nvim.components import ExternalNvimFacade
from ribosome.nvim import NvimFacade


class ExternalVimSpec(AutoPluginIntegrationKlkSpec):
    '''
    test $test
    '''

    def _nvim_facade(self, vim: Nvim) -> NvimFacade:
        return ExternalNvimFacade(vim, self._prefix)

    def module(self) -> str:
        return 'integration._support.external_vim'

    @property
    def plugin_prefix(self) -> str:
        return 'ev'

    def test(self) -> Expectation:
        self.vim.call_once_defined('EvWait')
        self.vim.call('EvCheck')
        return k(1) == 1

__all__ = ('ExternalVimSpec',)
