
import click
import os
import inflection
import datetime
from jinja2 import Environment, PackageLoader, select_autoescape
import urllib

today = datetime.date.today()

env = Environment(
    loader=PackageLoader('c2dx', 'templates'),
    autoescape=select_autoescape(['cpp', 'h', 'txt'])
)


@click.group()
def cli():
    #print(os.getcwd())
    pass


@cli.command('layer')
@click.option('--class', '-c', 'class_name', prompt='Name of the layer class',
              help="Name of layer class to generate ")
def layer_gen(class_name):
    """Generate Cocos2d-x Layer class"""
    if os.path.isdir("Classes"):
        args = generate_args(class_name, 'h')
        generate_file_from_template('layer.h', "Classes/{0}.h".format(args['f_name']), **args)
        args = generate_args(class_name, 'cpp')
        generate_file_from_template('layer.cpp', "Classes/{0}.cpp".format(args['f_name']), **args)
    else:
        print "Please make sure you are in the cocos2dx project directory"


def generate_args(name, ext='cpp'):
    return {
        'class_name': inflection.camelize(name),
        'f_name': inflection.underscore(name),
        'user_name': os.environ.get('USER', ''),
        'ext': ext,
        'date_time': "{:%d, %b %Y }".format(today)
    }


def generate_file_from_template(template_name, file_name, **kwargs):
    template = env.get_template(template_name)
    target = open(file_name, 'w')
    target.write(template.render(**kwargs))
    print "Generated {0}".format(file_name)

