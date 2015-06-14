# -*- coding: utf-8 -*-
import json
import os
import os.path
import subprocess
import zc.buildout


class Recipe(object):
    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

        if 'packages' not in options:
            raise zc.buildout.UserError('Missing packages option')

        parts_dir = buildout['buildout']['parts-directory']
        base_dir = os.path.join(parts_dir, 'bower')
        options.setdefault('base-directory', base_dir)
        options.setdefault('executable', 'bower')
        options.setdefault('downloads', 'downloads')

        # Remove unnecessary whitespace.
        packages = [p.strip() for p in options['packages'].splitlines()
                    if p.strip() != '']
        options['packages'] = ' '.join(packages)

    def install(self):
        return self.update()

    def update(self):
        base_dir = self.options['base-directory']
        download_dir = self.options['downloads']
        bowerrc = os.path.join(base_dir, '.bowerrc')

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        with open(bowerrc, 'w') as f:
            json.dump({'directory': download_dir}, f)

        cmd = '{} install {}'.format(self.options['executable'],
                                     self.options['packages'])
        os.chdir(base_dir)
        subprocess.call(cmd, shell=True)

        return bowerrc, os.path.normpath(os.path.join(base_dir, download_dir))
