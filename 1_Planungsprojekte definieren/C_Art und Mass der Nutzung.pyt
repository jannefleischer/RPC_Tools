# -*- coding: utf-8 -*-

import _rpcpath

from rpctools.utils.encoding import encode
from rpctools.definitions.nutzungsart.tbx_flaechenbilanz import TbxFlaechenbilanz
from rpctools.definitions.nutzungsart.tbx_nutzungen import TbxNutzungen


class Toolbox(object):
    def __init__(self):
        self.label = encode(u'Art und Maß der Nutzung')
        self.alias = ''
        self.tools = [TbxFlaechenbilanz, TbxNutzungen]


def main():
    tbx = Toolbox()
    tool = Flaechenbilanz()
    tool.execute(tool.getParameterInfo(), None)
    tool = Nutzungen()
    tool.execute(tool.getParameterInfo(), None)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action="store_true")
    options = parser.parse_args()
    if options.debug:
        main()