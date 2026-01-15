import unittest
import textwrap

from isso import config
from isso.html.misaka import MisakaMarkdown


class TestHTMLMisaka(unittest.TestCase):

    def test_markdown(self):
        convert = MisakaMarkdown(plugins=())
        examples = [
            ("*Ohai!*", "<p><em>Ohai!</em></p>"),
            ("<em>Hi</em>", "<p><em>Hi</em></p>"),
            ("http://example.org/", '<p>http://example.org/</p>')]

        for (markup, expected) in examples:
            self.assertEqual(convert(markup), expected)

    def test_markdown_plugins(self):
        conf = config.new({
            "markup.misaka": {
                "plugins": "strikethrough, superscript"
            }
        })
        convert = MisakaMarkdown(conf.section('markup.misaka'))
        examples = [
            ("~~strike~~ through", "<p><del>strike</del> through</p>"),
            ("sup^(script)", "<p>sup<sup>script</sup></p>")]

        for (markup, expected) in examples:
            self.assertEqual(convert(markup), expected)

    def test_github_flavoured_markdown(self):
        convert = MisakaMarkdown()

        # without lang
        _in = textwrap.dedent("""\
            Hello, World

            ```
            #!/usr/bin/env python
            print("Hello, World")""")
        _out = textwrap.dedent("""\
            <p>Hello, World</p>
            <pre><code>#!/usr/bin/env python
            print("Hello, World")
            </code></pre>""")

        self.assertEqual(convert(_in), _out)

        # w/ lang
        _in = textwrap.dedent("""\
            Hello, World

            ```python
            #!/usr/bin/env python
            print("Hello, World")""")
        _out = textwrap.dedent("""\
            <p>Hello, World</p>
            <pre><code class="python">#!/usr/bin/env python
            print("Hello, World")
            </code></pre>""")

    def test_render(self):
        conf = config.new({
            "markup": {
                "options": "autolink",
                "flags": "",
                "allowed-elements": "",
                "allowed-attributes": ""
            }
        })
        renderer = MisakaMarkdown(conf.section("markup")).render
        self.assertIn(renderer("http://example.org/ and sms:+1234567890"),
                      ['<p><a href="http://example.org/" rel="nofollow noopener">http://example.org/</a> and sms:+1234567890</p>',
                       '<p><a rel="nofollow noopener" href="http://example.org/">http://example.org/</a> and sms:+1234567890</p>'])

    def test_sanitized_render_extensions(self):
        """Options should be normalized from both dashed-case or snake_case (legacy)"""
        conf = config.new({
            "markup": {
                "options": "no_intra_emphasis",  # Deliberately snake_case
                "flags": "",
                "allowed-elements": "",
                "allowed-attributes": ""
            }
        })
        renderer = MisakaMarkdown(conf.section("markup")).render
        self.assertEqual(renderer("foo_bar_baz"), '<p>foo_bar_baz</p>')

        conf.set("markup", "options", "no-intra-emphasis")  # dashed-case
        renderer = MisakaMarkdown(conf.section("markup")).render
        self.assertEqual(renderer("foo_bar_baz"), '<p>foo_bar_baz</p>')

    def test_code_blocks(self):
        convert = MisakaMarkdown()
        examples = [
            ("```\nThis is a code-fence. <hello>\n```", "<p><pre><code>This is a code-fence. &lt;hello&gt;\n</code></pre></p>"),
            ("```cpp\nThis is a code-fence. <hello>\n```", "<p><pre><code class=\"language-cpp\">This is a code-fence. &lt;hello&gt;\n</code></pre></p>"),
            ("    This is a four-character indent. <hello>", "<p><pre><code>This is a four-character indent. &lt;hello&gt;\n</code></pre></p>")]

        for (markup, expected) in examples:
            self.assertEqual(convert.render(markup), expected)
