# Purpose: trusted string tag reader & stream tag reader
# Created: 10.04.2016
# Copyright (C) 2016, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from .types import DXFTag, is_point_code, cast_tag
from .const import DXFStructureError

DUMMY_TAG = DXFTag(999, '')


def string_tagger(s):
    """ Generates DXFTag() from trusted (internal) source - relies on
    well formed and error free DXF format. Does not skip comment
    tags 999.
    """
    def next_tag():
        return DXFTag(int(lines[pos]), lines[pos+1])

    lines = s.split('\n')
    if s.endswith('\n'):  # split() creates an extra item, if s ends with '\n'
        lines.pop()
    pos = 0
    count = len(lines)
    while pos < count:
        x = next_tag()
        pos += 2
        code = x.code
        if is_point_code(code):
            y = next_tag()  # y coordinate is mandatory - string_tagger relies on well formed DXF strings
            pos += 2
            if pos < count:
                z = next_tag()  # z coordinate just for 3d points
            else:  # if string s ends with a 2d point
                z = DUMMY_TAG
            if z.code == code + 20:
                pos += 2
                point = (float(x.value), float(y.value), float(z.value))
            else:
                point = (float(x.value), float(y.value))
            yield DXFTag(code, point)
        else:
            yield cast_tag(x)


def skip_comments(tagger, comments=None):
    if comments is None:
        comments = []
    for tag in tagger:
        if tag.code != 999:
            yield tag
        else:
            comments.append(tag.value)


def low_level_tagger(stream):
    """ Generates DXFTag(code, value) tuples from a stream (untrusted external source) and does not optimize coordinates.
    Does not skip comment tags 999. code is always an int and value is always an unicode string without a trailing '\n'.
    Works with file system streams and StringIO() streams.
    """
    def next_tag():
        code = stream.readline()
        value = stream.readline()
        if code and value:  # StringIO(): empty strings indicates EOF
            return DXFTag(int(code[:-1]), value[:-1])  # without '\n'
        else:  # StringIO(): missing '\n' indicates EOF
            raise EOFError()

    try:
        while True:
            yield next_tag()
    except EOFError:
        return


def tag_optimizer(tagger):
    """ Optimizes from low_level_tagger() imported tags. Does not skip comment tags 999.
    """
    class Counter:
        def __init__(self):
            self.counter = 0

    undo_tag = None
    line = Counter()  # writeable line counter for next_tag(), Python 2.7 does not support the nonlocal statement

    def next_tag():
        line.counter += 2
        return next(tagger)

    while True:
        try:
            if undo_tag is not None:
                x = undo_tag
                undo_tag = None
            else:
                x = next_tag()
            code = x.code
            if is_point_code(code):
                y = next_tag()  # y coordinate is mandatory
                if y.code != code + 10:  # like 20 for base x-code 10
                    raise DXFStructureError("Missing required y coordinate near line: {}.".format(line.counter))
                z = next_tag()  # z coordinate just for 3d points
                try:
                    if z.code == code + 20:  # it is a z-coordinate like (30, 0.0) for base x-code 10
                        point = (float(x.value), float(y.value), float(z.value))
                    else:
                        point = (float(x.value), float(y.value))
                        undo_tag = z
                except ValueError:
                    raise DXFStructureError('Invalid floating point values near line: {}.'.format(line.counter))
                yield DXFTag(code, point)
            else:  # just a single tag
                try:
                    yield cast_tag(x)
                except ValueError:
                    raise DXFStructureError('Invalid tag (code={code}, value="{value}") near line: {line}.'.format(
                        line=line.counter,
                        code=x.code,
                        value=x.value,
                    ))
        except StopIteration:
            return
