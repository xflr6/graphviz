import shutil
import subprocess

import pytest

import graphviz

import _utils


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
def test_render_missing_file(quiet, engine='dot', format_='pdf'):
    with pytest.raises(subprocess.CalledProcessError) as e:
        graphviz.render(engine, format_, '', quiet=quiet)
    assert e.value.returncode == 2


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

    assert graphviz.render(engine, format_, str(lpath), renderer, formatter) == str(rendered)

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

    with _utils.as_cwd(tmp_path):
        assert graphviz.render(engine, format_, gv_rel) == str(rendered_rel)

    assert rendered.stat().st_size
    assert capsys.readouterr() == ('', '')


def test_render_mocked(capsys, mocker, run, quiet):
    run.return_value = subprocess.CompletedProcess(mocker.sentinel.cmd,
                                                   returncode=0,
                                                   stdout='stdout',
                                                   stderr='stderr')

    assert graphviz.render('dot', 'pdf', 'nonfilepath', quiet=quiet) == 'nonfilepath.pdf'

    run.assert_called_once_with([_utils.DOT_BINARY, '-Kdot', '-Tpdf', '-O', 'nonfilepath'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                cwd=None,
                                startupinfo=mocker.ANY,)
    _utils.check_startupinfo(run.call_args.kwargs['startupinfo'])
    assert capsys.readouterr() == ('', '' if quiet else 'stderr')
