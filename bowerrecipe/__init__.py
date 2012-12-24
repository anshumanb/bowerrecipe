# -*- coding: utf-8 -*-
import zc.buildout
import os.path
import os
import json
import subprocess


class Recipe(object):
    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.base_dir = os.path.join(buildout['buildout']['parts-directory'],
                                     'bower')
        options.setdefault('binary', 'bower')
        options.setdefault('downloads', 'downloads')
        if 'packages' not in options:
            raise zc.buildout.UserError('Missing packages option')


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
