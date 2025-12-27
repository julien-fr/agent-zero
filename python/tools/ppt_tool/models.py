
from pydantic import BaseModel, Field
from typing import List, Optional, Union, Literal

class SlideBase(BaseModel):
    type: str

class TitleSlide(SlideBase):
    type: Literal['title']
    content: str
    subcontent: Optional[str] = None

class BulletSlide(SlideBase):
    type: Literal['bullet']
    title: str
    bullets: List[str]

class QuoteSlide(SlideBase):
    type: Literal['quote']
    text: str
    author: Optional[str] = None

class ImageSlide(SlideBase):
    type: Literal['image']
    title: Optional[str] = None
    path: str
    caption: Optional[str] = None

class ChartSeries(BaseModel):
    name: str
    values: List[float]

class ChartSlide(SlideBase):
    type: Literal['chart']
    title: str
    chart_type: Literal['BAR_CLUSTERED', 'LINE', 'PIE']
    categories: List[str]
    series: List[ChartSeries]

from typing import Annotated

class PresentationModel(BaseModel):
    title: str
    author: Optional[str] = None
    theme: str = 'default'
    template_path: Optional[str] = None
    slides: List[Annotated[Union[TitleSlide, BulletSlide, QuoteSlide, ImageSlide, ChartSlide], Field(discriminator='type')]]
