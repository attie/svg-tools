# SVG Tools

Basic tools to manipulate SVG paths...

I needed to create a TTF font, and their axes run from zero at the baseline (bottom-ish, left), whereas a standard SVG canvas starts with zero at the top left.

Scaling by (1,-1) and translating the path resolveds this issue.

## Usage

It's not really ready for use yet, but here's a starter:

```bash
virtualenv -p python3.6 venv
. venv/bin/activate
pip install -r requirements.txt
```
