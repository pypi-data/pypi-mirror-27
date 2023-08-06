
import hanlp.utils as utils
import hanlp.parsers as parsers

import jpype
import os

class HanLPTool(utils.StartRelease):

    def __init__(self, config=None):

        self.configuration = utils.Configuration(config)

        utils.build(self.configuration["java_class_path"],
                    self.configuration["java_sources_path"],
                    self.configuration["properties_path"])

        self.startJVM(self.configuration['root'], self.configuration['java_class_path'])

        self.HanLP = utils.jclass('com.hankcs.hanlp.HanLP')

        self.apply_settings()

    def apply_settings(self):
        self.HanLPConfig = utils.jclass('com.hankcs.hanlp.HanLP$Config')
        try:
            self.HanLPConfig.ShowTermNature = self.configuration['show_term_nature']
            self.HanLPConfig.Normalization = self.configuration['normalization']
        except KeyError as e:
            print(e)

    def segment(self, text):
        """
        分词
        :param text:文本
        :return:切分后的单词列表
        """
        StandardTokenizer = jpype.JClass("com.hankcs.hanlp.tokenizer.StandardTokenizer")
        # try:
        #     if self.config['enable_custom_dic']:
        #         StandardTokenizer.SEGMENT.enableCustomDictionary(True)
        #     else:
        #         StandardTokenizer.SEGMENT.enableCustomDictionary(False)
        # except KeyError as error:
        #     print(error)

        segments = []
        for w in self.HanLP.segment(text):
            segments.append(str(w).strip())
        return segments

    def parse_dependency(self, sentence):
        """
        依存文法分析
        :param sentence: 待分析的句子
        :return:    CoNLL格式的依存关系树
        """
        return self.HanLP.parseDependency(sentence)

    def extract_phrase(self, text, size):
        """
        提取短语
        :param text: 文本
        :param size: 需要多少个短语
        :return: 一个短语列表，大小 <= size
        """
        return self.HanLP.extractPhrase(text, size)

    def extract_new_words(self, text, size, new_words_only):
        """
        提取词语
        :param text: 大文本
        :param size: 需要提取词语的数量
        :param new_words_only: 是否只提取词典中没有的词语
        :return: 一个词语列表
        """
        if new_words_only:
            return self.HanLP.extract_words(text, size, new_words_only)
        else:
            return self.HanLP.extract_words(text, size)

    def extract_keywords(self, document, size):
        return self.HanLP.extractKeyword(document, size)

    def extract_summary(self, document, size):
        """
        自动摘要
        分割目标文档时的默认句子分隔符为，,。:：“”？?！!；;
        :param document: 目标文档
        :param size: 需要的关键句的个数
        :return: 关键句列表
        """
        return self.HanLP.extractSummary(document, size)

    def get_summary(self, document, max_length):
        """
        自动摘要
        分割目标文档时的默认句子分割符为，,。:：“”？?！!；;
        :param document: 目标文档
        :param max_length: 需要摘要的长度
        :return: 摘要文本
        """
        return self.HanLP.getSummary(document, max_length)

    def convert_string_to(self, string, mode):

        if mode == "hk2tw":
            #香港繁體到臺灣正體
            return self.HanLP.hk2tw(string)
        elif mode == "tw2hk":
            #臺灣正體到香港繁體
            return self.HanLP.tw2hk(string)
        elif mode == "hk2t":
            #香港繁體到繁體
            return self.HanLP.hk2t(string)
        elif mode == "t2hk":
            #繁體到香港繁體
            return self.HanLP.t2hk(string)
        elif mode == "tw2t":
            #臺灣正體到繁體
            return self.HanLP.tw2t(string)
        elif mode == "t2tw":
            #繁體到臺灣正體
            self.HanLP.t2tw(string)
        elif mode == "hk2s":
            #香港繁體到簡體
            return self.HanLP.hk2s(string)
        elif mode == "s2hk":
            #簡體到香港繁體
            return self.HanLP.s2hk(string)
        elif mode == "tw2s":
            #臺灣正體到簡體
            return self.HanLP.tw2s(string)
        elif mode == "s2tw":
            #簡體到臺灣正體
            return self.HanLP.s2tw(string)
        elif mode == "t2s":
            #繁体中文(大陆标准)转简体中文
            return self.HanLP.t2s(string)
        elif mode == "s2t":
            #简体中文转繁体中文(大陆标准)
            return self.HanLP.s2t(string)
        elif mode == "2tc":
            #简转繁
            return self.HanLP.convertToTraditionalChinese(string)
        elif mode == "2sc":
            #繁转简
            return self.HanLP.convertToSimplifiedChinese(string)

    def convert2pinyin(self, text, separator, remain_none=True, first_char=False):
        """
        转化为拼音
        :param text:文本
        :param separator:分隔符
        :param remain_none: 有些字没有拼音（如标点），是否保留它们的拼音（true用none表示，false用原字符表示）
        :param first_char: 是否返回拼音首字母
        :return:一个字符串，由[拼音][分隔符][拼音]构成
        """
        if first_char:
            return self.HanLP.convertToPinyinFirstCharString(text, separator, remain_none)
        else:
            return self.HanLP.convertToPinyinString(text, separator, remain_none)
