# +---+---+---+---+---+---+---+---+---+
# |   |   |   |   | @ |   |   |   |   |
# +---+---+---+---+---+---+---+---+---+
# |   |   |   |   |   |   |   |   |   |
# +---+---+---+---+---+---+---+---+---+
# |   |   |   |   |   |   |   |   |   |
# +---+---+---+---+---+---+---+---+---+
# |   #   |   |   |   |   |   |   |   |
# +---#---+---+=======+---+---+---+---+
# |   #   |   |   |   |   |   |   |   |
# +---+---+---+---+---+---+---+---+---+
# |   |   |   |   |   |   |   #   |   |
# +---+---+---+---+---+---+---#---+---+
# |   |   |   |   |   #   |   #   |   |
# +---+---+---+---+---#=======+---+---+
# |   #   |   |   |   #   |   |   |   |
# +---#---+---+---+---+---+---+---+---+
# |   #   |   |   | * |   |   |   |   |
# +---+---+---+---+---+---+---+---+---+

# Everything will be drawn left to right so cell content is oriented to be drawn from left to right
BORDER_HORIZONTAL = "+"
BORDER_VERTICAL = "|"
BORDER_BOTTOM = "+---"
BORDER_COLUMNS = "\n   a   b   c   d   e   f   g   h   i    \n "
# No top as each cell draws above it and to the left of it

# Horizontal cell (rows with '+')
CELL_HORIZONTAL = "+---"
CELL_HORIZONTAL_EDGE = "---"
CELL_HORIZONTAL_EDGE_WALLED = "==="
CELL_HORIZONTAL_WALLED = "+==="
CELL_HORIZONTAL_WALLED_CONNECTED = "===="
CELL_HORIZONTAL_WALLED_INTERSECTION = "#==="
CELL_HORIZONTAL_INTERSECTION = "#---"

# Vertical cells (rows with '|')
CELL_VERTICAL = "|   "
CELL_VERTICAL_EDGE = "   "
CELL_VERTICAL_WALLED = "#   "

# Cells with pawns
CELL_VERTICAL_PAWN_WHITE = "| * "
CELL_VERTICAL_EDGE_PAWN_WHITE = " * "
CELL_VERTICAL_WALLED_PAWN_WHITE = "# * "

CELL_VERTICAL_PAWN_BLACK = "| @ "
CELL_VERTICAL_EDGE_PAWN_BLACK = " @ "
CELL_VERTICAL_WALLED_PAWN_BLACK = "# @ "

# Pawns
PAWN_WHITE = "*"
PAWN_BLACK = "@"