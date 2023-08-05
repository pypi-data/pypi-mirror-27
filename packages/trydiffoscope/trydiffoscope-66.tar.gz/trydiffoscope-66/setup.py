import subprocess

from distutils.core import setup

VERSION = subprocess.check_output(
    ('dpkg-parsechangelog', '-S', 'Version'),
).decode('utf-8').strip()

setup(
    name='trydiffoscope',
    version=VERSION,
    author="Chris Lamb",
    author_email="lamby@debian.org",
    scripts=(
        'trydiffoscope',
    ),
)
