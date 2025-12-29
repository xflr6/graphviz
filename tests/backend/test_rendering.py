import contextlib
import pathlib
import os
import shutil
import subprocess

import pytest

import graphviz
from graphviz import _tools
from graphviz.backend import rendering

import _common

TEST_FILES_DIRECTORY = pathlib.Path(__file__).parent.parent


@pytest.fixture(scope='module')
def files_path():
    return TEST_FILES_DIRECTORY


@pytest.mark.exe
def test_render_missing_file(quiet, engine='dot', format_='pdf'):
    with pytest.raises(subprocess.CalledProcessError) as e:
        graphviz.render(engine, format_, 'nonexisting', quiet=quiet)
    assert e.value.returncode == 2


@pytest.mark.parametrize(
    'args, expected_exception, match',
    [(['', 'pdf', 'nonfilepath'], ValueError, r'unknown engine'),
     (['dot', '', 'nonfilepath'], ValueError, r'unknown format'),
     (['dot', 'ps', 'nonfilepath', '', None], ValueError, r'unknown renderer'),
     (['dot', 'ps', 'nonfilepath', None, 'core'],
      graphviz.RequiredArgumentError, r'without renderer'),
     (['dot', 'ps', 'nonfilepath', 'ps', ''], ValueError, r'unknown formatter')],
    ids=lambda x: getattr(x, '__name__', x))
def test_render_unknown_parameter_raises(args, expected_exception, match,
                                         supported_number=3):
    checker = (pytest.deprecated_call(match=rf'\b{supported_number:d} positional args\b')
               if len(args) > supported_number
               else contextlib.nullcontext())
    with pytest.raises(expected_exception, match=match), checker:
        graphviz.render(*args)


@pytest.mark.exe
@pytest.mark.parametrize(
    'format_, renderer, formatter, expected_suffix',
    [('pdf', None, None, 'pdf'),
     pytest.param('plain', 'dot', 'core', 'core.dot.plain',
         marks=pytest.mark.xfail('graphviz.version() == (5, 0, 1)',
         reason='https://gitlab.com/graphviz/graphviz/-/issues/2270'))])
@pytest.mark.parametrize('engine', ['dot'])
def test_render(capsys, tmp_path, engine, format_, renderer, formatter,
                expected_suffix, filename='hello.gv',
                data=b'digraph { hello -> world }'):
    lpath = tmp_path / filename
    assert lpath.write_bytes(data) == len(data) == lpath.stat().st_size
    rendered = lpath.with_suffix(f'{lpath.suffix}.{expected_suffix}')

    with pytest.deprecated_call(match=r'\b3 positional args\b'):
        result = graphviz.render(engine, format_, str(lpath),
                                 renderer, formatter)

    assert result == str(rendered)

    assert rendered.exists()
    assert rendered.stat().st_size
    assert capsys.readouterr() == ('', '')


@pytest.mark.exe
def test_render_img(capsys, tmp_path, files_path, engine='dot', format_='pdf'):
    subdir = tmp_path / 'subdir'
    subdir.mkdir()

    img_path = subdir / 'dot_red.png'
    shutil.copy(files_path / img_path.name, img_path)
    assert img_path.exists()
    assert img_path.stat().st_size

    gv_path = subdir / 'img.gv'
    rendered = gv_path.with_suffix(f'{gv_path.suffix}.{format_}')
    gv_rel, rendered_rel = (p.relative_to(tmp_path) for p in (gv_path, rendered))
    assert all(str(s).startswith('subdir') for s in (gv_rel, rendered_rel))
    gv_path.write_text(f'graph {{ red_dot [image="{img_path.name}"] }}',
                       encoding='ascii')

    with _common.as_cwd(tmp_path):
        assert graphviz.render(engine, format_, gv_rel) == str(rendered_rel)

    assert rendered.exists()
    assert rendered.stat().st_size
    assert capsys.readouterr() == ('', '')


@pytest.mark.exe
def test_render_outfile_differnt_parent(capsys, tmp_path,
                                        engine='dot', outfile='spam.pdf',
                                        source='graph { spam }'):
    outfile = tmp_path / 'rendered' / outfile
    outfile.parent.mkdir()
    assert not outfile.exists()

    filepath = tmp_path / 'sources' / outfile.with_suffix('.gv').name
    filepath.parent.mkdir()
    assert filepath.write_text(source) == len(source) == filepath.stat().st_size

    result = graphviz.render(engine, filepath=filepath, outfile=outfile)

    assert result == os.fspath(outfile)

    assert outfile.exists()
    assert outfile.stat().st_size

    assert capsys.readouterr() == ('', '')


@pytest.mark.parametrize(
    'directory', [None, 'dot_sources'])
def test_render_mocked(capsys, mock_run, quiet, directory,
                       filepath='nonfilepath'):
    mock_run.return_value = subprocess.CompletedProcess(_common.INVALID_CMD,
                                                        returncode=0,
                                                        stdout='stdout',
                                                        stderr='stderr')

    if directory is not None:
        filepath = os.path.join(directory, filepath)

    result = graphviz.render('dot', 'pdf', filepath,
                             y_invert=True,
                             neato_no_op=True,
                             quiet=quiet)

    assert result == f'{filepath}.pdf'

    mock_run.assert_called_once_with([_common.EXPECTED_DOT_BINARY,
                                      '-Kdot', '-Tpdf',
                                      '-y', '-n1',
                                      '-O', 'nonfilepath'],
                                     capture_output=True,
                                     cwd=_tools.promote_pathlike(directory),
                                     startupinfo=_common.StartupinfoMatcher())
    assert capsys.readouterr() == ('', '' if quiet else 'stderr')


