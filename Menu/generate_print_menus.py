from __future__ import annotations

import argparse
from io import BytesIO
from pathlib import Path
import shutil

from PIL import Image, ImageOps
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
PHOTO_DIR = ROOT / "img-print"
OUTPUT_DIR = PROJECT_ROOT / "output" / "pdf"

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 28

PAPER = HexColor("#FFF8EA")
CARD = HexColor("#FFFDF8")
INK = HexColor("#171717")
MUTED = HexColor("#5B5B5B")
YELLOW = HexColor("#F5C400")
BLUE = HexColor("#1457A8")
RED = HexColor("#C9252D")
LINE = HexColor("#D8D0C4")
PALE_YELLOW = HexColor("#FFF1B8")
PALE_BLUE = HexColor("#E8F1FC")
PALE_RED = HexColor("#FBE9E6")

FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"


def register_fonts() -> None:
    global FONT_REGULAR, FONT_BOLD
    regular = Path("C:/Windows/Fonts/arial.ttf")
    bold = Path("C:/Windows/Fonts/arialbd.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("LCF-Regular", str(regular)))
        pdfmetrics.registerFont(TTFont("LCF-Bold", str(bold)))
        FONT_REGULAR = "LCF-Regular"
        FONT_BOLD = "LCF-Bold"


register_fonts()


MAIN_DISHES = [
    {
        "name": "Picada Colombiana",
        "price": "Small $23 | Large $31",
        "description": "Our house special: yellow and white potatoes, chorizo, chicken, pork ribs, corn, crispy pork belly, and ripe plantains.",
        "image": "Picada.jpg",
    },
    {
        "name": "Frijolada",
        "price": "$20",
        "description": "Hearty Colombian beans with rice, sausage, ripe plantain, and avocado.",
        "image": "Cazuela.jpg",
    },
    {
        "name": "Arroz Paisa",
        "price": "$20",
        "description": "Colombian-style rice with sausage, pork ribs, chicken, corn, ripe plantain, and bacon.",
        "image": "ArrozPaisa.jpg",
    },
    {
        "name": "Arroz con Pollo",
        "price": "$20",
        "description": "Seasoned rice with shredded chicken, bell pepper, onion, carrot, peas, and corn.",
        "image": "ArrozConPollo.jpg",
    },
]

SOUPS = [
    {
        "name": "Ajiaco",
        "price": "$20",
        "description": "Chicken-and-potato soup with corn, scallions, cream, and capers, served with avocado and rice.",
        "image": "Ajiaco.jpg",
    },
    {
        "name": "Sancocho",
        "price": "$20",
        "description": "Colombian soup with chicken, pork rib, yellow and white potatoes, cassava, and corn.",
        "image": "Sancocho.jpg",
    },
]

BROTHS = [
    {
        "name": "Caldo de Costilla",
        "price": "$16",
        "description": "Traditional beef rib broth with white potatoes, scallions, and cilantro.",
        "image": "CaldoDeCostilla.jpg",
    },
    {
        "name": "Caldo de Pollo",
        "price": "$16",
        "description": "Traditional chicken broth with a square-cut chicken piece, sliced potatoes, scallions, and cilantro.",
        "image": "CaldoDePollo.jpg",
    },
]

BREAKFAST = [
    {
        "name": "Huevos Pericos",
        "price": "$8",
        "description": "Colombian-style scrambled eggs with tomato and scallions.",
        "image": "HuevosPericos.jpg",
    },
    {
        "name": "Huevos Pericos con Arroz",
        "price": "$10",
        "description": "Scrambled eggs with tomato and scallions, served with white rice.",
        "image": "HuevosPericosConArroz.jpg",
    },
    {
        "name": "Huevos Pericos con Arepa",
        "price": "$12",
        "description": "Scrambled eggs with tomato and scallions, served with a corn arepa.",
        "image": "HuevosPericosConArepa.jpg",
    },
    {
        "name": "2 Arepas con Queso",
        "price": "$5",
        "description": "Two Colombian corn cakes served with cheese.",
        "image": "Arepas.jpg",
    },
    {
        "name": "Chocolate Caliente",
        "price": "$5",
        "description": "Rich Colombian-style hot chocolate.",
        "image": "HotChocolate.jpg",
    },
]

SNACKS = [
    {
        "name": "Papa Rellena",
        "price": "$8",
        "description": "Crispy potato stuffed with seasoned ground beef and egg.",
        "image": "PapaRellenaCarne.jpg",
    },
    {
        "name": "Empanada",
        "price": "$5",
        "description": "Savory meat, rice, egg, and potato filling. Guava and cheese is also available.",
        "image": "Empanadas.jpg",
    },
]

DRINKS = [
    {"name": "Soda", "price": "$1", "description": "Choice of canned soft drink.", "image": "Soda.jpg"},
    {"name": "Agua", "price": "$1", "description": "Bottled water.", "image": "Agua.jpg"},
    {
        "name": "Limonada Natural",
        "price": "12 oz $5",
        "description": "Fresh lime juice, cold water, natural sugar, and ice.",
        "image": "Limonada.jpg",
    },
    {
        "name": "Limonada Cremosa",
        "price": "16 oz $8",
        "description": "Fresh lime juice blended with sweetened condensed milk and ice.",
        "image": "Cremosa.jpg",
    },
    {
        "name": "Jugo de Naranja Natural",
        "price": "12 oz $6",
        "description": "Freshly squeezed orange juice.",
        "image": "Naranja.jpg",
    },
    {
        "name": "Salpicón",
        "price": "16 oz $9",
        "description": "Fresh Colombian fruit mix in a sweet, juicy base.",
        "image": "Salpicon.jpg",
    },
]


IMAGE_CACHE: dict[tuple[str, int, int], tuple[ImageReader, BytesIO]] = {}


def wrap_text(text: str, font_name: str, font_size: float, max_width: float) -> list[str]:
    words = text.split()
    if not words:
        return [""]

    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if pdfmetrics.stringWidth(candidate, font_name, font_size) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def photo_reader(filename: str, width: float, height: float) -> ImageReader:
    pixel_width = max(120, round(width * 2.4))
    pixel_height = max(120, round(height * 2.4))
    key = (filename, pixel_width, pixel_height)
    if key in IMAGE_CACHE:
        return IMAGE_CACHE[key][0]

    source = PHOTO_DIR / filename
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        image = ImageOps.fit(
            image,
            (pixel_width, pixel_height),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5),
        )
        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=84, optimize=True, progressive=False)
        buffer.seek(0)

    reader = ImageReader(buffer)
    IMAGE_CACHE[key] = (reader, buffer)
    return reader


