# -*- coding: utf8 -*-

import glob
import nltk
import re


class TextProcessor:
    def __init__(self):
        self.word_regexp = re.compile(u"(?u)\w+")

    def tokenize(self, text, stop_words=None):
        tokens = self.word_regexp.findall(text.lower())
        filtered_tokens = []
        for token in tokens:
            ch = token[0]
            if stop_words is not None and token in stop_words:
                continue
            filtered_tokens.append(token)
        return filtered_tokens

    @staticmethod
    def get_files_in_folder(folder):
        files = sorted(glob.glob(folder + '\\*'))
        files_in_folder = [s.rsplit('\\', 1)[-1] for s in files]
        files_in_folder.sort(key=lambda x: int(x))
        return files_in_folder

    @staticmethod
    def get_document_text(folder):
        files_in_folder = TextProcessor.get_files_in_folder(folder)
        text = ""
        if len(files_in_folder) == 0:
            raise Exception('No folder "{0}" found'.format(folder))
        for file in files_in_folder:
            file = folder + '\\' + file
            with open(file, mode='r', encoding='utf-8', errors='replace') as f:
                text += f.read()
        return text

    @staticmethod
    def fix_text(text_string):
        joined_text_string = ""
        for string in text_string.splitlines():
            if len(string) < 2:
                continue
            if string[-1] == '-' or string[-1] == '­' or string[-1] == '­':
                joined_text_string += string[:-1]
            else:
                joined_text_string += string

        for i in range(len(joined_text_string) - 1):
            if joined_text_string[i] == '.':
                joined_text_string = joined_text_string[:i + 1] + ' ' + joined_text_string[i + 1:]
        return joined_text_string

    def process_texts(self):
        text_string = ""
        # folder = '..\\text\\bd000087382'  # сленг
        # folder = '..\\text\\bd000000190'  # фитонимы
        # folder = '..\\text\\bd000000509'  # предприятие
        folder = '..\\text\\bd000000053'

        text = self.get_document_text(folder)
        fixed_text = self.fix_text(text)
        print(fixed_text)

if __name__ == "__main__":
    tp = TextProcessor()
    tp.process_texts()
