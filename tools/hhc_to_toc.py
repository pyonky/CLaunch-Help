# hhc_to_toc.py
import argparse
import html
from html.parser import HTMLParser


class HhcParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.events = []
        self.in_sitemap = False
        self.current = None

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs = dict(attrs)

        if tag == "ul":
            self.events.append(("ul_start", None))

        elif tag == "object":
            obj_type = attrs.get("type", "").lower()
            if obj_type == "text/sitemap":
                self.in_sitemap = True
                self.current = {"name": "", "local": ""}

        elif tag == "param" and self.in_sitemap and self.current is not None:
            name = attrs.get("name", "").lower()
            value = attrs.get("value", "")

            if name == "name":
                self.current["name"] = value.strip()
            elif name == "local":
                self.current["local"] = value.strip()

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag == "object" and self.in_sitemap:
            self.events.append(("item", self.current))
            self.in_sitemap = False
            self.current = None

        elif tag == "ul":
            self.events.append(("ul_end", None))


def convert_hhc_to_toc(hhc_text, title="Contents", lang="en"):
    parser = HhcParser()
    parser.feed(hhc_text)

    out = []
    indent = 0
    level = 0
    li_open = []

    def write(s):
        out.append("  " + "  " * indent + s)

    def close_open_li():
        nonlocal indent
        if li_open and li_open[-1]:
            indent -= 1
            write("</li>")
            li_open[-1] = False

    def make_last_li_parent():
        for i in range(len(out) - 1, -1, -1):
            stripped = out[i].lstrip()
            if stripped.startswith("<li>"):
                out[i] = out[i].replace("<li>", '<li class="toc-parent">', 1)
                break

    out.append("<!DOCTYPE html>")
    out.append(f'<html lang="{html.escape(lang, quote=True)}">')
    out.append("<head>")
    out.append('  <meta charset="utf-8">')
    out.append(f"  <title>{html.escape(title)}</title>")
    out.append('  <link rel="stylesheet" href="online.css">')
    out.append("</head>")
    out.append('<body class="toc-page">')
    out.append(f'  <div class="toc-title">{html.escape(title)}</div>')

    for kind, data in parser.events:

        if kind == "ul_start":
            if level > 0 and li_open and li_open[-1]:
                make_last_li_parent()

            if level == 0:
                cls = "toc-root"
            else:
                cls = f"toc-level{level}"

            write(f'<ul class="{cls}">')
            indent += 1
            level += 1
            li_open.append(False)

        elif kind == "ul_end":
            close_open_li()

            li_open.pop()
            level -= 1
            indent -= 1
            write("</ul>")

            if level > 0:
                close_open_li()

        elif kind == "item":
            close_open_li()

            name = html.escape(data.get("name", ""))
            local = data.get("local", "")

            if local:
                href = html.escape(local, quote=True)
                write(f'<li><a href="{href}" target="content">{name}</a>')
            else:
                write(f'<li><span class="toc-section">{name}</span>')

            indent += 1
            li_open[-1] = True

    out.append("</body>")
    out.append("</html>")

    return "\n".join(out) + "\n"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Input .hhc file")
    ap.add_argument("output", help="Output toc.html file")
    ap.add_argument("--title", default="Contents")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--encoding", default="utf-8")
    args = ap.parse_args()

    with open(args.input, "r", encoding=args.encoding) as f:
        hhc_text = f.read()

    toc_html = convert_hhc_to_toc(hhc_text, args.title, args.lang)

    with open(args.output, "w", encoding="utf-8", newline="\n") as f:
        f.write(toc_html)


if __name__ == "__main__":
    main()