def draw_photo(pdf: canvas.Canvas, filename: str, x: float, y: float, width: float, height: float, radius: float = 5) -> None:
    pdf.saveState()
    path = pdf.beginPath()
    path.roundRect(x, y, width, height, radius)
    pdf.clipPath(path, stroke=0, fill=0)
    pdf.drawImage(photo_reader(filename, width, height), x, y, width=width, height=height, preserveAspectRatio=False, mask=None)
    pdf.restoreState()
    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(0.6)
    pdf.roundRect(x, y, width, height, radius, stroke=1, fill=0)


def draw_logo(pdf: canvas.Canvas, x: float, y: float, size: float) -> None:
    pdf.drawImage(str(PHOTO_DIR / "Logo.jpg"), x, y, width=size, height=size, preserveAspectRatio=False, mask=None)
    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(0.7)
    pdf.rect(x, y, size, size, stroke=1, fill=0)


def draw_placeholder(pdf: canvas.Canvas, label: str, x: float, y: float, width: float, height: float) -> None:
    pdf.setFillColor(BLUE)
    pdf.roundRect(x, y, width, height, 5, stroke=0, fill=1)
    band = width / 3
    for index, color in enumerate((YELLOW, BLUE, RED)):
        pdf.setFillColor(color)
        pdf.rect(x + (index * band), y, band + 0.3, 4, stroke=0, fill=1)
    pdf.setFillColor(white)
    pdf.setFont(FONT_BOLD, 7 if len(label) > 2 else 12)
    pdf.drawCentredString(x + (width / 2), y + (height / 2) - 2.5, label)


