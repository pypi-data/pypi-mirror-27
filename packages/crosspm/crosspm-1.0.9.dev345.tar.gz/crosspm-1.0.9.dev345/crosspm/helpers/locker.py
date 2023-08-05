# -*- coding: utf-8 -*-
import os
from collections import OrderedDict

from crosspm.helpers.config import CROSSPM_DEPENDENCY_FILENAME
from crosspm.helpers.downloader import Downloader
from crosspm.helpers.exceptions import CrosspmException, CROSSPM_ERRORCODE_PACKAGE_NOT_FOUND
from crosspm.helpers.output import Output


class Locker(Downloader):
    def __init__(self, config, packages=None):
        # TODO: revise logic to allow recursive search without downloading
        super(Locker, self).__init__(config, do_load=False or config.recursive)
        self._packages = packages if packages else None

        if not getattr(config, 'deps_path', ''):
            config.deps_path = config.deps_file_name or CROSSPM_DEPENDENCY_FILENAME
        deps_path = config.deps_path.strip().strip('"').strip("'")
        self._deps_path = os.path.realpath(os.path.expanduser(deps_path))

    # Download packages or just unpack already loaded (it's up to adapter to decide)
    def lock_packages(self, deps_file_path=None, depslock_file_path=None):
        if deps_file_path is None:
            deps_file_path = self._deps_path
        if depslock_file_path is None:
            depslock_file_path = self._depslock_path
        if deps_file_path == depslock_file_path:
            depslock_file_path += '.lock'
            # raise CrosspmException(
            #     CROSSPM_ERRORCODE_WRONG_ARGS,
            #     'Dependencies and Lock files are same: "{}".'.format(deps_file_path),
            # )

        if not self._packages:
            self._log.info('Check dependencies ...')
            self._root_package.find_dependencies(deps_file_path)

            self._log.info('')
            self._log.info('Dependency tree:')
            self._root_package.print(0, self._config.output('tree', [{self._config.name_column: 0}]))
            if not self._config.recursive:
                self._packages = self._root_package.packages

        _not_found = self.get_not_found_packages()

        if _not_found:
            raise CrosspmException(
                CROSSPM_ERRORCODE_PACKAGE_NOT_FOUND,
                'Some package(s) not found: {}'.format(', '.join(_not_found))
            )

        self._log.info('Writing lock file [{}]'.format(depslock_file_path))
        text = ''
        packages = OrderedDict()
        columns = self._config.get_columns()
        widths = {}
        for _pkg in self.get_raw_packages():
            _pkg_name = _pkg.package_name
            _params = _pkg.get_params(columns, merged=True, raw=False)
            if _pkg_name not in packages:
                packages[_pkg_name] = _params
                comment = 1
                for _col in columns:
                    widths[_col] = max(widths.get(_col, len(_col)), len(str(_params.get(_col, '')))) + comment
                    comment = 0
        comment = 1
        for _col in columns:
            text += '{}{} '.format(_col, ' ' * (widths[_col] - len(_col) - comment))
            comment = 0
        text = '#{}\n'.format(text.strip())
        for _pkg_name in sorted(packages, key=lambda x: str(x).lower()):
            _pkg = packages[_pkg_name]
            line = ''
            for _col in columns:
                line += '{}{} '.format(_pkg[_col], ' ' * (widths[_col] - len(str(_pkg[_col]))))
            text += '{}\n'.format(line.strip())

        # if _pkg.download(self.packed_path):
        #         _pkg.unpack(self.unpacked_path)

        Output().write_to_file(text, depslock_file_path)
        self._log.info('Done!')

        return self._packages
