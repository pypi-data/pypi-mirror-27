import jinja2
from shutil import copyfile
import os
import sys



def start(params):

    template_vars = params['template_vars']

    template_location = params['templates_dir'] + params['template']

    destination_dir = params['destination_dir'] + '/'

    directories = list()
    files_from_template = list()

    for root, dirs, files in os.walk(template_location):
        for d in dirs:
            directories.append(os.path.join(root,d))
        for f in files:
            if f == params['template'] + '-config.json':
                continue
            fullpath = os.path.join(root,f)
            fullpath = fullpath.replace(template_location, '')
            files_from_template.append(fullpath)

    for d in directories:
        tmp = d.replace(template_location, destination_dir)
        os.makedirs(tmp, exist_ok = True)

    templateLoader = jinja2.FileSystemLoader(searchpath=template_location)
    env = jinja2.Environment(loader = templateLoader)

    for fi in files_from_template:
        t = env.get_template(fi)
        t_rendered = t.render(template_vars)

        with open(destination_dir + fi, 'wb') as f:
            f.write(t_rendered.encode('utf-8'))


