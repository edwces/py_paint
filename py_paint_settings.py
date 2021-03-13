# Grid settings
PAINTABLE_SIZE = 5
ROWS = int(256 * (5 / PAINTABLE_SIZE))
COLUMNS = int(256 * (5 / PAINTABLE_SIZE))
DEFAULT_COLOR = (255, 255, 255)

# GUI settings
GUI_WIDTH = 50
GUI_HEIGHT = ROWS * PAINTABLE_SIZE
GUI_BACKGROUND = (140,140,140)
GUI_BORDER = (120, 120, 120)

BUTTON_WIDTH = 15
BUTTON_HEIGHT = 15
BUTTON_BACKGROUND = (120, 120, 120)

# Window settings
WIDTH = COLUMNS * PAINTABLE_SIZE + GUI_WIDTH
HEIGHT = ROWS * PAINTABLE_SIZE
TITLE = "Py_paint"
FPS = 500

# Colors
BLACK = (0,0,0)
DARK_PURPLE = (75,0,130)
PURPLE = (148,0,211)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
ORANGE = (255,127,0)
RED = (255,0,0)
WHITE = (255,255,255)
COLORS = [BLACK, DARK_PURPLE, PURPLE, BLUE, GREEN, YELLOW, ORANGE, RED, WHITE]

# w jakiej kolejnosci rysuja sie narzedzia
# WAZNE: nazwy narzedi nie moga sie roznic nazwa co do plikow
TOOLS_ORDER = ["brush", "eraser", "color_picker", "paint_bucket", "save", "load"]