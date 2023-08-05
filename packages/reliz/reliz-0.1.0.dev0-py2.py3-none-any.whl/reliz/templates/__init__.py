from jinja2 import Environment, PackageLoader


def render_template(template, filename, **ctx):
    '''
    Render a template from mastic aplication.
    '''
    env = Environment(
        loader=PackageLoader('reliz', 'templates'),
    )
    template = env.get_template(template)
    with open(filename, 'w') as out:
        data = template.render(**ctx)
        out.write(data)
