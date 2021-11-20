"""Set default parameters and jupyter display format."""

__all_ = ['set_default_engine', 'set_default_format', 'set_jupyter_format']


def set_default_engine(engine: str) -> str:
    """Change the default engine, return the old default value.

    Args:
        engine: new default engine for all present and newly created instances.

    Returns:
        The old default engine.
    """
    from . import parameters

    parameters.verify_engine(engine)

    old_default_engine = parameters.Parameters._engine
    parameters.Parameters._engine = engine
    return old_default_engine


def set_default_format(format: str) -> str:
    """Change the default format, return the old default value.

    Args:
        format: new default format for all present and newly created instances.

    Returns:
        The old default format.
    """
    from . import parameters

    parameters.verify_format(format)

    old_default_format = parameters.Parameters._format
    parameters.Parameters._format = format
    return old_default_format


def set_jupyter_format(jupyter_format: str) -> str:
    """Change the default mimetype format for ``_repr_mimebundle_(include, exclude)``
        and return the old value.

    Args:
        jupyter_format: new display format for all present and newly created instances.

    Returns:
        The old default display format.
    """
    from . import jupyter_integration

    mimetype = jupyter_integration.get_jupyter_format_mimetype(jupyter_format)

    old_mimetype = jupyter_integration.JupyterIntegration._jupyter_mimetype
    old_format = jupyter_integration.get_jupyter_mimetype_format(old_mimetype)

    jupyter_integration.JupyterIntegration._jupyter_mimetype = mimetype
    return old_format
