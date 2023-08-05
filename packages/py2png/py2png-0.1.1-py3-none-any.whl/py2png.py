#!/usr/bin/env python3
import click
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import pygments
from pygments.lexers import Python3Lexer
from pygments.formatters import ImageFormatter


@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.argument('output', type=click.Path(exists=False))
@click.option('--highlight/--no-highlight', default=True)
def convert(file, output, highlight):
    """Convert python module into a PNG snapshot."""
    if not highlight:
        no_highlight(file, output)
    else:
        with open(file) as f:
            text = f.read()
        pygments.highlight(
            text,
            Python3Lexer(),
            ImageFormatter(font_name='Courier', line_numbers=False),
            output)


def no_highlight(file, output):
    with open(file) as f:
        text = f.readlines()

    # calculate image dimentions
    image_width = max(len(l) for l in text) * 11
    image_height = (len(text) + 1) * 18

    # draw background
    img = Image.new('RGBA', (image_width, image_height))
    draw = ImageDraw.Draw(img)

    # draw text
    font = ImageFont.truetype("/Library/Fonts/Courier New", 18)
    for n, line in enumerate(text):
        draw.text((0, n * 18), line, (100, 100, 100), font=font)
    img.save(output)


if __name__ == '__main__':
    convert()
