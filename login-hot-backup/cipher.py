DEFAULT_MAPPING = mapping = {
    'A': 'T',
    'B': 'I',
    'C': 'M',
    'D': 'E',
    'E': 'O',
    'F': 'D',
    'G': 'A',
    'H': 'N',
    'I': 'S',
    'J': 'F',
    'K': 'R',
    'L': 'B',
    'M': 'C',
    'N': 'G',
    'O': 'H',
    'P': 'J',
    'Q': 'K',
    'R': 'L',
    'S': 'P',
    'T': 'Q',
    'U': 'U',
    'V': 'V',
    'W': 'W',
    'X': 'X',
    'Y': 'Y',
    'Z': 'Z',
    '0': '9',
    '1': '8',
    '2': '7',
    '3': '6',
    '4': '5',
    '5': '4',
    '6': '3',
    '7': '2',
    '8': '1',
    '9': '0'
}


class PasswordCipher:
    def __init__(self, mapping=None):
        if mapping is None:
            self._mapping = DEFAULT_MAPPING
        else:
            self._mapping = mapping

    def _do_mapping(self, c):
        if c in self._mapping:
            return self._mapping[c]

        return '*'

    def cipher(self, password):
        return "".join([self._do_mapping(c) for c in password])
