import pygame
import sys, time, random
from pygame.locals import MOUSEMOTION, MOUSEBUTTONUP, QUIT
class Game():
    
    def __init__(self):
        pygame.init()
        infoObject = pygame.display.Info()
        self.screen_width = infoObject.current_w
        self.center = self.screen_width // 2
        self.w = self.screen_width // 100
        display = pygame.display.set_mode((self.screen_width, infoObject.current_h))
        pygame.display.set_caption("Tic Tac Toe Game")
        self.main_bg = "azure2"
        display.fill(self.main_bg)
        self.display = display
        self.font = pygame.font.SysFont("serif", self.screen_width // 10)
        self.custom_font = pygame.font.SysFont("serif", self.screen_width // 12)
        self.is_over = False
        self.blank_board()
        self.depth = 10
        
    def blank_board(self):
        self.board = []
        for _ in range(3):
            self.board.append( [" "] * 3)
            
    def print_board_lines(self):
        size = self.screen_width
        pygame.draw.line(self.display, "black", (0, self.center - self.w // 2), (size, self.center - self.w // 2), self.w) # first row
        pygame.draw.line(self.display, "black", (0, size + self.center + self.w // 2), (size, size + self.center + self.w // 2), self.w) # last row
        for i in range(1,3):
            pygame.draw.line(self.display, "black", (0, (size * i) // 3 + self.center), (size, (size * i) // 3 + self.center), self.w) # Row lines
            pygame.draw.line(self.display, "black", ((size * i) // 3, self.center), ((size * i) // 3, size + self.center), self.w) # Column lines
            
    def place(self, x, y, symbol: bool):
        self.board[y][x] = symbol
        cell_size = self.screen_width // 3
        offset = cell_size // 10
        # Coordinates
        sq_pos = [cell_size * x, cell_size * y]
        top_left = (sq_pos[0] + offset, sq_pos[1] + offset + self.center)
        bottom_right = (sq_pos[0] + cell_size - offset, sq_pos[1] + cell_size - offset + self.center)
        bottom_left = (sq_pos[0] + offset, sq_pos[1] + cell_size - offset + self.center)
        top_right = (sq_pos[0] + cell_size - offset, sq_pos[1] + offset + self.center)
        center = (sq_pos[0] + cell_size // 2, sq_pos[1] + cell_size // 2 + self.center)
        radius = (cell_size - offset) / 2
        
        if symbol: # Place X
            pygame.draw.line(self.display, "red", top_left, bottom_right, self.w)
            pygame.draw.line(self.display, "red", bottom_left, top_right, self.w)
            
        else: # Place O
            pygame.draw.circle(self.display, "blue", center, radius, self.w)
        
    def draw_selecting_text(self):
        text = self.font.render("Select your symbol", True, "black")
        text_rect = text.get_rect(center = (self.center, self.screen_width * 0.65) )
        self.display.blit(text, text_rect)
        
    def draw_buttons(self):
        global button_o, button_x
        screen = self.screen_width
        
        radius = screen // 10
        offset = screen // 30
        left = screen * 0.2
        top = screen * 0.85
        width = screen - 2*left # Center box
        
        box = pygame.Rect(left, top, width, radius*2) # Only for alignment / invisible
        # Drawing O
        pygame.draw.circle(self.display, "blue", (box.x + radius, box.y + radius), radius, self.w)
        # Drawing X
        bottom_right = (box.bottomright[0] - offset // 2, box.bottomright[1] - offset // 2)
        top_left = (box.bottomright[0] + offset // 2 - radius*2, box.bottomright[1] + offset // 2 - radius*2)
        bottom_left = (box.bottomright[0] + offset // 2 - radius*2, box.bottomright[1] - offset // 2)
        top_right = (box.bottomright[0] - offset // 2, box.bottomright[1] + offset // 2 - radius*2)
        pygame.draw.line(self.display, "red", bottom_right, top_left, self.w)
        pygame.draw.line(self.display, "red", bottom_left, top_right, self.w)
        
        button_o = pygame.Rect(left - offset, top - offset, 2*(radius+offset), 2*(radius+offset)) # Button for O
        button_x = pygame.Rect(left + width - 2*radius - offset, top - offset, 2*(radius+offset), 2*(radius+offset)) # Button for X
        pygame.draw.rect(self.display, "black", button_o, self.w, 20)
        pygame.draw.rect(self.display, "black", button_x, self.w, 20)
    
    def AI_level(self):
        global select_button
        text = self.custom_font.render("AI Level", True, "black")
        screen = self.screen_width
        offset = screen // 30
        text_rect = text.get_rect(center = (screen // 2, screen * 1.2 + text.get_height() ))
        self.display.blit(text, text_rect)
        left =  text_rect.left - offset
        top = text_rect.top - offset
        select_button = pygame.Rect(left, top, text.get_width() + 2 * offset, text.get_height() + 2 * offset)
        pygame.draw.rect(self.display, "black", select_button, self.w, 20)
        
    def draw_selection_buttons(self, close_button_bg = "red1"):
        global selecting, easy_button, normal_button, imp_button, close_button
        selecting = True
        screen = self.screen_width
        offset = screen // 30
        close_button_size = offset * 2
        exit_pos = screen - 2*offset - close_button_size
        close_button = pygame.Rect(exit_pos - offset, offset + self.center, 2*offset + close_button_size, 2*offset + close_button_size)
        pygame.draw.rect(self.display, close_button_bg, close_button, 0, 100)
        pygame.draw.line(self.display, "black", (exit_pos, close_button.top + offset + close_button_size), (screen - 2*offset, close_button.top + offset), self.w)
        pygame.draw.line(self.display, "black", (exit_pos, close_button.top + offset), (exit_pos + close_button_size, close_button.top + offset + close_button_size), self.w)
        pygame.draw.rect(self.display, "black", close_button, self.w, 100)
        easy = self.font.render("Easy", False, "black")
        normal = self.font.render("Normal", False, "black")
        imp = self.font.render("Impossible", False, "black")
        height = easy.get_height()
        height_sum = easy.get_height() + normal.get_height() + imp.get_height()
        gap = (screen - height_sum) // 4
        easy_rect = easy.get_rect(center = (self.center, gap + easy.get_height() // 2 + self.center * 1.15))
        normal_rect = normal.get_rect(center = (self.center, 2*gap + easy.get_height() + normal.get_height() // 2 + self.center * 1.15))
        imp_rect = imp.get_rect(center = (self.center, 3*gap + easy.get_height() + normal.get_height() + imp.get_height() // 2 + self.center * 1.15))
        self.display.blit(easy, easy_rect)
        self.display.blit(normal, normal_rect)
        self.display.blit(imp, imp_rect)
        left = lambda x: x.left - offset
        top = lambda x: x.top - offset
        width = lambda x: x.get_width() + 2 * offset
        height = lambda x: x.get_height() + 2 * offset
        easy_button = pygame.Rect(left(easy_rect), top(easy_rect) , width(easy), height(easy))
        normal_button = pygame.Rect(left(normal_rect), top(normal_rect), width(normal), height(normal))
        imp_button = pygame.Rect(left(imp_rect), top(imp_rect), width(imp), height(imp))
        pygame.draw.rect(self.display, self.main_bg, easy_button, self.w + 10, 20)
        pygame.draw.rect(self.display, self.main_bg, normal_button, self.w + 10, 20)
        pygame.draw.rect(self.display, self.main_bg, imp_button, self.w + 10, 20)
        pygame.draw.rect(self.display, "black", easy_button, self.w, 20)
        pygame.draw.rect(self.display, "black", normal_button, self.w, 20)
        pygame.draw.rect(self.display, "black", imp_button, self.w, 20)
        match self.depth:
            case 0:
                pygame.draw.rect(self.display, "darkorchid", easy_button, self.w + 10, 20)
            case 1:
                pygame.draw.rect(self.display, "darkorchid", normal_button, self.w + 10, 20)
            case 10:
                pygame.draw.rect(self.display, "darkorchid", imp_button, self.w + 10, 20)
        pygame.display.update()
        
    def play(self):
        global run, selecting
        run, selecting = False, False
        
        self.AI_level()
        self.draw_buttons()
        self.draw_selecting_text()
        
        while not run: # Starting screen
            pygame.time.delay(10)
            for event in pygame.event.get():
                self.handle_events(event)
                pygame.display.update()
        
        # Player selected symbol
        self.display.fill(self.main_bg)
        self.print_board_lines()
        self.move = 0
        self.turn = self.player
        # Game started
        while run:
            pygame.display.update()
            pygame.time.delay(10)
            # Player plays
            for event in pygame.event.get():
                self.handle_events(event)
                pygame.display.update()
                
            if self.game_over()[0]:
                run = False
                time.sleep(1)
            # Computer plays
            if not self.turn and run:
                best_move = self.find_best_move(not self.player)
                self.place(best_move[0], best_move[1], not self.player)
                pygame.display.update()
                #print("played",best_move)
                if self.game_over()[0]:
                    run = False
                    time.sleep(1)
                self.turn = True
            
            # Game Over
            if not run:
                self.is_over = True
                match self.game_over()[1]:
                    case "draw":
                        self.display.fill(self.main_bg)
                        text = self.font.render("Draw!", True, "black")
                        text_rect = text.get_rect(center = (self.center, self.screen_width * 0.8) )
                        self.display.blit(text, text_rect)
                    case "player":
                        self.display.fill(self.main_bg)
                        text = self.font.render("Player wins!", True, "black")
                        text_rect = text.get_rect(center = (self.center, self.screen_width * 0.8) )
                        self.display.blit(text, text_rect)
                    case "computer":
                        self.display.fill(self.main_bg)
                        text = self.font.render("Computer wins!", True, "black")
                        text_rect = text.get_rect(center = (self.center, self.screen_width * 0.8) )
                        self.display.blit(text, text_rect)
                self.draw_restart_button()
                pygame.display.update()
                # Loop for player to press restart
                while True:
                    for event in pygame.event.get():
                        self.handle_events(event)
                        pygame.display.update()
                        
    def draw_line(self, player, row = None, col = None, diagonal = None):
        color = "red" if player else "blue"
        cell_size = self.screen_width // 3
        offset = cell_size // 4
        screen = self.screen_width
        if row != None:
            left = (offset, cell_size // 2 + row * cell_size + self.center)
            right = (screen - offset, cell_size // 2 + row * cell_size + self.center)
            pygame.draw.line(self.display, color, left, right, self.w + 10)
            
        if col != None:
            top = (cell_size // 2 + col * cell_size, offset + self.center)
            bottom = (cell_size // 2 + col * cell_size, screen-offset + self.center)
            pygame.draw.line(self.display, color, top, bottom, self.w + 10)
            
        if diagonal != None:
            if all([self.board[i][i] == player for i in range(3)]):
                pygame.draw.line(self.display, color, (offset, offset + self.center), (screen - offset, screen - offset + self.center), self.w + 10)
            else:
                pygame.draw.line(self.display, color, (offset, screen - offset + self.center), (screen - offset, offset + self.center), self.w + 10)
                
        pygame.display.update()
            
    def draw_restart_button(self):
        global res_button
        restart_text = self.font.render("Restart", True, "black")
        restart_rect = restart_text.get_rect(center = (self.center, self.screen_width * 1.1)) # Only for alignment / invisible
        self.display.blit(restart_text, restart_rect)
        res_button = restart_text.get_rect(width = 2*restart_text.get_width(), height = 1.5*restart_text.get_height(), center = restart_rect.center)
        pygame.draw.rect(self.display, "black", res_button, self.w, 20)
        
    def game_over(self):
        if self.check_winner(self.player)[0]:
            info = self.check_winner(self.player)
            self.draw_line(self.player, row=info[1], col=info[2], diagonal=info[3])
            return (True,"player")
        
        if self.check_winner(not self.player)[0]:
            info = self.check_winner(not self.player)
            self.draw_line(not self.player, row=info[1], col=info[2], diagonal=info[3])
            return (True, "computer")
        
        if len(self.avaliable_moves()) == 0:
            return (True, "draw")
        
        return (False, None)
    
    def handle_events(self,event):
        global run, selecting
        cell_size = self.screen_width // 3
        pos = pygame.mouse.get_pos()
        x = pos[0] // cell_size
        y = (pos[1] - self.center) // cell_size
        offset = 3
        box_size = cell_size - self.w
        margin = lambda x: (cell_size + 2) * x + offset
        bg_color = "gold"
        
        # Hover effect for restart button
        if event.type == MOUSEMOTION and self.is_over:
            
            # Coloring button's background
            if res_button.collidepoint(pos[0], pos[1]) and self.is_over:
                pygame.draw.rect(self.display, bg_color, res_button, 0, 20)
                self.draw_restart_button()
                
            # Resetting button's background
            else:
                pygame.draw.rect(self.display, self.main_bg, res_button, 0, 20)
                self.draw_restart_button()
        
        # Hover effect for selection buttons
        elif event.type == MOUSEMOTION and not run:
            
            # Coloring buttons' background
            if not selecting:
                if button_o.collidepoint(pos[0], pos[1]):
                    pygame.draw.rect(self.display, bg_color, button_o, 0, 20)
                    self.draw_buttons()
                elif button_x.collidepoint(pos[0], pos[1]):
                    pygame.draw.rect(self.display, bg_color, button_x, 0, 20)
                    self.draw_buttons()
                
                elif select_button.collidepoint(pos[0], pos[1]):
                    pygame.draw.rect(self.display, bg_color, select_button, 0, 20)
                    self.AI_level()
                    
                # Reseting buttons' background
                else:
                    pygame.draw.rect(self.display, self.main_bg, button_o, 0, 20)
                    pygame.draw.rect(self.display, self.main_bg, button_x, 0, 20)
                    pygame.draw.rect(self.display, self.main_bg, select_button, 0, 20)
                    self.draw_buttons()
                    self.AI_level()
                    
            else:
                if easy_button.collidepoint(pos[0], pos[1]):
                    pygame.draw.rect(self.display, bg_color, easy_button, 0, 20)
                    self.draw_selection_buttons()
                elif normal_button.collidepoint(pos[0], pos[1]):
                    pygame.draw.rect(self.display, bg_color, normal_button, 0, 20)
                    self.draw_selection_buttons()
                elif imp_button.collidepoint(pos[0], pos[1]):
                    pygame.draw.rect(self.display, bg_color, imp_button, 0, 20)
                    self.draw_selection_buttons()
                elif close_button.collidepoint(pos[0], pos[1]):
                    pygame.draw.rect(self.display, bg_color, close_button, 0, 100)
                    self.draw_selection_buttons(bg_color)
                else:
                    pygame.draw.rect(self.display, self.main_bg, easy_button, 0, 20)
                    pygame.draw.rect(self.display, self.main_bg, normal_button, 0, 20)
                    pygame.draw.rect(self.display, self.main_bg, imp_button, 0, 20)
                    pygame.draw.rect(self.display, self.main_bg, close_button, 0, 100)
                    self.draw_selection_buttons()
                
        # Hover effect for avaliable cells
        elif event.type == MOUSEMOTION and run:
            
            # Reseting cell's background
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "f":
                        filler = pygame.Rect(margin(j), margin(i) + self.center, box_size, box_size)
                        pygame.draw.rect(self.display, self.main_bg, filler)
                        self.board[i][j] = " "
                        
            # Coloring cell's background
            if (x, y) in self.avaliable_moves():
                filler = pygame.Rect(margin(x), margin(y) + self.center, box_size, box_size)
                pygame.draw.rect(self.display, bg_color, filler)
                self.board[y][x] = "f"
        
        if event.type == MOUSEBUTTONUP and event.button == 1: # Left click
            # Reset button
            if self.is_over:
                if res_button.collidepoint(pos[0], pos[1]):
                    self.is_over = False
                    self.display.fill(self.main_bg)
                    self.blank_board()
                    self.play()
            
            # Placing symbol on the cell  
            elif run and self.turn:
                if (x, y) in self.avaliable_moves():
                    # Resetting cell's background color before placing
                    filler = pygame.Rect(margin(x), margin(y) + self.center, box_size, box_size)
                    pygame.draw.rect(self.display, self.main_bg, filler)
                    
                    self.place(x , y, self.player)
                    pygame.display.update()
                    time.sleep(0.5)
                    self.move += 1
                    self.turn = False
                    
            # Selecting symbol
            elif not any((run, self.is_over, selecting)):
                if button_o.collidepoint(pos[0], pos[1]):
                    self.player = False
                    run = True
                if button_x.collidepoint(pos[0], pos[1]):
                    self.player = True
                    run = True
                if select_button.collidepoint(pos[0], pos[1]):
                    self.display.fill(self.main_bg)
                    self.draw_selection_buttons()
                    
            elif selecting:
                if easy_button.collidepoint(pos[0], pos[1]):
                    self.depth = 0
                    self.draw_selection_buttons()
                    time.sleep(1)
                    self.starting_screen()
                    selecting = False
                if normal_button.collidepoint(pos[0], pos[1]):
                    self.depth = 1
                    self.draw_selection_buttons()
                    time.sleep(1)
                    self.starting_screen()
                    selecting = False
                if imp_button.collidepoint(pos[0], pos[1]):
                    self.depth = 10
                    self.draw_selection_buttons()
                    time.sleep(1)
                    self.starting_screen()
                    selecting = False
                if close_button.collidepoint(pos[0], pos[1]):
                    self.starting_screen()
                    selecting = False
                
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    def starting_screen(self):
        self.display.fill(self.main_bg)
        self.AI_level()
        self.draw_selecting_text()
        self.draw_buttons()
        
    def check_winner(self, player : bool):
        # Returns row, col or diagonal values for drawing winning line
        
        for row in self.board:
            if all([cell == player for cell in row]):
                return (True, self.board.index(row), None, None)
            
        for col in range(3):
            if all([self.board[row][col] == player for row in range(3)]):
                return (True, None, col, None)
            
        if all([self.board[i][i] == player for i in range(3)]) or all([self.board[i][2-i] == player for i in range(3)]):
            return (True, None, None, True)
        
        return (False, None, None, None)
    
    def static_evaluation(self):
        for row in self.board:
            row_list = [cell for cell in row]
            if row_list.count(" ") == 1:
                row_list.remove(" ")
                if len(set(row_list)) == 1 and row_list[0] == self.player:
                    return self.player
        for col in range(3):
            col_list = [self.board[row][col] for row in range(3)]
            if col_list.count(" ") == 1:
                col_list.remove(" ")
                if len(set(col_list)) == 1 and col_list[0] == self.player:
                    return self.player
        diag_list = [self.board[i][i] for i in range(3)]
        if diag_list.count(" ") == 1:
            diag_list.remove(" ")
            if len(set(diag_list)) == 1 and diag_list[0] == self.player:
                return self.player
        diag_list = [self.board[i][2-i] for i in range(3)]
        if diag_list.count(" ") == 1:
            diag_list.remove(" ")
            if len(set(diag_list)) == 1 and diag_list[0] == self.player:
                return self.player
        return None
    
    def minimax(self, depth : int, alpha, beta, maximizingPlayer : bool): # Minimax Algorithm with alpha-beta pruning
        if self.depth == 0 and random.randint(1, 5) == 1: # Level Easy: 20% random
            return random.choice((0, 1, -1))
        
        if self.check_winner(not self.player)[0]:
            return depth + 1
        
        if self.check_winner(self.player)[0]:
            return - depth - 1
        
        if len(self.avaliable_moves()) == 0:
            return 0
        
        if depth <= 0:
            if self.static_evaluation() == self.player and self.depth % 2 == 0:
                return -1
            if self.static_evaluation() == maximizingPlayer and self.depth % 2 == 1:
                return 1
            return 0
            
        # Own perspective
        if maximizingPlayer != self.player:
            best_score = -float("inf")
            for move in self.avaliable_moves():
                self.board[move[1]][move[0]] = maximizingPlayer
                score = self.minimax(depth - 1, alpha, beta, not maximizingPlayer)
                self.board[move[1]][move[0]] = " "
                best_score = max(best_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best_score
        
        # Opponent's perspective
        else:
            best_score = float("inf")
            for move in self.avaliable_moves():
                self.board[move[1]][move[0]] = maximizingPlayer
                score = self.minimax(depth - 1, alpha, beta, not maximizingPlayer)
                self.board[move[1]][move[0]] = " "
                best_score = min(best_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best_score
        
    def find_best_move(self, symbol : bool):
        # All moves are equal at the start
        if self.move == 0:
            time.sleep(0.5)
            return random.choice(self.avaliable_moves())
        
        best_moves = []
        best_score = -float("inf")
        for move in self.avaliable_moves():
            self.board[move[1]][move[0]] = symbol
            score = self.minimax(self.depth, -float("inf"), float("inf"), not symbol)
            # print(move, score)
            self.board[move[1]][move[0]] = " "
            # Selecting moves that has highest score
            if score > best_score:
                best_score = score
                # If it finds move that has higher score than it already stored moves
                # Deletes previous moves
                best_moves.clear()
                best_moves.append( (move , score) )
                
            # Adds move to list if the move has same score 
            elif score == best_score:
                best_moves.append( (move , score) )
        # print(best_moves)
        # Selects one of the best moves
        return random.choice(best_moves)[0]
    
    def avaliable_moves(self):
        moves = []
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == " " or cell == "f":
                    moves.append((x,y))
        return moves

if __name__ == "__main__":
    new_game = Game()
    new_game.play()


