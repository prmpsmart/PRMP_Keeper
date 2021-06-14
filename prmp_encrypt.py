

import random, base64, zlib

class EN_DE:
    def __init__(self, mode, text, level):
        self.mode = mode
        self.text = text
        self.level = level

class PRMP_Encrypt:
    'Mini encryption'

    def space_dealer(self, text, with_space=1):
        'Deals with the insertion or removal of space " " : in the actual text'

        space=[chr(35) + chr(97) + chr(35), chr(35) + chr(97) + chr(98) + chr(35), chr(35) + chr(98) + chr(97) + chr(35), chr(35) + chr(98) + chr(35)]
        comad = chr(32)

        if with_space:
            reset = []
            for letter in text:
                if letter == comad: rep = random.choice(space)
                else: rep = letter
                reset.append(rep)
            text = ''.join(reset)
        else:
            while True:
                for on in space:
                    if on in text: text = text.replace(on,comad)
                if space[0] or space[1] or space[2] or space[3] not in text: break

        return text

    def easy_en_decode(self, text):
        'As the name entails'
        d = {}
        for c in (65, 97):
            for i in range(26): d[chr(i+c)] = chr((i+13) % 26 + c)

        easy = ''.join(d.get(c,c) for c in text)

        return easy

    def hard_en_decode(self, text):
        'As the name entails'

        f = {}
        f[chr(95)] = chr(96)
        f[chr(96)] = chr(95)
        f[chr(97)] = chr(126)
        f[chr(126)] = chr(97)

        for a in range(58, 65): f[chr(a)] = chr(a + 7) # +7
        for a in range(65, 72): f[chr(a)] = chr(a - 7) # -7
        for a in range(81, 85): f[chr(a)] = chr(a + 10) # +10
        for a in range(91, 95): f[chr(a)] = chr(a - 10) # -10
        for a in range(72, 78): f[chr(a)] = chr(a + 13) # +13
        for a in range(85, 91): f[chr(a)] = chr(a - 13) # -13
        for a in range(78, 81): f[chr(a)] = chr(a + 45) # +45
        for a in range(123, 126): f[chr(a)] = chr(a - 45) # -45
        for a in range(33,  58): f[chr(a)] = chr(a + 65) # +65
        for a in range(98,  123): f[chr(a)] = chr(a - 65) # -65

        hard = ''.join(f.get(c,c) for c in text)

        return hard

    def encode(self, text, level=1):
        'The different levels of encryptions'

        if level == 1: returnable = self.easy_en_decode(text)

        elif level == 2:
            a = self.space_dealer(text, with_space=1)
            b = self.hard_en_decode(a)
            returnable = self.easy_en_decode(b)

        elif level == 3:
            a = self.space_dealer(text)
            b = self.easy_en_decode(a)
            returnable = self.hard_en_decode(b)

        elif level == 4:
            a = self.hard_en_decode(text)
            returnable = base64.b64encode(a.encode())

        elif level == 5:
            a = self.easy_en_decode(text)
            b = self.hard_en_decode(a)
            returnable = base64.b64encode(b.encode())

        elif level == 6:
            a = self.hard_en_decode(text)
            b = self.easy_en_decode(a)
            returnable = base64.b64encode(zlib.compress(zlib.compress(b.encode())))

        elif level == 7:
            a = self.hard_en_decode(text)
            returnable = base64.b64encode(base64.b64encode(base64.b64encode(base64.b64encode(a.encode()))))

        elif level == 8: returnable = base64.b64encode(zlib.compress(text.encode()))

        elif level == 9:
            a = base64.b64encode(zlib.compress(zlib.compress(zlib.compress(text.encode()))))
            returnable = str(a)

        return str(returnable)

    def decode(self, text, level=1):
        'The different levels of encryptions'
        if isinstance(text, str) and text.startswith("b'"):
            text = text[2:-1]
            text = text.encode()

        if level == 1: returnable = self.easy_en_decode(text)

        elif level == 2:
            a = self.easy_en_decode(text)
            b = self.hard_en_decode(a)
            returnable = self.space_dealer(b, with_space=0)

        elif level == 3:
            a = self.hard_en_decode(text)
            b = self.easy_en_decode(a)
            returnable = self.space_dealer(b, with_space=False)

        elif level == 4:
            a = base64.b64decode(text)
            returnable = self.hard_en_decode(a.decode())

        elif level == 5:
            a = base64.b64decode(text)
            a = self.hard_en_decode(a.decode())
            returnable = self.easy_en_decode(a)

        elif level == 6:
            a = zlib.decompress(zlib.decompress(base64.b64decode(text)))
            b = self.easy_en_decode(a.decode())
            returnable = self.hard_en_decode(b)

        elif level == 7:
            a = base64.b64decode(base64.b64decode(base64.b64decode(base64.b64decode(text))))
            returnable = self.hard_en_decode(a.decode())

        elif level == 8: returnable = zlib.decompress(base64.b64decode(text)).decode()

        elif level == 9: returnable = zlib.decompress(zlib.decompress(zlib.decompress(base64.b64decode(text)))).decode()

        return str(returnable)

    def process(self, obj):
        if obj.mode == 'EN': return EN_DE('DE', self.decode(obj.text), level=obj.level)
        else: return EN_DE('EN', self.encode(obj.text), level=obj.level)



