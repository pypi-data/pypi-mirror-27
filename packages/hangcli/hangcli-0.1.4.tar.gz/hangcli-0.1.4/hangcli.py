import click
import os
import json
from shutil import copyfile
from pkg_resources import resource_string

@click.command()
@click.option('--project', default='demo', help='input the project name default demo')
@click.argument('operate')
def router(operate, project):
	if operate == "react":
		foo_config = resource_string(__name__, 'hangcli/package.json')
		# foo_config = resource_string(__name__)
		print(foo_config)
		# react(project)
	else:
		print("input the operate")


def react(project):
	reactSrcJsonPath = os.getcwd() + '/' + 'src' + '/' + 'react' + '/' + 'package.json'
	reactSrcWebpackConfigPath = os.getcwd() + '/' + 'src' + '/' + 'react' + '/' + 'webpack.config.js'
	print(reactSrcJsonPath)
	print(reactSrcWebpackConfigPath)

	# 通过输入的project名字，修改package.json中的项目名称
	with open(reactSrcJsonPath, "r+") as jsonFile:
	    data = json.load(jsonFile)
	    data["name"] = project
	    jsonFile.seek(0)  # rewind
	    json.dump(data, jsonFile)
	    jsonFile.truncate()
	os.mkdir(project)
	copyfile(reactSrcJsonPath, os.getcwd()+ '/'+ project + '/' + 'package.json')
	




if __name__ == '__main__':
    router()
