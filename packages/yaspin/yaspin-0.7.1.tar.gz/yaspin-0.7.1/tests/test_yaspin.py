# -*- coding: utf-8 -*-

"""
tests.test_yaspin
~~~~~~~~~~~~~~~~~

Basic unittests.
"""

from __future__ import absolute_import

import os
import sys
from collections import namedtuple
from inspect import getsource

import pytest

from yaspin import Spinner, yaspin
from yaspin.base_spinner import default_spinner
from yaspin.compat import builtin_str, bytes, str, basestring
from yaspin.constants import ENCODING
from yaspin.termcolor import colored


#
# Helpers
#
def to_bytes(str_or_bytes, encoding=ENCODING):
    if isinstance(str_or_bytes, str):
        return str_or_bytes.encode(encoding)
    return str_or_bytes


def to_unicode(str_or_bytes, encoding=ENCODING):
    if isinstance(str_or_bytes, bytes):
        return str_or_bytes.decode(encoding)
    return str_or_bytes


#
# Tests
#

ids = [
    "default frames and interval",
    "str text, str frames",
    "unicode text, unicode frames (marked as unicode)",
    "unicode text, str frames",
    "str text, unicode frames",
    "str text, List[] frames",
    "str text, List[bytes] frames",
    "str text, List[unicode] frames",
    "str text, Tuple[] frames",
    "str text, Tuple[bytes] frames",
    "str text, Tuple[unicode] frames",
]


test_cases = [
    # default frames and interval
    ("", "", None),

    # str text, str frames
    ("Loading", "+x*", 80),

    # unicode text, unicode frames (marked as unicode)
    (u"Загрузка", u"⢄⢂⢁⡁⡈⡐⡠", 80),

    # unicode text, str frames
    ("ℙƴ☂ℌøἤ", "+x*", 80),

    # str text, unicode frames
    ("Loading", "⢄⢂⢁⡁⡈⡐⡠", 80),

    #
    # Iter frames
    #

    # TODO: add custom type that Implements iterable
    #
    # XXX: this is Bad, because different text inputs should
    #      combine with different frames input

    # str text, List[] frames
    ("Empty list", [], 400),

    # str text, List[bytes] frames
    ("Bytes list", [b"\xf0\x9f\x8c\xb2", b"\xf0\x9f\x8e\x84"], 400),

    # str text, List[unicode] frames
    ("Unicode list", [u"🌲", u"🎄"], 400),

    # str text, Tuple[] frames
    ("Empty tuple", (), 400),

    # str text, Tuple[bytes] frames
    ("Bytes tuple", (b"\xf0\x9f\x8c\xb2", b"\xf0\x9f\x8e\x84"), 400),

    # str text, Tuple[unicode] frames
    ("Unicode tuple", (u"🌲", u"🎄"), 400),
]


@pytest.mark.parametrize("text, frames, interval", test_cases, ids=ids)
@pytest.mark.parametrize("right", [False, True], ids=["left", "right"])
@pytest.mark.parametrize("reverse", [False, True], ids=["default", "reverse"])
def test_input_converted_to_unicode(text, frames, interval, right, reverse):
    sp = Spinner(frames, interval)
    swirl = yaspin(sp, text, right=right, reverse=reverse)

    if isinstance(swirl._frames, basestring):
        assert isinstance(swirl._frames, str)

    if isinstance(swirl._frames, (list, tuple)):
        assert isinstance(swirl._frames[0], str)

    assert isinstance(swirl._text, str)


@pytest.mark.parametrize("text, frames, interval", test_cases, ids=ids)
@pytest.mark.parametrize("right", [False, True], ids=["left", "right"])
@pytest.mark.parametrize("reverse", [False, True], ids=["default", "reverse"])
def test_out_converted_to_builtin_str(text, frames, interval, right, reverse):
    sp = Spinner(frames, interval)
    swirl = yaspin(sp, text, right=right, reverse=reverse)

    for _ in range(20):             # test 20 frames
        frame = next(swirl._cycle)
        out = swirl._compose_out(frame)
        assert isinstance(out, builtin_str)


@pytest.mark.parametrize("text, frames, interval", test_cases, ids=ids)
def test_repr(text, frames, interval):
    sp = Spinner(frames, interval)
    swirl = yaspin(sp, text)

    assert isinstance(repr(swirl), builtin_str)


@pytest.mark.parametrize("text, frames, interval", test_cases, ids=ids)
def test_piping_output(text, frames, interval):
    py_fname = "spin.py"
    fname = "out.txt"

    def teardown():
        os.remove(py_fname)
        os.remove(fname)

    code = """\
# -*- coding: utf-8 -*-

import time
from yaspin import yaspin, Spinner

with yaspin(Spinner('%s', %s), '%s') as sp:
    time.sleep(0.5)
    sp.fail('🙀')
"""

    with open(py_fname, 'wb') as f:
        text = to_unicode(text)
        frames = to_unicode(frames)
        interval = to_unicode(interval)
        code = to_unicode(code)
        res = code % (frames, interval, text)
        f.write(to_bytes(res))

    try:
        # $ python spin.py > out.txt
        os.system("{0} {1} > {2}".format(sys.executable, py_fname, fname))
    except UnicodeEncodeError as err:
        pytest.fail(err)
    finally:
        teardown()


