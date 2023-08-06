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
	# 通过输入的project名字，修改package.json中的项目名称
	reactSrcJsonPath = '/usr/local/hangcli/package.json'
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
