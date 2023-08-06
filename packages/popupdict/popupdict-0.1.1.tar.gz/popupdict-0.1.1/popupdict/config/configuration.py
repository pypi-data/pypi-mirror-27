import os.path
from configparser import ConfigParser
from typing import List
import pkg_resources

from popupdict.gtk import *
from .clients import *


class Configuration:
    # 默认配置，始终加载
    DEFAULT_CONFIG = pkg_resources.resource_string(__package__, 'default.ini').decode()
    # 候选配置文件，按顺序检查，只加载第一个存在的文件
    CANDIDATE_CONFIG_FILES = [
        os.path.join(GLib.get_user_config_dir(), 'popup-dict/config.ini'),
        '/etc/popup-dict/config.ini',
    ]  # type: List[str]

    def __init__(self, config_file: str = None):
        parser = ConfigParser(default_section='client')
        parser.read_string(__class__.DEFAULT_CONFIG)

        if config_file:
            if not os.path.exists(config_file):
                raise ConfigError("Config file {} does not exist!".format(repr(config_file)))
            else:
                parser.read(config_file)
        else:
            # 若未指定配置文件，从候选配置文件中加载第一个存在的文件
            for path in __class__.CANDIDATE_CONFIG_FILES:
                if os.path.exists(path):
                    parser.read(path)
                    break

        if not parser.has_section('global'):
            raise ConfigError('Missing configuration section: global')

        # 全局配置
        try:
            global_section = parser['global']
            self.query_client = global_section['query_client']

            # 弹窗显示时间
            self.popup_timeout = global_section.getfloat('popup_timeout')

            # Gtk Global Dark Theme
            # 不设置或设为空则使用系统默认设置
            prefer_dark_theme = global_section.get('prefer_dark_theme')
            if prefer_dark_theme is not None and prefer_dark_theme != '':
                self.prefer_dark_theme = global_section.getboolean('prefer_dark_theme')
                Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", self.prefer_dark_theme)
            else:
                self.prefer_dark_theme = None

        except KeyError as e:
            raise ConfigError('Missing global configuration: ' + e.args[0])

        # 各查询客户端配置
        try:
            self.fake = FakeConfiguration()
            self.youdao_web = YoudaoWebConfiguration(parser['youdao-web'])
            self.youdao_zhiyun = YoudaoZhiyunConfiguration(parser['youdao-zhiyun'])
        except KeyError as e:
            raise ConfigError('Missing configuration section: ' + e.args[0])

    def __repr__(self):
        return 'Configuration(\n  query_method: {},\n  youdao_web: {},\n  youdao_zhiyun: {}\n)'.format(
            self.query_client, self.youdao_web, self.youdao_zhiyun)
