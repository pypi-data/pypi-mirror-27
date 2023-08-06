
import os
import jpype
import platform
import yaml
from hanlp import *

class Configuration(object):

    def __init__(self, hanlder_or_path):
        if hanlder_or_path is None:
            raise Exception("config should not be null.")

        if isinstance(hanlder_or_path, str):
            self.configuration = yaml.load(open(hanlder_or_path, 'rb'))
        else:
            self.configuration = hanlder_or_path

        try:
            self.configuration["java_class_path"] = os.path.join(self.configuration["root"], self.configuration["java_class"])
            self.configuration["java_sources_path"] = os.path.join(self.configuration["root"], self.configuration["java_sources"])
            self.configuration["properties_path"] = os.path.join(self.configuration["root"], self.configuration["properties"])
        except KeyError as e:
            print(e)

    def __iter__(self):
        return iter(self.configuration)

    def __getitem__(self, item):
        return self.configuration[item]


class StartRelease(object):

    def startJVM(self, class_path, jar_path):
        if not is_jvm_started():
            if is_windows():
                class_path = '-Djava.class.path=' + class_path + ";" + jar_path
            else:
                class_path = '-Djava.class.path=' + class_path + ":" + jar_path
            jpype.startJVM(jpype.getDefaultJVMPath(), class_path, '-Xms1g', '-Xmx1g')

    def release(self):
        jpype.shutdownJVM()


def build(java_class_path, java_source_path, properties_path):
    if not os.path.exists(java_class_path):
        raise Exception("hanlp jar class not found.")
    if not os.path.exists(java_source_path):
        raise Exception("hanlp sources jar class not found.")
    if not os.path.exists(properties_path):
        raise Exception("hanlp properties file not found.")

    from shutil import copyfile
    module_path = os.path.dirname(java_class_path)
    copyfile(properties_path, os.path.join(module_path, "hanlp.default.properties"))
    with open(properties_path, "r+") as f:
        properties = f.read()
        f.seek(0)
        f.truncate()
        f.write(properties.replace('root=/usr/home/HanLP/', "root=" + module_path))
        print('Create hanlp.properties')

def is_jvm_started():
    return jpype.isJVMStarted()

def is_windows():
    return (platform.system() == 'Windows')

def is_darwin():
    return (platform.system() == 'Darwin')

def is_linux():
    return (platform.system() == 'Linux')

def jclass(java_class):
    return jpype.JClass(java_class)

def initialize(java_class):
    return jpype.JClass(java_class)()