from setuptools import setup

setup(
    name='hangcli',
    version='0.2.6',
    py_modules=['hangcli'],
    url = "http://blog.coderhelper.cn",
    author = "limhang",
    author_email = "lm_hang@163.com",
    data_files=[('hangcli/react', ['src/react/package.json']),('hangcli/react', ['src/react/.babelrc']), ('hangcli/react', ['src/react/index.html']) ,('hangcli/react', ['src/react/index.js']), ('hangcli/react', ['src/react/webpack.config.js'])],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hangcli=hangcli:router
    ''',
)
