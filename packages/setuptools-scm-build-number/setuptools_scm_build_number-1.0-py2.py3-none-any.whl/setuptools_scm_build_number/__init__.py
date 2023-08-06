from .__about__ import __version__


def get_node_date_and_build_number(version):
    """
    Return local version as per setuptools_scm, but append the build number if any.
    """
    import os
    from pkg_resources import load_entry_point
    node_and_date = load_entry_point('setuptools_scm', 'setuptools_scm.local_scheme', 'node-and-date')
    version = node_and_date(version)
    build_number = os.getenv('BUILD_NUMBER')

    if version and build_number:
        return '{0}.b{1}'.format(version, build_number)
    elif build_number:
        return '+b{0}'.format(build_number)
    else:
        return version
