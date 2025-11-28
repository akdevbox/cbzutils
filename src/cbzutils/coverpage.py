import tempfile
from pathlib import Path
from typing import Union

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .source import Source

default_font_path = Path(__file__).parent / "fonts" / "opensans.ttf"

type ColorType = Union[tuple[int, int, int, int], tuple[int, int, int], str]


class CoverPage(Source):
    """
    A coverpage class that subclasses the Source abstract class.
    This is a wrapper over generate_coverpage function that can be
    directly appended to a writer object.
    """

    def __init__(self, title: str, subtitle: str, background: str = None):
        self.title = title
        self.subtitle = subtitle
        self.background = background
        self._tempfile = None

    def __len__(self):
        return 1

    def __getitem__(self, idx: int) -> Path:
        """
        Auto generates the cover when index is set to 0. Raises IndexError
        otherwise.
        """
        if idx != 0:
            raise IndexError(
                f"No such page as index {idx}, Cover page only supports one page at index 0"
            )

        if self._tempfile is not None:
            return self._tempfile.name

        # Generate the cover page if it does not exist
        self._tempfile = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        generate_coverpage(self.title, self.subtitle, self.background).save(
            self._tempfile, "PNG"
        )
        self._tempfile.close()
        return Path(self._tempfile.name)

    def __del__(self):
        if self._tempfile is not None:
            Path(self._tempfile.name).unlink(missing_ok=True)


def generate_coverpage(
    title: str, subtitle: str, background: str = None
) -> Image.Image:
    """
    Generates a cover page with the given background image.
    If no image is provided, takes a white background.
    """
    if background is None:
        img = Image.new("RGB", (2000, 2828), (255, 255, 255))
    else:
        img = Image.open(background)
        img = img.resize(_resize_size(img, 2000, -1))

    # Get the text ready
    t1_img = _render_text(title, 200, str(default_font_path))
    t2_img = _render_text(subtitle, 150, str(default_font_path))
    margin_height = int(0.02 * img.height)

    text_width_max = int(img.width * 0.9)
    if t1_img.width > text_width_max:
        t1_img = t1_img.resize(_resize_size(t1_img, text_width_max, -1))
    if t2_img.width > text_width_max:
        t2_img = t2_img.resize(_resize_size(t2_img, text_width_max, -1))

    combined_text = Image.new(
        "RGBA",
        (
            max(t1_img.width, t2_img.width),
            t1_img.height + t2_img.height + margin_height,
        ),
        (0, 0, 0, 0),
    )
    combined_text.paste(t1_img, (0, 0))
    combined_text.paste(t2_img, (0, t1_img.height + margin_height))

    # Blur the background, draw a translucent rectangle and write the text
    img = img.filter(ImageFilter.GaussianBlur(radius=20))
    img = _draw_center_rect(
        img,
        combined_text.width + 0.05 * img.width,
        combined_text.height + 0.05 * img.height,
        220,
    )
    img = _paste_center(img, combined_text)

    return img


def _resize_size(img: Image.Image, width: int, height: int) -> tuple[int, int]:
    """
    Auto calculates the other dimension based on one dimension being provided. aspect ratio is taken from the given img.
    """
    aspect_ratio = img.width / img.height
    if width <= 0:
        width = int(height * aspect_ratio)
    elif height <= 0:
        height = int(width / aspect_ratio)
    return (width, height)


FILL_COLOR = (0, 0, 0)


# LLM generated
def _draw_center_rect(
    img: Image.Image, width: int, height: int, opacity: int = 220
) -> Image.Image:
    """
    Draws a semi-transparent rectangle centered on `img`.

    width, height = rectangle size in px
    opacity = 0–255 (128 = ~50%)
    """

    # Ensure the image is RGBA so alpha works
    base = img.convert("RGBA")

    # Transparent overlay
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    cx, cy = base.size[0] // 2, base.size[1] // 2

    left = cx - width // 2
    top = cy - height // 2
    right = cx + width // 2
    bottom = cy + height // 2

    draw.rectangle([left, top, right, bottom], fill=(*FILL_COLOR, opacity))

    return Image.alpha_composite(base, overlay)


def _paste_center(img_base: Image.Image, img_overlay: Image.Image) -> Image.Image:
    """
    Pastes `img_overlay` onto the center of `img_base`.
    Keeps transparency and works for RGBA overlays.
    """

    base = img_base.convert("RGBA")
    overlay = img_overlay.convert("RGBA")

    bw, bh = base.size
    ow, oh = overlay.size

    # Center position
    x = (bw - ow) // 2
    y = (bh - oh) // 2

    # Transparent layer to composite on
    tmp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    tmp.paste(overlay, (x, y), overlay)

    return Image.alpha_composite(base, tmp)


def _render_text(
    text: str,
    font_size: int,
    font_path: str,
    fill: ColorType = "white",
) -> Image.Image:
    """
    Renders text and returns it as an Image.
    """

    # ---------- Try shrinking single-line ----------
    font = ImageFont.truetype(font_path, font_size)

    l, t, r, b = font.getbbox(text)
    w = r - l
    h = b - t

    im = Image.new("RGBA", (w + 10, h + 10), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    draw.text((-l + 5, -t + 5), text, fill=fill, font=font)

    return im
