from setuptools import setup

setup(
    name='hangcli',
    version='0.1',
    py_modules=['hangcli'],
    url = "http://blog.coderhelper.cn",
    author = "limhang",
    author_email = "lm_hang@163.com",
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hangcli=hangcli:router
    ''',
)
