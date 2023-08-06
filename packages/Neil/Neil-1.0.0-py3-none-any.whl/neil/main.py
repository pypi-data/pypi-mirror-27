import click
import os
import sys
import json
import shutil
from neil import neil



def get_templates_dir():
    home = os.path.expanduser('~')
    return home + '/.neil/templates/'
    
def get_template_names():
    templates_dir = get_templates_dir()
    temps = []
    for root, dirs, files in os.walk(templates_dir):
        for d in dirs:
            temps.append(d)
        break

    return temps

@click.group()
def cli():
    """
    Neil, a utility program to generate boilerplate code/text from templates.
    """
    pass


@click.command('list')
def list_templates():
    """
    List all the available templates
    """

    temps = get_template_names()
    if len(temps) == 0:
        click.echo('No templates installed')
        return

    click.echo('Available templates:')
    for d in temps:
        print('- {}'.format(d))


@click.command('add')
@click.argument('src')
def add_new_template(src):
    """
    Add a new template to the program
    """
    bname = os.path.basename(src)
    templates_dir = get_templates_dir()
    shutil.copytree(src, templates_dir + bname)


@click.command('new')
@click.argument('template')
def main(template):
    """
    Create a new project from a template
    """
    templates_dir = get_templates_dir()

    destination_dir = os.getcwd()
    if os.listdir(destination_dir):
        print('Error -- Current directory is not empty!')
        sys.exit(1)

    # Check if the template exists
    valid_template = os.path.isdir(templates_dir + template)
    if not valid_template:
        print('Error -- Template not known')
        sys.exit(1)

    # Check if config file for template exists
    # If true, read it
    conf_file = templates_dir + template + '/' + template + '-config.json'
    config_exists = os.path.exists(conf_file)
    with open(conf_file) as f:
        template_config = json.load(f)

    params = {'template': template}
    params['templates_dir'] = templates_dir
    params['destination_dir'] = destination_dir

    template_vars = {}

    click.echo('#########')
    click.echo('Selected template: {}'.format(template))
    click.echo('#########')

    questions = template_config['questions']

    for q in questions:
        a = input(q['question'] + ': ')
        template_vars[q['param_name']] = a

    params['template_vars'] = template_vars

    click.echo('Starting to generate {}'.format(template))
    neil.start(params)
    click.echo('Generate done.')


cli.add_command(list_templates)
cli.add_command(main)
cli.add_command(add_new_template)