def draw_header(pdf: canvas.Canvas, title: str, subtitle: str) -> float:
    pdf.setFillColor(PAPER)
    pdf.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)

    stripe_height = 9
    stripe_width = PAGE_WIDTH / 3
    for index, color in enumerate((YELLOW, BLUE, RED)):
        pdf.setFillColor(color)
        pdf.rect(index * stripe_width, PAGE_HEIGHT - stripe_height, stripe_width + 0.5, stripe_height, stroke=0, fill=1)

    logo_size = 70
    logo_y = PAGE_HEIGHT - 89
    draw_logo(pdf, MARGIN, logo_y, logo_size)

    text_x = MARGIN + logo_size + 15
    pdf.setFillColor(RED)
    pdf.setFont(FONT_BOLD, 8.4)
    pdf.drawString(text_x, PAGE_HEIGHT - 30, "LA COLOMBIANA FOOD")

    pdf.setFillColor(BLUE)
    pdf.setFont(FONT_BOLD, 24)
    pdf.drawString(text_x, PAGE_HEIGHT - 55, title)

    pdf.setFillColor(INK)
    pdf.setFont(FONT_BOLD, 8.7)
    pdf.drawString(text_x, PAGE_HEIGHT - 70, subtitle)

    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_REGULAR, 7.8)
    pdf.drawString(text_x, PAGE_HEIGHT - 83, "+1 406 260 9165  |  @lacolombianafood.truck")

    divider_y = PAGE_HEIGHT - 101
    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(1)
    pdf.line(MARGIN, divider_y, PAGE_WIDTH - MARGIN, divider_y)
    return divider_y - 13


def draw_section_heading(pdf: canvas.Canvas, top: float, title: str, badge: str | None = None, seasonal: bool = False) -> float:
    pdf.setFillColor(BLUE)
    pdf.roundRect(MARGIN, top - 18, 4, 18, 2, stroke=0, fill=1)
    pdf.setFillColor(INK)
    pdf.setFont(FONT_BOLD, 10.8)
    pdf.drawString(MARGIN + 10, top - 13, title)

    if badge:
        badge_size = 6.6
        badge_width = pdfmetrics.stringWidth(badge, FONT_BOLD, badge_size) + 18
        badge_x = PAGE_WIDTH - MARGIN - badge_width
        pdf.setFillColor(PALE_RED if seasonal else PALE_BLUE)
        pdf.setStrokeColor(RED if seasonal else BLUE)
        pdf.roundRect(badge_x, top - 18, badge_width, 17, 6, stroke=1, fill=1)
        pdf.setFillColor(RED if seasonal else BLUE)
        pdf.setFont(FONT_BOLD, badge_size)
        pdf.drawCentredString(badge_x + (badge_width / 2), top - 12, badge)
    return top - 26


def draw_featured_picada(pdf: canvas.Canvas, top: float, item: dict) -> float:
    height = 104
    y = top - height
    width = PAGE_WIDTH - (2 * MARGIN)
    pdf.setFillColor(PALE_YELLOW)
    pdf.setStrokeColor(YELLOW)
    pdf.roundRect(MARGIN, y, width, height, 9, stroke=1, fill=1)

    photo_x = MARGIN + 7
    photo_y = y + 7
    photo_width = 178
    draw_photo(pdf, item["image"], photo_x, photo_y, photo_width, height - 14, radius=6)

    text_x = photo_x + photo_width + 14
    text_width = PAGE_WIDTH - MARGIN - text_x - 10
    pdf.setFillColor(RED)
    pdf.roundRect(text_x, top - 24, 92, 17, 6, stroke=0, fill=1)
    pdf.setFillColor(white)
    pdf.setFont(FONT_BOLD, 7.4)
    pdf.drawCentredString(text_x + 46, top - 18, "HOUSE SPECIAL")

    pdf.setFillColor(INK)
    pdf.setFont(FONT_BOLD, 15)
    pdf.drawString(text_x, top - 44, item["name"])

    pdf.setFillColor(RED)
    pdf.setFont(FONT_BOLD, 11)
    pdf.drawString(text_x, top - 61, item["price"])

    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_REGULAR, 7.3)
    cursor_y = top - 75
    for line in wrap_text(item["description"], FONT_REGULAR, 7.3, text_width)[:3]:
        pdf.drawString(text_x, cursor_y, line)
        cursor_y -= 8.5
    return y - 11