@pytest.mark.parametrize(
    'args,  kwargs, expected_exception, match',
    [(['dot'], {}, graphviz.RequiredArgumentError, r'filepath: \(required'),
     (['dot'], {'format': 'png'}, graphviz.RequiredArgumentError, r'filepath: \(required'),
     (['dot'], {'filepath': 'spam'}, graphviz.RequiredArgumentError, r'format: \(required'),
     (['dot', 'svg'], {}, graphviz.RequiredArgumentError, r'filepath: \(required'),
     (['dot', 'gv', 'spam.gv'], {'outfile': 'spam.gv'}, ValueError,
      r"outfile 'spam\.gv' must be different from input file 'spam\.gv'"),
     (['dot'], {'outfile': 'spam.png',
                'raise_if_result_exists': True, 'overwrite_filepath': True},
      ValueError,
      r'overwrite_filepath cannot be combined with raise_if_result_exists'),
     (['dot'], {'outfile': 'spam.png', 'raise_if_result_exists': True},
      graphviz.FileExistsError, r"output file exists: 'spam.png'")])
def test_render_raises_mocked(tmp_path, mock_run, args, kwargs,
                              expected_exception, match):
    if issubclass(expected_exception, FileExistsError):
        existing_outfile = tmp_path / kwargs['outfile']
        existing_outfile.touch()

    with _common.as_cwd(tmp_path):
        with pytest.raises(expected_exception, match=match):
            graphviz.render(*args, **kwargs)


@pytest.mark.parametrize(
    'filepath,  kwargs, expected_fspath',
    [('spam.gv', {'format': 'pdf'}, 'spam.gv.pdf'),
     ('spam.gv', {'format': 'plain', 'renderer': 'dot'}, 'spam.gv.dot.plain')])
def test_get_outfile(filepath, kwargs, expected_fspath):
    result = rendering.get_outfile(filepath, **kwargs)
    assert os.fspath(result) == expected_fspath


@pytest.mark.parametrize(
    'outfile,  expected_fspath',
    [('spam.pdf', 'spam.gv'),
     ('spam', 'spam.gv')])
def test_get_filepath(outfile, expected_fspath):
    result = rendering.get_filepath(outfile)
    assert os.fspath(result) == expected_fspath


@pytest.mark.parametrize(
    'outfile_name, format, expected_result',
    [('spam.gv.pdf', None, 'pdf'),
     ('spam.jpeg', None, 'jpeg'),
     ('spam.SVG', None, 'svg'),
     ('spam.pdf', None, 'pdf'),
     ('spam.pdf', 'pdf', 'pdf')])
def test_get_format(outfile_name, format, expected_result):
    outfile = pathlib.Path(outfile_name)

    result = rendering.get_format(outfile, format=format)

    assert result == expected_result


@pytest.mark.parametrize(
    'outfile_name,  format, expected_result, expected_warning, match',
    [('spam.jpg', 'jpeg', 'jpeg', graphviz.FormatSuffixMismatchWarning,
      r"expected format 'jpg' from outfile differs from given format: 'jpeg'"),
     ('spam.dot', 'plain', 'plain', graphviz.FormatSuffixMismatchWarning,
      r"expected format 'dot' from outfile differs from given format: 'plain'"),
     ('spam', 'svg', 'svg', graphviz.UnknownSuffixWarning,
      r"unknown outfile suffix '' \(expected: '\.svg'\)"),
     ('spam.peng', 'png', 'png', graphviz.UnknownSuffixWarning,
      r"unknown outfile suffix '.peng' \(expected: '\.png'\)"),
     ('spam', 'pdf', 'pdf', graphviz.UnknownSuffixWarning,
      r"unknown outfile suffix '' \(expected: '\.pdf'\)")])
def test_get_format_warns(outfile_name, format, expected_result,
                          expected_warning, match):
    outfile = pathlib.Path(outfile_name)

    with pytest.warns(expected_warning, match=match):
        result = rendering.get_format(outfile, format=format)

    assert result == expected_result


@pytest.mark.parametrize(
    'outfile_name,  expected_exception, match',
    [('spam', graphviz.RequiredArgumentError,
      r"cannot infer rendering format from suffix '' of outfile: 'spam'"),
     ('spam.peng', graphviz.RequiredArgumentError,
      r"cannot infer rendering format from suffix '.peng' of outfile: 'spam.peng'"),
     ('spam.wav', graphviz.RequiredArgumentError,
      r"cannot infer rendering format from suffix '.wav' of outfile: 'spam.wav'")])
def test_get_format_raises(outfile_name, expected_exception, match):
    outfile = pathlib.Path(outfile_name)

    with pytest.raises(expected_exception, match=match):
        rendering.get_format(outfile, format=None)
