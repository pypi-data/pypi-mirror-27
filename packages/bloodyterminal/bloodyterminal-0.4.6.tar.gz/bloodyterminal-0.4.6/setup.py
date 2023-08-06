from setuptools import setup
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='bloodyterminal',
    packages=['bloodyterminal'],
    version='0.4.6',
    description='A little helper to structure your terminal output',
    long_description=long_description,
    author='TheBloodyScreen',
    author_email='jaydee@thebloodyscreen.com',
    license='MIT',
    classifiers=[
                'Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.2',
                'Programming Language :: Python :: 3.3',
                'Programming Language :: Python :: 3.4',
                'Programming Language :: Python :: 3.5',
                'Programming Language :: Python :: 3.6'
    ],
    install_requires=['colorama'],
    url='https://github.com/TheBloodyScreen/bloodyterminal/'
)
