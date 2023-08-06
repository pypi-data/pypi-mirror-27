from setuptools import setup

setup(
    name='hangcli',
    version='0.2.0',
    py_modules=['hangcli'],
    url = "http://blog.coderhelper.cn",
    author = "limhang",
    author_email = "lm_hang@163.com",
    data_files=[('hangcli/react', ['src/react/*'])],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hangcli=hangcli:router
    ''',
)
