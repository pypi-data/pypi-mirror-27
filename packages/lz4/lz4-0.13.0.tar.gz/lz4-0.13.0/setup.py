#!/usr/bin/env python
from setuptools import setup, find_packages, Extension
import subprocess
import os
import sys
from distutils import ccompiler

def pkgconfig_cmd(cmd, libname):
    try:
        pkg_config_exe = os.environ.get('PKG_CONFIG', None) or 'pkg-config'
        # poor-man's check_output (for Python 2.6 compat)
        p = subprocess.Popen([pkg_config_exe, cmd, libname], stdout=subprocess.PIPE)
        stdout, _ = p.communicate()
        res = p.wait() # communicate already waits for us so this shouldn't block
        if res != 0:
            # pkg-config failed
            return None
        return stdout.decode('utf-8')
    except OSError:
        # pkg-config not present
        return None

def library_is_installed(libname):
    ''' Check to see if we have a library called 'libname' installed.

    This uses pkg-config to check for existence of the library, and
    returns True if it's found, False otherwise. If pkg-config isn't found,
    False is returned. '''
    return pkgconfig_cmd('--exists', libname) is not None

def get_cflags(libname):
    return pkgconfig_cmd('--cflags', libname).split()

def get_ldflags(libname):
    return pkgconfig_cmd('--libs', libname).split()

# Check to see if we have a lz4 library installed on the system and
# use it if so. If not, we'll use the bundled library.
liblz4_found = library_is_installed('liblz4')

# Check to see if we have the py3c headers installed on the system and
# use it if so. If not, we'll use the bundled library.
py3c_found = library_is_installed('py3c')

# Set up the extension modules. If a system wide lz4 library is found, we'll
# use that. Otherwise we'll build with the bundled one. If we're building
# against the system lz4 library we don't set the compiler flags, so they'll be
# picked up from the environment. If we're building against the bundled lz4
# files, we'll set the compiler flags to be consistent with what upstream lz4
# recommends. In addition, if we're building against the bundled library files,
# we'll set LZ4_VERSION for legacy compatibility.

include_dirs = []
libraries = []

lz4version_sources = [
    'lz4/_version.c'
]

lz4block_sources = [
    'lz4/block/_block.c'
]

lz4frame_sources = [
    'lz4/frame/_frame.c'
]

if liblz4_found is True:
    extra_link_args = get_ldflags('liblz4')
else:
    include_dirs.append('lz4libs')
    extra_link_args = []
    lz4version_sources.extend(
        [
            'lz4libs/lz4.c',
        ]
    )
    lz4block_sources.extend(
        [
            'lz4libs/lz4.c',
            'lz4libs/lz4hc.c',
        ]
    )
    lz4frame_sources.extend(
        [
            'lz4libs/lz4.c',
            'lz4libs/lz4hc.c',
            'lz4libs/lz4frame.c',
            'lz4libs/xxhash.c',
        ]
    )

if py3c_found is False:
    include_dirs.append('py3c')

compiler = ccompiler.get_default_compiler()

if compiler == 'msvc':
    extra_compile_args = ['/Ot', '/Wall']
elif compiler in ('unix', 'mingw32'):
    if liblz4_found:
        extra_compile_args = get_cflags('liblz4')
    else:
        extra_compile_args = [
            '-O3',
            '-Wall',
            '-Wundef'
        ]
else:
    print('Unrecognized compiler: {0}'.format(compiler))
    sys.exit(1)

lz4version = Extension('lz4._version',
                       lz4version_sources,
                       extra_compile_args=extra_compile_args,
                       extra_link_args=extra_link_args,
                       libraries=libraries,
                       include_dirs=include_dirs,
)

lz4block = Extension('lz4.block._block',
                     lz4block_sources,
                     extra_compile_args=extra_compile_args,
                     extra_link_args=extra_link_args,
                     libraries=libraries,
                     include_dirs=include_dirs,
)

lz4frame = Extension('lz4.frame._frame',
                     lz4frame_sources,
                     extra_compile_args=extra_compile_args,
                     extra_link_args=extra_link_args,
                     libraries=libraries,
                     include_dirs=include_dirs,
)

# Finally call setup with the extension modules as defined above.
setup(
    name='lz4',
    use_scm_version={
        'write_to': "lz4/version.py",
    },
    setup_requires=[
        'setuptools_scm',
        'pytest-runner',
    ],
    description="LZ4 Bindings for Python",
    long_description=open('README.rst', 'r').read(),
    author='Jonathan Underwood',
    author_email='jonathan.underwood@gmail.com',
    url='https://github.com/python-lz4/python-lz4',
    packages=find_packages(),
    ext_modules=[
        lz4version,
        lz4block,
        lz4frame
    ],
    tests_require=[
        'pytest',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
