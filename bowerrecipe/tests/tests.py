from bowerrecipe import Recipe
import json
import mock
import os.path
import shutil
import unittest
import zc.buildout


@mock.patch('subprocess.call')
@mock.patch('os.chdir')
class RecipeTest(unittest.TestCase):

    def setUp(self):
        self.parts_dir = os.path.abspath('parts')
        self.base_dir = os.path.join(self.parts_dir, 'bower')
        self.buildout = {'buildout': {
                             'parts-directory': self.parts_dir}}

    def tearDown(self):
        shutil.rmtree(self.base_dir, ignore_errors=True)

    def test_binary_should_default_to_bower_on_path(self, chdir, spcall):
        options = {'recipe': 'bowerrecipe', 'packages': 'jquery'}
        Recipe(self.buildout, 'bower', options)
        self.assertEqual('bower', options['binary'])

    def test_at_least_one_package_should_be_specified(self, chdir, spcall):
        options = {'recipe': 'bowerrecipe'}
        self.assertRaises(zc.buildout.UserError, Recipe,
                          self.buildout, 'bower', options)

    def test_bowerrc_file_should_be_configured(self, chdir, spcall):
        options = {'recipe': 'bowerrecipe', 'packages': 'jquery'}
        recipe = Recipe(self.buildout, 'bower', options)
        expected = json.dumps({'directory': options['downloads']})
        bowerrc = os.path.join(self.base_dir, '.bowerrc')

        recipe.install()

        with open(bowerrc) as f:
            config = json.dumps(json.load(f))
        self.assertEqual(expected, config)

    def test_install_should_return_base_directory(self, chdir, spcall):
        options = {'recipe': 'bowerrecipe', 'packages': 'jquery'}
        recipe = Recipe(self.buildout, 'bower', options)

        base_path = recipe.install()
        self.assertEqual(self.base_dir, base_path)

    def test_install_should_call_bower_install(self, chdir, spcall):
        options = {'recipe': 'bowerrecipe',
                   'packages': 'jquery',
                   'binary': 'testbinary'}
        recipe = Recipe(self.buildout, 'bower', options)

        recipe.install()

        spcall.assert_called_with('testbinary install jquery', shell=True)

    def test_downloads_default_to_sensible_location(self, chdir, spcall):
        options = {'recipe': 'bowerrecipe', 'packages': 'jquery'}
        Recipe(self.buildout, 'bower', options)
        self.assertEqual('downloads', options['downloads'])

    def test_changes_to_correct_directory_pre_install(self, chdir, spcall):
        options = {'recipe': 'bowerrecipe', 'packages': 'jquery'}
        recipe = Recipe(self.buildout, 'bower', options)

        recipe.install()

        chdir.assert_called_with(self.base_dir)
