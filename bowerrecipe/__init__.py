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
        self.base_dir = os.path.join(parts_dir, 'bower')
        options.setdefault('binary', 'bower')
        options.setdefault('downloads', 'downloads')

        # Remove unnecessary whitespace.
        packages = [p.strip() for p in options['packages'].splitlines()
                    if p.strip() != '']
        options['packages'] = ' '.join(packages)

    def install(self):
        conf = os.path.join(self.base_dir, '.bowerrc')
        os.makedirs(self.base_dir)
        with open(conf, 'w') as f:
            json.dump({'directory': self.options['downloads']}, f)
        cmd = '{} install {}'.format(self.options['binary'],
                                     self.options['packages'])
        os.chdir(self.base_dir)
        subprocess.call(cmd, shell=True)
        return self.base_dir

    def update(self):
        pass
