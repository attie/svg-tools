import re

RE_SEP       = r'( +| *, *)'
RE_SEP_ORNEG = r'( +| *, *|(?=-))'

RE_NUM_INT   = r'-?[0-9]+'
RE_NUM_FLOAT = r'-?[0-9]*\.?[0-9]+'
RE_NUM_SCI   = r'-?[0-9]*\.?[0-9]+(e[+-]?[0-9]+)?'

class SvgPathComponent:
    def __init__(self, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def configure(self, cmd, is_relative, translate=(0,0), scale=(1,1), decimal_places=5):
        self.cmd = cmd
        self.is_relative = is_relative
        self.translate = translate
        self.scale = scale
        self.decimal_places = decimal_places

    def process(self, **kwargs):
        pass

    def format(self, **kwargs):
        pass

class SvgPathXY(SvgPathComponent):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def process(self):
        if not self.is_relative:
            self.x += self.translate[0]
            self.y += self.translate[1]

        self.x *= self.scale[0]
        self.y *= self.scale[1]

        self.x = round(self.x, self.decimal_places)
        self.y = round(self.y, self.decimal_places)

    def format(self):
        return f'{self.cmd}{self.x},{self.y}'

class SvgPathMoveTo(SvgPathXY):
    re_pattern = fr'{RE_SEP}?(?P<x>{RE_NUM_SCI}){RE_SEP_ORNEG}(?P<y>{RE_NUM_SCI})'

    @classmethod
    def try_mode(self, text):
        if text[0] == 'M':
            return self, False
        if text[0] == 'm':
            return self, True

class SvgPathLineTo(SvgPathXY):
    re_pattern = fr'{RE_SEP}?(?P<x>{RE_NUM_SCI}){RE_SEP_ORNEG}(?P<y>{RE_NUM_SCI})'

    @classmethod
    def try_mode(self, text):
        if text[0] == 'L':
            return self, False
        if text[0] == 'l':
            return self, True

class SvgPathLineToHoriz(SvgPathComponent):
    re_pattern = fr'{RE_SEP}?(?P<x>{RE_NUM_SCI})'

    @classmethod
    def try_mode(self, text):
        if text[0] == 'H':
            return self, False
        if text[0] == 'h':
            return self, True

    def __init__(self, x):
        self.x = float(x)

    def process(self):
        if not self.is_relative:
            self.x += self.translate[0]

        self.x *= self.scale[0]

        self.x = round(self.x, self.decimal_places)

    def format(self):
        return f'{self.cmd}{self.x}'

class SvgPathLineToVert(SvgPathComponent):
    re_pattern = fr'{RE_SEP}?(?P<y>{RE_NUM_SCI})'

    @classmethod
    def try_mode(self, text):
        if text[0] == 'V':
            return self, False
        if text[0] == 'v':
            return self, True

    def __init__(self, y):
        self.y = float(y)

    def process(self):
        if not self.is_relative:
            self.y += self.translate[1]

        self.y *= self.scale[1]

        self.y = round(self.y, self.decimal_places)

    def format(self):
        return f'{self.cmd}{self.y}'

class SvgPathCurveTo(SvgPathComponent):
    re_pattern = fr'{RE_SEP}?(?P<x1>{RE_NUM_SCI}){RE_SEP_ORNEG}(?P<y1>{RE_NUM_SCI}){RE_SEP_ORNEG}' \
                          fr'(?P<x2>{RE_NUM_SCI}){RE_SEP_ORNEG}(?P<y2>{RE_NUM_SCI}){RE_SEP_ORNEG}' \
                          fr'(?P<x>{RE_NUM_SCI}){RE_SEP_ORNEG}(?P<y>{RE_NUM_SCI})'

    @classmethod
    def try_mode(self, text):
        if text[0] == 'C':
            return self, False
        if text[0] == 'c':
            return self, True

    def __init__(self, x1, y1, x2, y2, x, y):
        self.x1 = float(x1)
        self.y1 = float(y1)
        self.x2 = float(x2)
        self.y2 = float(y2)
        self.x = float(x)
        self.y = float(y)

    def process(self):
        if not self.is_relative:
            self.x1 += self.translate[0]
            self.y1 += self.translate[1]
            self.x2 += self.translate[0]
            self.y2 += self.translate[1]
            self.x += self.translate[0]
            self.y += self.translate[1]

        self.x1 *= self.scale[0]
        self.y1 *= self.scale[1]
        self.x2 *= self.scale[0]
        self.y2 *= self.scale[1]
        self.x *= self.scale[0]
        self.y *= self.scale[1]

        self.x1 = round(self.x1, self.decimal_places)
        self.y1 = round(self.y1, self.decimal_places)
        self.x2 = round(self.x2, self.decimal_places)
        self.y2 = round(self.y2, self.decimal_places)
        self.x = round(self.x, self.decimal_places)
        self.y = round(self.y, self.decimal_places)

    def format(self):
        return f'{self.cmd}{self.x1},{self.y1} {self.x2},{self.y2} {self.x},{self.y}'

class SvgPathCurveToShort(SvgPathComponent):
    re_pattern = fr'{RE_SEP}?(?P<x2>{RE_NUM_SCI}){RE_SEP_ORNEG}(?P<y2>{RE_NUM_SCI}){RE_SEP_ORNEG}' \
                          fr'(?P<x>{RE_NUM_SCI}){RE_SEP_ORNEG}(?P<y>{RE_NUM_SCI})'

    @classmethod
    def try_mode(self, text):
        if text[0] == 'S':
            return self, False
        if text[0] == 's':
            return self, True

    def __init__(self, x2, y2, x, y):
        self.x2 = float(x2)
        self.y2 = float(y2)
        self.x = float(x)
        self.y = float(y)

    def process(self):
        if not self.is_relative:
            self.x2 += self.translate[0]
            self.y2 += self.translate[1]
            self.x += self.translate[0]
            self.y += self.translate[1]

        self.x2 *= self.scale[0]
        self.y2 *= self.scale[1]
        self.x *= self.scale[0]
        self.y *= self.scale[1]

        self.x2 = round(self.x2, self.decimal_places)
        self.y2 = round(self.y2, self.decimal_places)
        self.x = round(self.x, self.decimal_places)
        self.y = round(self.y, self.decimal_places)

    def format(self):
        return f'{self.cmd}{self.x2},{self.y2} {self.x},{self.y}'

class SvgPathArcTo(SvgPathComponent):
    re_pattern = fr'{RE_SEP}?(?P<rx>{RE_NUM_SCI}){RE_SEP_ORNEG}(?P<ry>{RE_NUM_SCI}){RE_SEP_ORNEG}' \
                          fr'(?P<x_axis_rotation>{RE_NUM_SCI}){RE_SEP_ORNEG}' \
                          fr'(?P<large_arc_flag>{RE_NUM_INT}){RE_SEP_ORNEG}(?P<sweep_flag>{RE_NUM_INT}){RE_SEP_ORNEG}' \
                          fr'(?P<x>{RE_NUM_SCI}){RE_SEP_ORNEG}(?P<y>{RE_NUM_SCI})'

    @classmethod
    def try_mode(self, text):
        if text[0] == 'A':
            return self, False
        if text[0] == 'a':
            return self, True

    def __init__(self, rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, x, y):
        self.rx = float(rx)
        self.ry = float(ry)
        self.x_axis_rotation = float(x_axis_rotation)
        self.large_arc_flag = int(large_arc_flag)
        self.sweep_flag = int(sweep_flag)
        self.x = float(x)
        self.y = float(y)

    def process(self):
        if not self.is_relative:
            self.x += self.translate[0]
            self.y += self.translate[1]

        self.rx *= self.scale[0]
        self.ry *= self.scale[1]
        self.x *= self.scale[0]
        self.y *= self.scale[1]

        self.rx = round(self.rx, self.decimal_places)
        self.ry = round(self.ry, self.decimal_places)
        self.x = round(self.x, self.decimal_places)
        self.y = round(self.y, self.decimal_places)

    def format(self):
        return f'{self.cmd}{self.rx},{self.ry} {self.x_axis_rotation} {self.large_arc_flag},{self.sweep_flag} {self.x},{self.y}'

class SvgPathClose(SvgPathComponent):
    re_pattern = r'^'

    @classmethod
    def try_mode(self, text):
        if text[0] == 'Z':
            return self, False
        if text[0] == 'z':
            return self, True

    def format(self):
        return f'{self.cmd}' # + '\n'

class SvgTranslate:
    def __init__(self, translate=(0,0), scale=(1,1), decimal_places=5):
        self.translate = translate
        self.scale = scale
        self.decimal_places = decimal_places

        self.handlers = [
            SvgPathMoveTo,
            SvgPathLineTo,
            SvgPathLineToHoriz,
            SvgPathLineToVert,
            SvgPathCurveTo,
            SvgPathCurveToShort,
            SvgPathArcTo,
            SvgPathClose,
        ]

    def trymatch(self, string, regex, flags=0):
        if regex is None:
            raise Exception('no regex...')

        match = re.match(regex, string, flags=flags)
        if match is None:
            print(regex)
            print(string)
            raise Exception('no match... ')

        match_end = match.span()[1]
        match_dict = match.groupdict()

        string_trimmed = string[match_end:]

        return string_trimmed, match_dict

    def parse(self, path):
        while path != '':
            path, match = self.trymatch(path, r'^ *(?P<mode>.)?')
            mode = match['mode']

            if mode is None:
                if path == '':
                    break

                print(path)
                raise Exception('missing mode...')

            for handler in self.handlers:
                if handler.try_mode(mode):
                    break

            path, match = self.trymatch(path, handler.re_pattern)

            with handler(**match) as h:
                h.configure(mode, mode.islower(), self.translate, self.scale, self.decimal_places)
                h.process()

                yield h.format()
