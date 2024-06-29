import unittest
from unittest.mock import patch
from io import StringIO

from devops.config_management.cli_parser import create_parser

class TestCliParser(unittest.TestCase):

    def setUp(self):
        self.parser = create_parser()
        pass 

    def test_bootstrap_cmd(self):
        # cli tested: file.py bootstrap
        args = self.parser.parse_args(["bootstrap"])
        self.assertEqual(args.command, "bootstrap")
        pass

    def test_prepare_cmd(self):
        # cli tested: file.py prepare
        args = self.parser.parse_args(["prepare"])
        self.assertEqual(args.command, "prepare")
        pass

    def test_build_with_default_cmd(self):
        # cli tested: 
        #   $ file.py build
        args = self.parser.parse_args(["build"])
        self.assertEqual(args.command, "build")
        self.assertEqual(args.type, "debug")
    
    def test_build_cmd(self):
        # cli tested: 
        #   $ file.py build --type debug
        args = self.parser.parse_args(['build', '--type', 'debug'])
        self.assertEqual(args.command, 'build')
        self.assertEqual(args.type, 'debug')
        
        # cli tested: file.py build -t debug
        args = self.parser.parse_args(['build', '-t', 'debug'])
        self.assertEqual(args.command, 'build')
        self.assertEqual(args.type, 'debug')

        # cli tested: 
        #   $ file.py build --type release
        args = self.parser.parse_args(['build', '--type', 'release'])
        self.assertEqual(args.command, 'build')
        self.assertEqual(args.type, 'release')

        # cli tested: file.py build -t release
        args = self.parser.parse_args(['build', '-t', 'release'])
        self.assertEqual(args.command, 'build')
        self.assertEqual(args.type, 'release')
        pass

    def test_help(self):
        with self.assertRaises(SystemExit):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('sys.argv', ['cli_tool.py', '--help']):
                    self.parser.parse_args()
                help_output = mock_stdout.getvalue()
                self.assertIn('usage:', help_output)
                self.assertIn('Automation tool to manage, configure, build and package C++ projects.', help_output)
                self.assertIn('Available commands:', help_output)

    def test_subcommand_help(self):
        with self.assertRaises(SystemExit):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('sys.argv', ['cli_tool.py', 'bootstrap', '--help']):
                    self.parser.parse_args()
                help_output = mock_stdout.getvalue()
                self.assertIn('usage:', help_output)
                self.assertIn('Initialize the environment', help_output)
                self.assertIn('--env', help_output)


    def test_invalidCommand(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['booty'])
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['prepa'])
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['bult', '--type', 'release'])
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['something else'])


    def test_invalidCommandOption(self):
        with self.assertRaises(SystemExit):
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                self.parser.parse_args(['bootstrap', '--type', 'debug'])
            error_output = mock_stderr.getvalue().strip()
            self.assertIn('unrecognized arguments: --type debug', error_output)

        with self.assertRaises(SystemExit):
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                self.parser.parse_args(['prepare', '--type', 'debug'])
            error_output = mock_stderr.getvalue().strip()
            self.assertIn('unrecognized arguments: --type debug', error_output)

        # with self.assertRaises(SystemExit):
        #     with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
        #         self.parser.parse_args(['build', '--typ', 'debug'])
        #     error_output = mock_stderr.getvalue().strip()
        #     self.assertIn('unrecognized arguments: --typ debug', error_output)

        # with self.assertRaises(SystemExit):
        #     with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
        #         self.parser.parse_args(['build', '-type', 'debug'])
        #     error_output = mock_stderr.getvalue().strip()
        #     self.assertIn('unrecognized arguments: -type debug', error_output)

    def test_invalidCommandOptionValue(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['bootstrap', '--type', 'bla'])
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['prepare', '--type', 'bla'])
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['build', '--type', 'bla'])


if __name__ == '__main__':
    unittest.main()
