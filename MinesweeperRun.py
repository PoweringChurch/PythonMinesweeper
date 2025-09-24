import pygame
from MinesweeperMain import Board, GenClassicCellmap

# --- Config ---
CELL_SIZE = 40
PADDING = 1
FONT_SIZE = 40
UI_FONT_SIZE = 22

# --- Colors ---
PADDING_COLOR = (30, 30, 30)

HIDDEN_COLOR1 = (70, 180, 70)
HIDDEN_COLOR2 = (90, 200, 90)

REVEALED_COLOR = (200, 200, 200)
MINE_COLOR = (200, 20, 20)
FLAG_COLOR = (255,50,50)
TEXT_COLOR = (0, 0, 0)

screenAdjusty = 50
screenAdjustx = 640
def draw_board(screen:pygame.Surface, board:Board, font:pygame.font):
    totalBoardLength = board.Size.x * CELL_SIZE
    halfscreenX = screen.get_size()[0]/2

    for y in range(int(board.Size.y)):
        for x in range(int(board.Size.x)):
            centerAdjustment = halfscreenX-(totalBoardLength/2)
            cell = board.Cellmap[y][x]
            px = x * CELL_SIZE
            py = y * CELL_SIZE
            rect = pygame.Rect(px+ centerAdjustment, py + screenAdjusty, CELL_SIZE - PADDING, CELL_SIZE - PADDING)
            if not cell.Revealed:
                if (x+1*y+1)%2 == 0:
                    pygame.draw.rect(screen, HIDDEN_COLOR1, rect)
                else:
                    pygame.draw.rect(screen, HIDDEN_COLOR2, rect)
                if cell.Flagged:
                    pygame.draw.rect(screen, FLAG_COLOR, rect)
            else:
                if cell.Value == 9:
                    pygame.draw.rect(screen, MINE_COLOR, rect)
                else:
                    pygame.draw.rect(screen, REVEALED_COLOR, rect)
                    if cell.Value > 0:
                        text = font.render(str(cell.Value), True, TEXT_COLOR)
                        screen.blit(text, (px + 10+centerAdjustment, py + 5 + screenAdjusty))

OVERLAY_COLOR = (150,150,150)
def draw_difficultyPresets(screen: pygame.Surface, board, font: pygame.font.Font):
    #width = int(board.Size.x * CELL_SIZE)
    overlay_rect = pygame.Rect(0, 0, 1280, 40)
    pygame.draw.rect(screen, OVERLAY_COLOR, overlay_rect)

    # Define buttons
    difficulties = ['Beginner', 'Intermediate', 'Expert', 'Master','Elite']
    spacing = 5
    button_width = 120
    button_height = 30
    buttons = {}
    for i, label in enumerate(difficulties):
        rect = pygame.Rect(spacing + i * (button_width + spacing), 5, button_width, button_height)
        buttons[label] = rect
        pygame.draw.rect(screen, (180, 180, 180), rect)
        text = font.render(label, True, (0, 0, 0))
        screen.blit(text, (rect.x + 10, rect.y + 5))
    return buttons 

def draw_toggles(screen: pygame.Surface, board: Board, font: pygame.font.Font, toggles: dict):
    buttons = {}
    spacing = 120
    btnSize = 30
    adjustment = 900
    for i, (label, state) in enumerate(toggles.items()):
        rect = pygame.Rect(spacing + i * (btnSize + spacing) + adjustment, 5, btnSize, btnSize)
        buttons[label] = rect
        # Color depends on toggle state
        color = (0, 255, 0) if state else (255, 0, 0)
        pygame.draw.rect(screen, color, rect)

        text = font.render(label, True, (0, 0, 0))
        screen.blit(text, (rect.left - rect.size[0]*3, rect.y + 5))
    return buttons
def overlay_attemptcounter(screen: pygame.Surface, font: pygame.font.Font, attempts: int, board):
    boardpx = board.Size.x * CELL_SIZE
    boardpy = board.Size.y * CELL_SIZE

    # get the full screen dimensions
    screen_width, screen_height = screen.get_size()

    # create overlay rect centered on the screen
    overlayrect = pygame.Rect(0, 0, boardpx, boardpy)
    overlayrect.center = (screen_width // 2, 0)
    overlayrect.top = screenAdjusty

    pygame.draw.rect(screen, OVERLAY_COLOR, overlayrect)

    # render and center the text in the overlay rect
    textstr = f"safe start attempt {str(attempts)}"
    text = font.render(textstr, True, (255, 255, 255))
    text_rect = text.get_rect(center=overlayrect.center)

    screen.blit(text, text_rect)

def get_cell_from_mouse(pos,board):
    mx, my = pos
    my_adjusted = my - screenAdjusty
    mx_adjusted = mx - 640+(board.Size.x*CELL_SIZE)/2
    if my_adjusted < 0:
        return None  # Clicked in the overlay
    return int(my_adjusted // CELL_SIZE), int(mx_adjusted // CELL_SIZE)

def flag(board):
    result = get_cell_from_mouse(pygame.mouse.get_pos(),board)
    if result is None:
        return
    row, col = result
    board.Flag(pygame.Vector2(row, col))

def main():
    pygame.init()
    board = Board(9, 9, 1)
    board.Cellmap = GenClassicCellmap(board)
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Minesweeper")
    font = pygame.font.SysFont(None, FONT_SIZE)
    uifont = pygame.font.SysFont(None,UI_FONT_SIZE)
    running = True
    firstclick = True

    difficulty_presets = {
    'Beginner': Board(9, 9, 10),
    'Intermediate': Board(16, 16, 40),
    'Expert': Board(30, 16, 99),
    'Master': Board(30,16,130),
    'Elite': Board(30,16,199),
    }
    toggles = {
    "SafeStart": True,
    "LossReveal": True
    }
    while running:
        screen.fill(PADDING_COLOR)
        draw_board(screen, board, font)
        presetBtns = draw_difficultyPresets(screen,board,uifont)
        toggleBtns = draw_toggles(screen,board,uifont,toggles)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #handles clicking on difficulty buttons
                    for label, rect in presetBtns.items():
                        if rect.collidepoint(event.pos):
                            board = difficulty_presets[label]
                            board.Cellmap = GenClassicCellmap(board)
                            firstclick = True
                            break
                    #handles clicking on toggles
                    for label, rect in toggleBtns.items():
                        if rect.collidepoint(event.pos):
                            toggles[label] = not toggles[label]
                    #handle clicking on board
                    result = get_cell_from_mouse(event.pos,board)
                    if result is None:
                        continue
                    row, col = result
                    if firstclick and toggles['SafeStart']:
                        max_attempts = 2000
                        attempts = 0
                        while attempts < max_attempts:
                            board.Seed -= 1
                            board.Cellmap = GenClassicCellmap(board)
                            if board.Cellmap[row][col].Value == 0:
                                break
                            attempts += 1
                            overlay_attemptcounter(screen,font,attempts, board)
                            pygame.display.flip()
                        if attempts == max_attempts:
                            print("Failed to generate a safe start. Proceeding anyway.")
                        firstclick = False
                    elif firstclick and not toggles['SafeStart']:
                        firstclick = False
                    board.Reveal(pygame.Vector2(row, col))
                    if board.Cellmap[row][col].Value == 9 and toggles['LossReveal']:
                        board.RevealBoard()
                if event.button == 3:
                    flag(board)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    board.RevealBoard()
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()