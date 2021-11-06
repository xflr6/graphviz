import graphviz


def test_saves_source_from_file(tmp_path, src='graph spam { spam }'):
    path = tmp_path / 'spam.gv'
    path.write_text(src)
    stat_before = path.stat()

    source = graphviz.Source.from_file(path)
    source.save()

    assert path.stat().st_mtime == stat_before.st_mtime, 'file not overwritten'
    assert path.read_text() == src, 'file contents unchanged'
    assert ''.join(source) == f'{src}\n', 'src with final newline'
