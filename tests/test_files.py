import os

import graphviz


def test_save_source_from_files(tmp_path):
    dot = graphviz.Digraph(directory=tmp_path)
    dot.edge('hello', 'world')
    dot.render()
    old_stat = os.stat(dot.filepath)

    source = graphviz.Source.from_file(dot.filepath)
    source.save()

    assert os.stat(dot.filepath).st_mtime == old_stat.st_mtime
