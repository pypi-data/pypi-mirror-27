import xldeploy
import pkg_resources
import platform

from os import environ, path
from sys import argv
from xld.xld_args_validator import XldArgsValidator
from xld.help import help_message


class XldCommands:

    def __init__(self, url=None, username=None, password=None):
        if self.__is_config_required(argv[0:]):
            self.__url = self.__get_arg_value(url, XldArgsValidator.XL_DEPLOY_URL)
            self.__username = self.__get_arg_value(username, XldArgsValidator.XL_DEPLOY_USERNAME)
            self.__password = self.__get_arg_value(password, XldArgsValidator.XL_DEPLOY_PASSWORD)

            XldArgsValidator().validate(self.__url, self.__username, self.__password)

            config = xldeploy.Config.initialize(url=self.__url + '/deployit',
                                                username=self.__username,
                                                password=self.__password)
            self.__client = xldeploy.Client(config)

    def __get_arg_value(self, param_value, env_variable):
        return environ.get(env_variable, None) if param_value is None else param_value

    def apply(self, path):
        return self.__client.deployfile.apply(open(path, 'r').read())

    def generate(self, *directories):
        return self.__client.deployfile.generate(list(directories))

    def help(self):
        return help_message

    def version(self):
        packagedir = path.abspath(path.join(__file__, "../"))
        version = "xld-py-cli %s from %s (python %s)" % (pkg_resources.get_distribution('xld-py-cli').version, packagedir, platform.python_version())
        return version

    def __is_config_required(self, args):
        return 'version' not in args and 'help' not in args
