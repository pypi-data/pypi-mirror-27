from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='pyjst',
    version='0.1.1',
    description='Bake a template from corresponding JSON object',
    long_description=readme(),
    keywords='simple static template templating json',
    url='http://github.com/GuillaumeDesforges/pyjst',
    author='Guillaume Desforges',
    author_email='aceus02@gmail.com',
    license='MIT',
    packages=['pyjst'],
    install_requires=[
      'jinja2',
    ],
    scripts=['bin/pyjst'],
    zip_safe=False
)
