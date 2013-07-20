import os
import errno
from jinja2 import Template

def mkdir_p(*path):
    """emulate unix `mkdir -p` command"""
    try:
        os.makedirs(os.path.sep.join(path))
    except OSError, e:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise

def touch(*path):
    """emulate unix `touch` command"""
    name = os.path.sep.join(path)
    with file(name, 'a'):
        os.utime(name, None)

def blueprint_template(name, templates):
    """create the basic blueprint"""
    mkdir_p("blueprints", name, templates)
    touch("blueprints", name, "__init__.py")

    input_path = os.path.sep.join(["lib", "blueprint.tpl"])
    output_path = os.path.sep.join(["blueprints", name, "blueprint.py"])
    with open(input_path, "r") as reader:
        template = Template(reader.read())
        with open(output_path, "w") as writer:
            writer.write(template.render(name=name, templates=templates))

    input_path = os.path.sep.join(["lib", "template.tpl"])
    output_path = os.path.sep.join(["blueprints", name, templates, "index.html"])
    with open(input_path, "r") as reader:
        with open(output_path, "w") as writer:
            writer.write(reader.read())

