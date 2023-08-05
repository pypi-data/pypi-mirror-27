import datetime
import setuptools


from stackchat.version import __version__



if __version__.endswith('-dev'):
    __version__ += str(int(datetime.datetime.utcnow().timestamp()))


setup = lambda: setuptools.setup(
    name='stackchat',
    version=__version__,
    python_requires='>=3',
    install_requires=[
        'stack.chat',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: MIT License',
    ],
    url='https://stack.chat',
    author='Jeremy Banks',
    author_email='_@jeremy.ca',
    license='MIT',
)


if __name__ == '__main__':
    setup()
