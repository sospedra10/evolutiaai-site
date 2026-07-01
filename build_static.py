import os
import re
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"


def reset_dir(path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def copy_tree(name):
    source = ROOT / name
    target = PUBLIC / name
    if source.exists():
        shutil.copytree(source, target)


def normalize_html(html):
    html = re.sub(r'href="\s*/\s*"', 'href="/"', html)
    html = re.sub(r'href="\s*/\s*#', 'href="/#', html)
    return html


def url_for(endpoint):
    if endpoint == "index":
        return "/"
    return f"/{endpoint}"


def main():
    reset_dir(PUBLIC)
    copy_tree("static")
    copy_tree("translations")

    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    env.globals["url_for"] = url_for

    html = normalize_html(
        env.get_template("home.html").render(chat_enabled=False)
    )

    (PUBLIC / "index.html").write_text(html, encoding="utf-8")
    (PUBLIC / "404.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