def draw_food_card(pdf: canvas.Canvas, x: float, top: float, width: float, height: float, item: dict) -> None:
    y = top - height
    pdf.setFillColor(CARD)
    pdf.setStrokeColor(LINE)
    pdf.roundRect(x, y, width, height - 2, 6, stroke=1, fill=1)

    photo_size = height - 14
    photo_x = x + 6
    photo_y = y + 6
    if item.get("image"):
        draw_photo(pdf, item["image"], photo_x, photo_y, photo_size, photo_size, radius=5)
    else:
        draw_placeholder(pdf, item.get("placeholder", "FOOD"), photo_x, photo_y, photo_size, photo_size)

    text_x = photo_x + photo_size + 9
    text_width = x + width - text_x - 7
    price = item["price"]
    price_size = 8.2
    price_width = pdfmetrics.stringWidth(price, FONT_BOLD, price_size)
    name_width = max(58, text_width - price_width - 7)
    name_lines = wrap_text(item["name"], FONT_BOLD, 8.1, name_width)

    cursor_y = top - 13
    pdf.setFillColor(INK)
    pdf.setFont(FONT_BOLD, 8.1)
    for line in name_lines[:2]:
        pdf.drawString(text_x, cursor_y, line)
        cursor_y -= 9

    pdf.setFillColor(RED)
    pdf.setFont(FONT_BOLD, price_size)
    pdf.drawRightString(x + width - 7, top - 13, price)

    cursor_y -= 1
    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_REGULAR, 6.55)
    for line in wrap_text(item["description"], FONT_REGULAR, 6.55, text_width)[:3]:
        pdf.drawString(text_x, cursor_y, line)
        cursor_y -= 7.4


def draw_food_section(
    pdf: canvas.Canvas,
    top: float,
    title: str,
    items: list[dict],
    *,
    badge: str | None = None,
    seasonal: bool = False,
    row_height: float = 64,
) -> float:
    cards_top = draw_section_heading(pdf, top, title, badge=badge, seasonal=seasonal)
    gap = 14
    column_width = (PAGE_WIDTH - (2 * MARGIN) - gap) / 2
    rows = (len(items) + 1) // 2
    for index, item in enumerate(items):
        row = index // 2
        column = index % 2
        x = MARGIN + column * (column_width + gap)
        draw_food_card(pdf, x, cards_top - (row * row_height), column_width, row_height, item)
    return cards_top - (rows * row_height) - 10


def draw_drink_card(pdf: canvas.Canvas, x: float, top: float, width: float, height: float, item: dict) -> None:
    y = top - height
    pdf.setFillColor(CARD)
    pdf.setStrokeColor(LINE)
    pdf.roundRect(x, y, width, height - 2, 6, stroke=1, fill=1)

    photo_size = height - 15
    photo_x = x + 6
    photo_y = y + 6
    if item.get("image"):
        draw_photo(pdf, item["image"], photo_x, photo_y, photo_size, photo_size, radius=5)
    else:
        draw_placeholder(pdf, item.get("placeholder", "D"), photo_x, photo_y, photo_size, photo_size)

    text_x = photo_x + photo_size + 7
    text_width = x + width - text_x - 6
    price_width = pdfmetrics.stringWidth(item["price"], FONT_BOLD, 7.2)
    name_width = max(42, text_width - price_width - 5)

    pdf.setFillColor(INK)
    pdf.setFont(FONT_BOLD, 7.1)
    cursor_y = top - 12
    for line in wrap_text(item["name"], FONT_BOLD, 7.1, name_width)[:2]:
        pdf.drawString(text_x, cursor_y, line)
        cursor_y -= 7.8

    pdf.setFillColor(RED)
    pdf.setFont(FONT_BOLD, 7.2)
    pdf.drawRightString(x + width - 6, top - 12, item["price"])

    cursor_y -= 1
    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_REGULAR, 5.8)
    for line in wrap_text(item["description"], FONT_REGULAR, 5.8, text_width)[:2]:
        pdf.drawString(text_x, cursor_y, line)
        cursor_y -= 6.5


