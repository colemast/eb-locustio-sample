import json
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('app', 'templates'))
env.filters['jsonify'] = json.dumps

# Template file at ./app/templates/example.json
template = env.get_template('example.json')

page = {
  'title': 'Jinja Example Page',
	'tags': ['jinja', 'python', 'migration'],
	'description': 'This is an example page created using Jinja2 with a JSON template.'
}

print template.render(page=page)