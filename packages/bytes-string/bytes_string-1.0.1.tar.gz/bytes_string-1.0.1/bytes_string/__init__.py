# -*- coding: utf-8 -*-


class BytesString:
    def __init__(self, size):
        self.bytes_str_arr = ['00' for x in range(size)]

    def add_string(self, text, index, encoding):
        self.add_to_array(text.encode(encoding).hex(), index)

    def add_integer(self, number, index):
        text = hex(number).replace("0x", "")
        self.add_to_array(text, index)

    def get_bytearray(self):
        return bytearray.fromhex(''.join(self.bytes_str_arr))

    def add_to_array(self, text, index):
        splited_arr = self.split_by_n(text, 2)
        for element in reversed(list(splited_arr)):
            element = ("0%s" % element) if len(element) == 1 else element

            self.bytes_str_arr[index - 1] = element
            index -= 1

    def split_by_n(self, seq, n):
        while seq:
            yield seq[:n]
            seq = seq[n:]