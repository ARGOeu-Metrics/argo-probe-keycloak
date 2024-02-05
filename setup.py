import glob
from distutils.core import setup

NAME = 'argo-probe-keycloak'
NAGIOSPLUGINS = '/usr/libexec/argo/probes/keycloak'


def get_ver():
    try:
        for line in open(NAME+'.spec'):
            if "Version:" in line:
                return line.split()[1]

    except IOError:
        SystemExit(1)


setup(
    name=NAME,
    version=get_ver(),
    license='ASL 2.0',
    author='SRCE',
    author_email='kzailac@srce.hr',
    description='Package includes probe for keycloak login',
    url='https://github.com/ARGOeu-Metrics/argo-probe-keycloak',
    package_dir={'argo_probe_keycloak': 'modules'},
    data_files=[('/usr/libexec/argo/probes/keycloak', glob.glob('src/*'))],
    packages=['argo_probe_keycloak']
)
