import mistune

from isso.html.markdown import Markdown


class MistuneMarkdown(Markdown):

    def __init__(self, conf):
        self.plugins = conf.getlist("plugins")
        self.parameters = conf.getlist("parameters")

        self.md = mistune.Markdown(plugins=self.plugins)

    @property
    def markdown(self):
        return self.md