def draw_drinks_section(pdf: canvas.Canvas, top: float) -> float:
    cards_top = draw_section_heading(pdf, top, "DRINKS (BEBIDAS)")
    gap = 10
    columns = 3
    column_width = (PAGE_WIDTH - (2 * MARGIN) - (gap * (columns - 1))) / columns
    row_height = 55
    for index, item in enumerate(DRINKS):
        row = index // columns
        column = index % columns
        x = MARGIN + column * (column_width + gap)
        draw_drink_card(pdf, x, cards_top - (row * row_height), column_width, row_height, item)
    return cards_top - (2 * row_height) - 10


def draw_footer(pdf: canvas.Canvas) -> None:
    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_REGULAR, 6.8)
    pdf.drawCentredString(PAGE_WIDTH / 2, 14, "Prices are in USD. Please let us know about any food allergies.")

    stripe_width = PAGE_WIDTH / 3
    for index, color in enumerate((YELLOW, BLUE, RED)):
        pdf.setFillColor(color)
        pdf.rect(index * stripe_width, 0, stripe_width + 0.5, 4, stroke=0, fill=1)


def build_main_menu(path: Path) -> float:
    pdf = canvas.Canvas(str(path), pagesize=A4, pageCompression=1)
    pdf.setTitle("La Colombiana Food - Main Menu")
    top = draw_header(pdf, "MAIN MENU", "MAIN DISHES, SEASONAL SOUPS, SNACKS & DRINKS")
    cursor_y = draw_featured_picada(pdf, top, MAIN_DISHES[0])
    cursor_y = draw_food_section(pdf, cursor_y, "MAIN DISHES (PLATOS PRINCIPALES)", MAIN_DISHES[1:])
    cursor_y = draw_food_section(
        pdf,
        cursor_y,
        "SOUPS (SOPAS)",
        SOUPS,
        badge="UNAVAILABLE DURING SUMMER / NO DISPONIBLES EN VERANO",
        seasonal=True,
    )
    cursor_y = draw_food_section(pdf, cursor_y, "SNACKS (ANTOJITOS)", SNACKS)
    cursor_y = draw_drinks_section(pdf, cursor_y)
    if cursor_y < 28:
        raise RuntimeError(f"Main menu content is too tall: bottom={cursor_y:.1f}")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()
    return cursor_y


def build_breakfast_menu(path: Path) -> float:
    pdf = canvas.Canvas(str(path), pagesize=A4, pageCompression=1)
    pdf.setTitle("La Colombiana Food - Breakfast Menu")
    top = draw_header(pdf, "BREAKFAST MENU", "COLOMBIAN BREAKFAST, AVAILABLE BROTHS, SNACKS & DRINKS")
    cursor_y = draw_food_section(pdf, top, "BREAKFAST (DESAYUNOS)", BREAKFAST)
    cursor_y = draw_food_section(
        pdf,
        cursor_y,
        "BROTHS (CALDOS)",
        BROTHS,
        badge="AVAILABLE WITH BREAKFAST / DISPONIBLES CON DESAYUNO",
    )
    cursor_y = draw_food_section(pdf, cursor_y, "SNACKS (ANTOJITOS)", SNACKS)
    cursor_y = draw_drinks_section(pdf, cursor_y)
    if cursor_y < 28:
        raise RuntimeError(f"Breakfast menu content is too tall: bottom={cursor_y:.1f}")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()
    return cursor_y


def build_selected(menu: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_CACHE.clear()

    if menu == "main":
        output = OUTPUT_DIR / "la-colombiana-main-menu.pdf"
        bottom = build_main_menu(output)
        for destination in (ROOT / "menu-principal.pdf", ROOT / "menu-impresion.pdf"):
            shutil.copy2(output, destination)
        print(f"Created {output} (content bottom: {bottom:.1f})")
        return

    output = OUTPUT_DIR / "la-colombiana-breakfast-menu.pdf"
    bottom = build_breakfast_menu(output)
    shutil.copy2(output, ROOT / "menu-desayunos.pdf")
    print(f"Created {output} (content bottom: {bottom:.1f})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate La Colombiana Food printable menus.")
    parser.add_argument("--menu", choices=("main", "breakfast"), required=True)
    args = parser.parse_args()
    build_selected(args.menu)


if __name__ == "__main__":
    main()
