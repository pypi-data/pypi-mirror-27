# -*- coding: utf-8 -*-


class BytesString:
    def __init__(self, size):
        self.bytes_str_arr = ['00' for x in range(size)]

    def add_string(self, text, index, encoding):
        self.add_to_array(index, value=text.encode(encoding).hex(), type="str")

    def add_integer(self, number, index):
        text = hex(number).replace("0x", "")
        self.add_to_array(index, value=text, type="number")

    def get_bytearray(self):
        return bytearray.fromhex(''.join(self.bytes_str_arr))

    def add_to_array(self, index, **kwargs):
        splited_arr = self.split_by_n(kwargs.get("value"), 2)
        loop_list = list(splited_arr) if kwargs.get("type") == "str" else reversed(list(splited_arr))

        for element in loop_list:
            element = ("0%s" % element) if len(element) == 1 else element

            if kwargs.get("type") == "str":
                self.bytes_str_arr[index - 1] = element
                index += 1
            else:
                self.bytes_str_arr[index - 1] = element
                index -= 1

    def split_by_n(self, seq, n):
        while seq:
            yield seq[:n]
            seq = seq[n:]
