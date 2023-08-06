import click
import os
import json
from shutil import copyfile


@click.command()
@click.option('--project', default='demo', help='input the project name default demo')
@click.argument('operate')
def router(operate, project):
	if operate == "react":
		react(project)
	else:
		print("input the operate")


def react(project):
	# 这里所写的/usr/local为包的src文件安装的路径，其中hangcli为setup中设置的
	reactSrcJsonPath = '/usr/local/hangcli/react/package.json'
	reactSrcWebpackconfig = '/usr/local/hangcli/react/webpack.config.js'
	babelRc = '/usr/local/hangcli/react/.babelrc'
	indexJS = '/usr/local/hangcli/react/index.js'
	indexHtml = '/usr/local/hangcli/react/index.html'
	# 修改package.json中项目的名称
	with open(reactSrcJsonPath, "r+") as jsonFile:
	    data = json.load(jsonFile)
	    data["name"] = project
	    jsonFile.seek(0)  # rewind
	    json.dump(data, jsonFile)
	    jsonFile.truncate()
	# 新建一个文件夹，命名为项目名字
	os.mkdir(project)
	# 将修改后的package.json文件放入到新建文件夹中
	copyfile(reactSrcJsonPath, os.getcwd()+ '/'+ project + '/' + 'package.json')
	# 将webpack.config.js放入新建文件夹中
	copyfile(reactSrcWebpackconfig, os.getcwd()+ '/'+ project + '/' + 'webpack.config.js')
	# 将.babelrc放入到新建文件夹中
	copyfile(babelRc, os.getcwd()+ '/'+ project + '/' + '.babelrc')
	# 将index.js放入到src/index.js中，其中src我们需要新建 -- 我们需要先建立src文件夹
	os.chdir(os.getcwd()+ '/'+ project)
	os.makedirs('src')
	copyfile(indexJS, os.getcwd() + '/' + 'src' + '/' + 'index.js')
	# 将index.html放入到dist/index.html中，其中dist我们需要新建 -- 我们需要先建立dist文件夹
	os.makedirs('dist')
	copyfile(indexHtml, os.getcwd() + '/' + 'dist' + '/' + 'index.html')



if __name__ == '__main__':
    router()
