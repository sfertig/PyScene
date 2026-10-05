#imports
"PyScene is a custom python + pygame framework / engine developed to streamline 2d game development."
"Version: 1.0.8"

from .Game import Game, Scene, handle_collision
from .Math import *
from .utils.Subscreen import *

from .Keys import *
from .objs import *
from .utils import *


#all
__all__ = [
    "Vector2D",
    "clamp",
    "SubScreen",
    "Game",
    "Scene",
    "Keys",

    "GameObj",
    "Rect",
    "Circle",
    "Line",
    "Text",
    "Image",
    "Timer",

    "Animation",
    "AnimationManager",

    "StaticCollisionRect",
    "DynamicCollisionRect",

    "Assets",
    "handle_collision"
]
