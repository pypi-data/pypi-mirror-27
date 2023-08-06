
import os
import hanlp.utils as utils

class NeuralNetworkDependencyParser(utils.StartRelease):
    def __init__(self, config=None):
        self.configuration = utils.Configuration(config)

        utils.build(self.configuration["java_class_path"],
                    self.configuration["java_sources_path"],
                    self.configuration["properties_path"])

        self.startJVM(self.configuration['root'], self.configuration['java_class_path'])

        self.parser = utils.initialize("com.hankcs.hanlp.dependency.nnparser.NeuralNetworkDependencyParser")

        try:
            enable_deprel_translator = self.configuration["enable_deprel_translator"]
            self.parser.enableDeprelTranslator(enable_deprel_translator)

        except KeyError as e:
            print(e)

    def parse(self, sentence):
        return self.parser.parse(sentence)
