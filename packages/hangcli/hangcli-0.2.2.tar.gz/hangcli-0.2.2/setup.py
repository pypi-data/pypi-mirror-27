from setuptools import setup

setup(
    name='hangcli',
    version='0.2.2',
    py_modules=['hangcli'],
    url = "http://blog.coderhelper.cn",
    author = "limhang",
    author_email = "lm_hang@163.com",
    data_files=[('hangcli/react/package.json', ['src/react/package.json']),('hangcli/react/.babelrc', ['src/react/.babelrc']), ('hangcli/react/index.html', ['src/react/index.html']) ,('hangcli/react/index.js', ['src/react/index.js']), ('hangcli/react/webpack.config.js', ['src/react/webpack.config.js'])],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hangcli=hangcli:router
    ''',
)
