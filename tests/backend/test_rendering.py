import pathlib
import os
import shutil
import subprocess

import pytest

import graphviz
from graphviz.backend import rendering

import _common

TEST_FILES_DIRECTORY = pathlib.Path(__file__).parent.parent


@pytest.fixture(scope='module')
def files_path():
    return TEST_FILES_DIRECTORY


@pytest.mark.exe
def test_render_missing_file(quiet, engine='dot', format_='pdf'):
    with pytest.raises(subprocess.CalledProcessError) as e:
        graphviz.render(engine, format_, '', quiet=quiet)
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
def test_render_unknown_parameter_raises(args, expected_exception, match):
    with pytest.raises(expected_exception, match=match):
        graphviz.render(*args)


@pytest.mark.exe
@pytest.mark.parametrize(
    'format_, renderer, formatter, expected_suffix',
    [('pdf', None, None, 'pdf'),
     ('plain', 'dot', 'core', 'core.dot.plain')])
@pytest.mark.parametrize('engine', ['dot'])
def test_render(capsys, tmp_path, engine, format_, renderer, formatter,
                expected_suffix, filename='hello.gv',
                data=b'digraph { hello -> world }'):
    lpath = tmp_path / filename
    lpath.write_bytes(data)
    rendered = lpath.with_suffix(f'{lpath.suffix}.{expected_suffix}')

    result = graphviz.render(engine, format_, str(lpath), renderer, formatter)

    assert result == str(rendered)

    assert rendered.stat().st_size
    assert capsys.readouterr() == ('', '')


@pytest.mark.exe
def test_render_img(capsys, tmp_path, files_path, engine='dot', format_='pdf'):
    subdir = tmp_path / 'subdir'
    subdir.mkdir()

    img_path = subdir / 'dot_red.png'
    shutil.copy(files_path / img_path.name, img_path)
    assert img_path.stat().st_size

    gv_path = subdir / 'img.gv'
    rendered = gv_path.with_suffix(f'{gv_path.suffix}.{format_}')
    gv_rel, rendered_rel = (p.relative_to(tmp_path) for p in (gv_path, rendered))
    assert all(str(s).startswith('subdir') for s in (gv_rel, rendered_rel))
    gv_path.write_text(f'graph {{ red_dot [image="{img_path.name}"] }}',
                       encoding='ascii')

    with _common.as_cwd(tmp_path):
        assert graphviz.render(engine, format_, gv_rel) == str(rendered_rel)

    assert rendered.stat().st_size
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

    result = graphviz.render('dot', 'pdf', filepath, quiet=quiet)

    assert result == f'{filepath}.pdf'

    mock_run.assert_called_once_with([_common.EXPECTED_DOT_BINARY,
                                      '-Kdot', '-Tpdf', '-O', 'nonfilepath'],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     cwd=directory,
                                     startupinfo=_common.StartupinfoMatcher())
    assert capsys.readouterr() == ('', '' if quiet else 'stderr')


@pytest.mark.parametrize(
    'args,  kwargs, expected_exception, match',
    [(['dot'], {}, graphviz.RequiredArgumentError, r'format: \(required'),
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
    'outfile_name, format, expected_result',
    [('spam.gv.pdf', None, 'pdf'),
     ('spam.jpeg', None, 'jpeg'),
     ('spam.SVG', None, 'svg'),
     ('spam.pdf', None, 'pdf'),
     ('spam.pdf', 'pdf', 'pdf'),
     ('spam', 'pdf', 'pdf')])
def test_get_rendering_format(outfile_name, format, expected_result):
    outfile = pathlib.Path(outfile_name)

    result = rendering.get_rendering_format(outfile, format=format)

    assert result == expected_result


@pytest.mark.parametrize(
    'outfile_name,  format, expected_result, expected_warning, match',
    [('spam.jpg', 'jpeg', 'jpeg', UserWarning,
      r"expected format 'jpg' from outfile differs from given format: 'jpeg'"),
     ('spam.dot', 'plain', 'plain', UserWarning,
      r"expected format 'dot' from outfile differs from given format: 'plain'"),
     ('spam', 'svg', 'svg', UserWarning,
      r"unknown outfile suffix '' \(expected: '.svg'\)"),
     ('spam.peng', 'png', 'png', UserWarning,
      r"unknown outfile suffix '.peng' \(expected: '.png'\)")])
def test_get_rendering_format_warns(outfile_name, format, expected_result,
                                    expected_warning, match):
    outfile = pathlib.Path(outfile_name)

    with pytest.warns(expected_warning, match=match):
        result = rendering.get_rendering_format(outfile, format=format)

    assert result == expected_result


@pytest.mark.parametrize(
    'outfile_name,  expected_exception, match',
    [('spam', graphviz.RequiredArgumentError,
      r"cannot infer rendering format from suffix '' of outfile: 'spam'"),
     ('spam.peng', graphviz.RequiredArgumentError,
      r"cannot infer rendering format from suffix '.peng' of outfile: 'spam.peng'"),
     ('spam.mp3', graphviz.RequiredArgumentError,
      r"cannot infer rendering format from suffix '.mp3' of outfile: 'spam.mp3'")])
def test_get_rendering_format_raises(outfile_name, expected_exception, match):
    outfile = pathlib.Path(outfile_name)

    with pytest.raises(expected_exception, match=match):
        rendering.get_rendering_format(outfile, format=None)
