# -*- coding: utf8 -*-

import glob
import nltk
import re
from enum import Enum


class SectionType(Enum):
    Beginning = 1
    Ending = 2


class TextSection:
    def __init__(self):
        self.parts = []

    def add_part(self, part):
        self.parts.append(part)


class TextPart:
    def __init__(self):
        pass


class TextParagraph(TextPart):
    def __init__(self):
        TextPart.__init__(self)
        pass


class TextList(TextPart):
    def __init__(self):
        TextPart.__init__(self)
        pass


class TextProcessor:
    def __init__(self):
        self.word_regexp = re.compile(u"(?u)\w+")
        self.approximate_line_length = 0

        self.text_sections = []

    def tokenize(self, text, stop_words=None):
        tokens = self.word_regexp.findall(text.lower())
        filtered_tokens = []
        for token in tokens:
            if stop_words is not None and token in stop_words:
                continue
            # Here we can insert some token filters if needed
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

    # try to determine if a new line is really needed, or it was just a line break
    def is_new_line(self, current_line, previous_line):
        if current_line[0] in '123456789' and current_line[1] in '.)' or \
                current_line[0] in '123456789' and current_line[1] in '0123456789' and current_line[2] in '.)':
            if current_line[1] in '.)':
                number = int(current_line[0])
            else:
                number = int(current_line[:2])
            if 0 < number < 50:
                return True
            else:
                return False
        elif len(previous_line) < self.approximate_line_length * 0.8:
            return True
        elif ord(current_line[0]) in range(ord('а'), ord('я')) and previous_line[-1] not in '.;:':
            return False
        elif current_line[0] == '-' and previous_line[-1] in ';.:':
            return True
        return False

    @staticmethod
    def remove_extra_spaces(text):
        new_text = ""
        previous_ch = ' '
        for line in text.splitlines():
            if len(line) < 2:
                continue
            new_line = ''
            for ch in line:
                if not (ch == ' ' and previous_ch == ' '):
                    new_line += ch
                previous_ch = ch
            while new_line[-1] == ' ':
                new_line = new_line[:-1]
            new_text += '\n' + new_line
        return new_text

    @staticmethod
    def find_line_length(text):  # Figuring out the approximate line length in original pdf
        length_dictionary = dict()
        for line in text.splitlines():
            length_dictionary.setdefault(len(line), 0)
            length_dictionary[len(line)] += 1
        length_sum = 0
        total_lines = 0
        for item in length_dictionary.items():
            if item[0] > 2 and item[1] > 1:
                length_sum += item[0] * item[1]
                total_lines += item[1]
        average = int(length_sum / total_lines)
        line_length = average
        for i in range(average, int(average * 0.8), -1):  # Certainly not the smartest way to do this
            if length_dictionary[i] / length_dictionary[i + 1] < 0.5:
                line_length = i
                break
        print(average)
        print(line_length)
        return line_length

    def join_lines(self, text):  # Trying to set newlines as they were inteded
        new_text = ' '
        previous_line = ""
        for line in text.splitlines():
            if len(line) < 2:
                continue
            try:
                # Single number on the line is most probably a page number
                int(line)
                continue
            except ValueError:
                pass
            if new_text[-1] == '-':
                new_text = new_text[:-1] + line
            elif self.is_new_line(line, previous_line):
                new_text = new_text + '\n' + line
            else:
                new_text = new_text + ' ' + line
            previous_line = line
        return new_text

    @staticmethod
    def filter_lines(text):
        new_text = ''
        for line in text.splitlines():
            if line[:4] == 'Рис.' or line[:4] == 'Табл':
                continue
            new_text += '\n' + line
        return new_text

    @staticmethod
    def replace_nonprintable_characters(text):
        printable_text = ""
        for ch in text:
            if ord(ch) > 1120:
                substr = '?'
            else:
                substr = ch
            printable_text += substr
        return printable_text

    def improve_text_quality(self, text):
        text = self.remove_extra_spaces(text)
        self.approximate_line_length = self.find_line_length(text)
        text = self.replace_nonprintable_characters(text)
        text = self.join_lines(text)
        text = self.filter_lines(text)

        return text

    def process_texts(self):
        # folder = '..\\text\\bd000087382'  # сленг
        # folder = '..\\text\\bd000000190'  # фитонимы
        # folder = '..\\text\\bd000000509'  # предприятие
        folder = '..\\text\\bd000000515'

        text = self.get_document_text(folder)
        fixed_text = self.improve_text_quality(text)
        print(fixed_text)

if __name__ == "__main__":
    tp = TextProcessor()
    tp.process_texts()
