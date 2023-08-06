from setuptools import setup

setup(
    name="c2dx",
    version='1.0.1',
    description='Cocos2d-x Class Generator for C++',
    url='https://bitbucket.org/cajun_code/c2dx.py',
    author='Allan Davis',
    author_email='cajun.code@gmail.com',
    license='MIT',
    include_package_data=True,
    packages=['c2dx'],
    install_requires=[
        'Click',
        'Jinja2',
        'inflection',
    ],
    entry_points='''
        [console_scripts]
        c2dx=c2dx:cli
    ''',
    zip_safe=False
)
