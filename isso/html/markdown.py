from abc import ABC, abstractmethod


class Markdown(ABC):
    @property
    @abstractmethod
    def markdown(self):
        pass

    def render(self, text):
        rv = self.markdown(text).rstrip("\n")
        if rv.startswith("<p>") or rv.endswith("</p>"):
            return rv
        return "<p>" + rv + "</p>"
