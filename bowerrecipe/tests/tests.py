from bowerrecipe import Recipe
import json
import mock
import os.path
import shutil
import tempfile
import unittest
import zc.buildout


@mock.patch('subprocess.call')
@mock.patch('os.chdir')
class RecipeTest(unittest.TestCase):

    def setUp(self):
        self.parts_dir = tempfile.mkdtemp()
        self.base_dir = os.path.join(self.parts_dir, 'bower')
        self.buildout = {'buildout': {
                             'parts-directory': self.parts_dir}}

    def tearDown(self):
        shutil.rmtree(self.parts_dir, ignore_errors=True)

    def test_exe_should_default_to_bower_on_path(self, chdir, spcall):
        options = {'recipe': 'bowerrecipe', 'packages': 'jquery'}
        Recipe(self.buildout, 'bower', options)
        self.assertEqual('bower', options['executable'])

    def test_at_least_one_package_should_be_specified(self, chdir, spcall):
        options = {'recipe': 'bowerrecipe'}
        self.assertRaises(zc.buildout.UserError, Recipe,
                          self.buildout, 'bower', options)

    def test_base_directory_should_have_a_default(self, chdir, spcall):
        options = {'recipe': 'bowerrecipe', 'packages': 'jquery'}
        Recipe(self.buildout, 'bower', options)
        self.assertEqual(self.base_dir, options['base-directory'])

    def test_bowerrc_file_should_reside_in_base_dir(self, chdir, spcall):
        options = {'recipe': 'bowerrecipe',
                   'base-directory': self.parts_dir,
                   'packages': 'jquery'}
        bowerrc = os.path.join(self.parts_dir, '.bowerrc')
        recipe = Recipe(self.buildout, 'bower', options)

        recipe.install()

        self.assertTrue(os.path.exists(bowerrc))

    def test_bowerrc_file_should_be_configured(self, chdir, spcall):
        options = {'recipe': 'bowerrecipe', 'packages': 'jquery'}
        recipe = Recipe(self.buildout, 'bower', options)
        expected = json.dumps({'directory': options['downloads']})
        bowerrc = os.path.join(self.base_dir, '.bowerrc')

        recipe.install()

        with open(bowerrc) as f:
            config = json.dumps(json.load(f))
        self.assertEqual(expected, config)

    def test_install_returns_bowerrc_and_downloads_dir(self, chdir, spcall):
        options = {'recipe': 'bowerrecipe',
                   'packages': 'jquery',
                   'downloads': '../downloads'}
        recipe = Recipe(self.buildout, 'bower', options)

        base_path, downloads_path = recipe.install()
        self.assertEqual(os.path.join(self.base_dir, '.bowerrc'), base_path)
        self.assertEqual(os.path.join(self.parts_dir, 'downloads'),
                         downloads_path)

    def test_install_should_call_bower_install(self, chdir, spcall):
        options = {'recipe': 'bowerrecipe',
                   'packages': 'jquery',
                   'executable': 'testbinary'}
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

    def test_multiple_packages_can_be_installed(self, chdir, spcall):
        options = {'recipe': 'bowerrecipe', 'packages': 'jquery bootstrap'}
        recipe = Recipe(self.buildout, 'bower', options)

        recipe.install()

        spcall.assert_called_with('bower install jquery bootstrap', shell=True)

    def test_packages_can_be_specified_on_multiple_lines(self, chdir, spcall):
        options = {'recipe': 'bowerrecipe',
                   'packages': '\n  jquery#1.8.1  \n  underscore  '}
        recipe = Recipe(self.buildout, 'bower', options)

        recipe.install()

        spcall.assert_called_with('bower install jquery#1.8.1 underscore',
                                  shell=True)
