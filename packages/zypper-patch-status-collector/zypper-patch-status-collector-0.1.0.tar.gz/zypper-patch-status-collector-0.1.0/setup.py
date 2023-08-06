# encoding=utf-8

from setuptools import setup

setup(
    name='zypper-patch-status-collector',
    use_scm_version=True,
    description='Exports patch status in Prometheus-compatible format.',
    long_description=open('README.rst').read(),
    url='https://gitlab.com/Marix/zypper-patch-status-collector',
    author='Matthias Bach',
    author_email='marix@marix.org',
    license='GPL-3.0+',
    packages=['zypper_patch_status_collector'],
    install_requires=['setuptools'],
    setup_requires=['setuptools_scm'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Monitoring',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'zypper-patch-status-collector=zypper_patch_status_collector._cli:main',
        ],
    },
)
