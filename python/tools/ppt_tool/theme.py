
from pptx.dml.color import RGBColor
from pydantic import BaseModel
from typing import Tuple

class ThemeColors(BaseModel):
    background: Tuple[int, int, int]
    title: Tuple[int, int, int]
    text: Tuple[int, int, int]
    accent: Tuple[int, int, int]

class ThemeSettings(BaseModel):
    name: str
    colors: ThemeColors
    font_name: str = "Arial"

THEMES = {
    "default": ThemeSettings(
        name="default",
        colors=ThemeColors(
            background=(255, 255, 255),
            title=(0, 0, 0),
            text=(50, 50, 50),
            accent=(0, 100, 200)
        )
    ),
    "corporate-blue": ThemeSettings(
        name="corporate-blue",
        colors=ThemeColors(
            background=(240, 248, 255),  # AliceBlue
            title=(0, 51, 102),          # Dark Blue
            text=(20, 20, 20),
            accent=(0, 120, 215)
        ),
        font_name="Calibri"
    ),
    "cyber-dark": ThemeSettings(
        name="cyber-dark",
        colors=ThemeColors(
            background=(20, 20, 30),     # Dark Navy/Black
            title=(0, 255, 255),         # Cyan Neon
            text=(230, 230, 230),        # Off-white
            accent=(255, 0, 128)         # Hot Pink
        ),
        font_name="Verdana"
    )
}

def get_theme(name: str) -> ThemeSettings:
    return THEMES.get(name, THEMES["default"])
