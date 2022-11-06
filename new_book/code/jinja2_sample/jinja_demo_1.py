from jinja2 import Template

template = Template('Hello {{ name }}!')
tmp = template.render(name='John Doe')
print(tmp)
