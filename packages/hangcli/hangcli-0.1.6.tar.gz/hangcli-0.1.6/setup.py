from setuptools import setup

setup(
    name='hangcli',
    version='0.1.6',
    py_modules=['hangcli'],
    url = "http://blog.coderhelper.cn",
    author = "limhang",
    author_email = "lm_hang@163.com",
    data_files=[('hangcli', ['src/react/package.json']),('hangcli', ['src/react/webpack.config.js'])],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hangcli=hangcli:router
    ''',
)
