import typing
import jinja2

template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("prompts")
)

class SparkProfile:

    def get_prompt(self, name: str, *args: typing.Any, **kwargs: typing.Any):
        template = template_env.get_template(f"{name}.j2")
        return template.render(*args, **kwargs)

