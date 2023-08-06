def test_with_build_number(monkeypatch):
    from setuptools_scm.version import format_version, ScmVersion

    monkeypatch.setenv('BUILD_NUMBER', '42')

    assert format_version(ScmVersion('1.0'),
                          version_scheme='guess-next-dev',
                          local_scheme='node-date-and-build-number') == '1.0+b42'
    assert format_version(ScmVersion('1.0', distance=1, node='baadf00d'),
                          version_scheme='guess-next-dev',
                          local_scheme='node-date-and-build-number') == '1.1.dev1+baadf00d.b42'


def test_without_build_number():
    from setuptools_scm.version import format_version, ScmVersion

    assert format_version(ScmVersion('1.0'),
                          version_scheme='guess-next-dev',
                          local_scheme='node-date-and-build-number') == '1.0'
    assert format_version(ScmVersion('1.0', distance=1, node='baadf00d'),
                          version_scheme='guess-next-dev',
                          local_scheme='node-date-and-build-number') == '1.1.dev1+baadf00d'