@pytest.mark.parametrize("spinner, expected", [
    # None
    (None, default_spinner),

    # hasattr(spinner, "frames") and not hasattr(spinner, "interval")
    (namedtuple('Spinner', "frames")("-\\|/"), default_spinner),

    # not hasattr(spinner, "frames") and hasattr(spinner, "interval")
    (namedtuple('Spinner', "interval")(42), default_spinner),

    # Both attrs, not set
    (Spinner("", 0), default_spinner),

    # Both attrs, not frames
    (Spinner("", 42), default_spinner),

    # Both attrs, not interval
    (Spinner("-\\|/", 0), default_spinner),

    # Both attrs, are set
    (Spinner("-\\|/", 42), Spinner("-\\|/", 42)),
])
def test_set_spinner(spinner, expected):
    swirl = yaspin(spinner)
    assert swirl.spinner == expected


@pytest.mark.parametrize("_, frames, interval", test_cases, ids=ids)
def test_spinner_getter(_, frames, interval):
    swirl = yaspin()
    assert swirl.spinner == default_spinner

    new_spinner = Spinner(frames, interval)
    swirl.spinner = new_spinner
    assert swirl.spinner == swirl._set_spinner(new_spinner)


@pytest.mark.parametrize("_, frames, interval", test_cases, ids=ids)
def test_spinner_setter(_, frames, interval):
    swirl = yaspin()
    assert swirl._spinner == default_spinner
    assert isinstance(swirl._frames, str)
    assert swirl._interval == swirl._spinner.interval * 0.001
    assert isinstance(repr(swirl), builtin_str)

    new_spinner = Spinner(frames, interval)
    swirl.spinner = new_spinner
    assert swirl._spinner == swirl._set_spinner(new_spinner)

    if isinstance(swirl._frames, basestring):
        assert isinstance(swirl._frames, str)

    if isinstance(swirl._frames, (list, tuple)):
        assert isinstance(swirl._frames[0], str)

    assert swirl._interval == swirl._spinner.interval * 0.001
    assert isinstance(repr(swirl), builtin_str)


@pytest.mark.parametrize("case_data", test_cases, ids=ids)
def test_text_property(case_data):
    text = case_data[0]

    swirl = yaspin()
    assert swirl.text == ""

    swirl.text = text
    assert isinstance(swirl.text, str)


@pytest.mark.parametrize("final_text", [
    "", u"",

    "OK", u"OK",

    "✔", u"✔",

    "☀️", u"☀️",

    "💥", u"💥",
])
def test_freeze(final_text):
    swirl = yaspin()
    swirl._freeze(final_text)

    assert isinstance(swirl._last_frame, builtin_str)
    assert swirl._last_frame[-1] == "\n"


def test_ok():
    swirl = yaspin()
    swirl.ok()

    assert isinstance(swirl._last_frame, builtin_str)
    assert swirl._last_frame[-1] == "\n"


def test_fail():
    swirl = yaspin()
    swirl.fail()

    assert isinstance(swirl._last_frame, builtin_str)
    assert swirl._last_frame[-1] == "\n"


#
# Test colors
#
colors_test_cases = [
    # Empty values
    ("", ""),
    (None, None),

    # Supported text colors
    ("red", "red"),
    ("green", "green"),
    ("yellow", "yellow"),
    ("blue", "blue"),
    ("magenta", "magenta"),
    ("cyan", "cyan"),
    ("white", "white"),

    # Unsupported text colors
    ("black", ValueError()),
    ("brown", ValueError()),
    ("orange", ValueError()),

    # Uppercase handling
    ("Red", "red"),
    ("grEEn", "green"),
    ("BlacK", ValueError()),

    # Callables
    (
        lambda frame: colored(frame, 'red', attrs=['bold']),
        lambda frame: colored(frame, 'red', attrs=['bold']),
    )
]


@pytest.mark.parametrize("color, expected", colors_test_cases)
def test_color_argument(color, expected):

    # Exception
    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            yaspin(color=color)

    # Callable arg
    elif callable(color):
        # Compare source code to check funcs equality
        fn1 = yaspin(color=color)._color
        fn2 = expected
        assert getsource(fn1) == getsource(fn2)

    # Common arg
    else:
        assert yaspin(color=color)._color == expected


@pytest.mark.parametrize("color, expected", colors_test_cases)
def test_color_property(color, expected):
    swirl = yaspin()

    # Exception
    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            swirl.color = color

    # Callable arg
    elif callable(color):
        # Compare source code to check funcs equality
        swirl.color = color
        assert getsource(swirl.color) == getsource(expected)

    # Common arg
    else:
        swirl.color = color
        assert swirl.color == expected


@pytest.mark.parametrize("color, expected", colors_test_cases)
def test_compose_out_with_color(color, expected):
    # Skip non relevant cases
    if not expected:
        return
    if isinstance(expected, Exception):
        return

    # Sanitize input
    if hasattr(color, 'lower'):
        color = color.lower()

    swirl = yaspin(color=color)
    out = swirl._compose_out(frame=u'/')
    assert out.startswith('\r\033')
    assert isinstance(out, builtin_str)


#
# Test right properties
#

@pytest.mark.parametrize("right", [False, True], ids=["left", "right"])
def test_right_property_getter(right):
    swirl = yaspin(right=right)
    assert swirl.right == right


@pytest.mark.parametrize("right", [False, True], ids=["left", "right"])
def test_right_property_setter(right):
    swirl = yaspin()
    swirl.right = right
    assert swirl.right == right


#
# Test reverse properties
#

@pytest.mark.parametrize("reverse", [False, True], ids=["default", "reversed"])
def test_reverse_property_getter(reverse):
    swirl = yaspin(reverse=reverse)
    assert swirl.reverse == reverse


@pytest.mark.parametrize("reverse", [False, True], ids=["default", "reversed"])
def test_reverse_property_setter(reverse):
    swirl = yaspin()
    swirl.reverse = reverse

    assert swirl.reverse == reverse
    assert isinstance(swirl._frames, str)
