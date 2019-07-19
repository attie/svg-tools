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

# Example Application

Look at `./example/fixup.py` for an example application... flipping the OSHW logo on the X-axis, and realigning it.

- `logo.svg` - the original, simplified logo
- `logo_font.svg` - `logo.svg` as an SVG font, with the logo in code point `a`
- `logo_font.ttf` - a TrueType font, with the logo upside down...
- `logo_font_fixed.svg` - `logo_font.svg` after running `fixup.py`
- `logo_font_fixed.ttf` - a TrueType font with, the logo the correct way up!

Use `svg2ttf` to re-create the fonts.
