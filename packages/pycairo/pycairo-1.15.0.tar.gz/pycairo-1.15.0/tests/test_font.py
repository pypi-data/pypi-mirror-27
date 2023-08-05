import cairo
import pytest


def test_font_face_cmp_hash():
    surface = cairo.ImageSurface(0, 10, 10)
    context = cairo.Context(surface)
    ff = context.get_font_face()
    other = context.get_font_face()
    assert ff == other
    assert not ff != other
    assert hash(ff) == hash(other)

    sf = context.get_scaled_font()
    other = context.get_scaled_font()
    assert sf == other
    assert not sf != other
    assert hash(sf) == hash(other)

    fo = context.get_font_options()
    # FontOptions compare by their content and they are mutable, so not
    # hashable.
    with pytest.raises(TypeError):
        hash(fo)


def test_toy_font_get_slant():
    font_face = cairo.ToyFontFace("")
    assert font_face.get_slant() == cairo.FontSlant.NORMAL
    assert isinstance(font_face.get_slant(), cairo.FontSlant)


def test_toy_font_get_weight():
    font_face = cairo.ToyFontFace("")
    assert font_face.get_weight() == cairo.FontWeight.NORMAL
    assert isinstance(font_face.get_weight(), cairo.FontWeight)


@pytest.fixture
def font_options():
    surface = cairo.ImageSurface(0, 10, 10)
    return surface.get_font_options()


def test_font_options_get_antialias(font_options):
    assert font_options.get_antialias() == cairo.Antialias.DEFAULT
    assert isinstance(font_options.get_antialias(), cairo.Antialias)


def test_font_options_get_hint_metrics(font_options):
    assert font_options.get_hint_metrics() == cairo.HintMetrics.ON
    assert isinstance(font_options.get_hint_metrics(), cairo.HintMetrics)


def test_font_options_get_hint_style(font_options):
    assert font_options.get_hint_style() == cairo.HintStyle.DEFAULT
    assert isinstance(font_options.get_hint_style(), cairo.HintStyle)


def test_font_options_get_subpixel_order(font_options):
    assert font_options.get_subpixel_order() == cairo.SubpixelOrder.DEFAULT
    assert isinstance(font_options.get_subpixel_order(), cairo.SubpixelOrder)


def test_scaled_font_get_ctm():
    surface = cairo.ImageSurface(0, 10, 10)
    ctx = cairo.Context(surface)
    sf = ctx.get_scaled_font()
    matrix = sf.get_ctm()
    assert isinstance(matrix, cairo.Matrix)


def test_scaled_font_get_font_matrix():
    surface = cairo.ImageSurface(0, 10, 10)
    ctx = cairo.Context(surface)
    sf = ctx.get_scaled_font()
    matrix = sf.get_font_matrix()
    assert isinstance(matrix, cairo.Matrix)


def test_scaled_font_get_font_options():
    surface = cairo.ImageSurface(0, 10, 10)
    ctx = cairo.Context(surface)
    sf = ctx.get_scaled_font()
    font_options = sf.get_font_options()
    assert isinstance(font_options, cairo.FontOptions)


def test_scaled_font_text_to_glyphs():
    surface = cairo.ImageSurface(0, 10, 10)
    ctx = cairo.Context(surface)
    sf = ctx.get_scaled_font()
    assert sf.text_to_glyphs(0, 0, u"") == ([], [], 0)
    glyphs, clusters, flags = sf.text_to_glyphs(0, 0, u"a")
    assert sf.text_to_glyphs(0, 0, u"a", True) == (glyphs, clusters, flags)
    assert len(glyphs) == 1
    assert isinstance(glyphs[0], cairo.Glyph)
    assert len(clusters) == 1
    assert isinstance(clusters[0], cairo.TextCluster)
    assert flags == 0
    assert sf.text_to_glyphs(0, 0, u"a", False) == glyphs
    glyphs, clusters, flags = sf.text_to_glyphs(0, 0, u"a b")
    assert len(glyphs) == 3
    assert glyphs[0] != glyphs[1]
    assert len(clusters) == 3
