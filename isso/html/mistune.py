import mistune

from isso.html.markdown import Markdown


class MistuneMarkdown(Markdown):

    def __init__(self, conf):
        self.plugins = conf.getlist("plugins")
        arguments = conf.getlist("arguments")

        escape = True if 'escape' in arguments else False
        hard_wrap = True if 'hard_wrap' in arguments else False
        self.md = mistune.create_markdown(escape=escape, hard_wrap=hard_wrap, plugins=self.plugins)

    @property
    def _markdown(self):
        return self.md

    def _render(self, text:str) -> str:
        return self.md(text)
