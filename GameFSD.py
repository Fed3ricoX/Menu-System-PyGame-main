import pygame, sys, random, math, threading
from tkinter import messagebox as mess
from tkinter import simpledialog
from button import Button

# Impostazioni della edit_screen 
schermo_larghezza = 1000
schermo_altezza = 700
cell_size = 20
path_cell_size = cell_size // 2
num_rows = schermo_altezza // cell_size
num_cols = schermo_larghezza // cell_size
N_OBSTACLE = 0 
posizione_start = None
obstacle_positions = []
path = []
posizioni_goals = []
draw_path = False
current_step = tipo_euristica = 0
count_goal = 0
delay = 200  
speed = 50   

# Colori Standard
WHITE = (255, 255, 255) # Bianco
BLACK = (0, 0, 0) # Nero
GRAY = (150, 150, 150)  # Grigio
GREEN = (0, 255, 0) # Verde 
RED = (255, 0, 0) # Rosso
YELLOW = (255, 255, 0) # Giallo   
ORANGE = (255, 165, 0)# Arancio
DARKGREEN = (0, 128, 0) # Verde scuro

Colori = [
    (255, 255, 0),    #Colore Giallo
    (155,48,255),      #Colore Purple
    (0,100,0),        #Colore Dark green
    (255, 0, 255),    # Colore Magenta
    (0,206,209),      #Colore Darkturquoise
    (0,201,87),       #Colore Emeraldgreen
    (255, 255, 255),  # Colore Bianco
    (0, 255, 0),      # Colore verde
    (255, 165, 0),    # Colore ORANGEne
    (128, 0, 128),    # Colore viola
    (255, 192, 203),  # Colore rosa
    (165, 42, 42),    # Colore marrone
    (0, 255, 255),    # Colore ciano
    (0, 255, 0),      # Colore lime
    (255, 215, 0),    # Colore oro
    (192, 192, 192),  # Colore argento
    (0, 255, 255),    # Colore acqua
    (128, 128, 0),    # Colore oliva
    (0, 128, 128),    # Colore teal
    (0, 0, 128),      # Colore navy
    (255, 127, 80),   # Colore corallo
    (75, 0, 130),     # Colore indaco
    (230, 230, 250),  # Colore lavanda
    (64, 224, 208),   # Colore turchese
    (221, 160, 221),   # Colore prugna
    (0, 64, 128),      # Blu scuro profondo
    (255, 140, 0),    # Rosso-ORANGE
    (0, 0, 255),      # Blu 
    (128, 128, 128),  # Grigio medio
    (255, 255, 128)  # Giallo pallido
]


# Funzioni dei pulsanti                    
def start_pos():
    global posizione_start

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Calcola le coordinate della casella in base alla posizione del mouse
                col = event.pos[0] // cell_size
                row = event.pos[1] // cell_size
                # Verifica se la casella è valida (non è un ostacolo) e si trova nella griglia
                if (col, row) not in obstacle_positions and 0 <= col < num_cols and 0 <= row < num_rows:
                    posizione_start = (col, row)
                    return
def goal_pos():
    global posizione_goal, posizioni_goals, count_goal

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Calcola le coordinate della casella in base alla posizione del mouse
                col = event.pos[0] // cell_size
                row = event.pos[1] // cell_size
                # Verifica se la casella è valida (non è un ostacolo) e si trova nella griglia
                if (col, row) not in obstacle_positions and 0 <= col < num_cols and 0 <= row < num_rows:
                    posizioni_goals.append((col, row))
                    count_goal += 1
                return
                
def select_euristica1():
    global tipo_euristica
    tipo_euristica = 1
    print("Hai selezionato l'euristica di Euclide")
    
def select_euristica2():
    global tipo_euristica, num_rows, num_cols 
    tipo_euristica = 2
    print("Hai selezionato l'euristica di Chebyshev")

def get_input():
    global N_OBSTACLE, obstacle_positions
    user_input = simpledialog.askstring("Input", "Inserisci il numero degli ostacoli:")

    if posizioni_goals and posizione_start:
        max_num_obst = num_rows * num_cols - len(posizioni_goals) - len(posizione_start)
    else:
        max_num_obst = num_rows * num_cols

    if user_input is not None:
        if int(user_input) < 0 or int(user_input) > max_num_obst:
            mess.showerror("Errore", f"Inserisci un numero valido compreso tra: 1 e {max_num_obst}")
        else: 
            try:
                N_OBSTACLE = int(user_input)
                obstacle_positions = generate_obstacle(N_OBSTACLE)
            except ValueError:
                mess.showerror("Errore", f"Inserisci un numero valido compreso tra: 1 e {max_num_obst}")    
    else:
        mess.showerror ("Errore", "Nessun input inserito")

def increase_speed():
    global delay
    delay -= speed
    if delay < 0:
        delay = 0

def decrease_speed():
    global delay
    delay += speed
    if delay > 400:
        delay = 400

def edit_screen():
    global obstacle_positions, posizione_start, posizione_goal, posizioni_goals, count_goal
    obstacle_positions = []
    posizione_start = None
    posizioni_goals = []
    count_goal = 0
    change_value("cell_size")
    change_value("num_cols")
    change_value("num_rows")

def change_value(variable_name):
    global cell_size, num_cols, num_rows, path_cell_size

    if variable_name == "cell_size":
        min_value = 10
        max_value = 40
        prompt = f"Inserisci la nuova dimensione della cella (minimo {min_value}, massimo {max_value}):"
        current_value = cell_size
    elif variable_name == "num_cols":
        min_value = 2
        max_value = schermo_larghezza // cell_size
        prompt = f"Inserisci la nuova dimensione delle colonne (minimo {min_value}, massimo {max_value}):"
        current_value = num_cols
    elif variable_name == "num_rows":
        min_value = 2
        max_value = schermo_altezza // cell_size
        prompt = f"Inserisci la nuova dimensione delle righe (minimo {min_value}, massimo {max_value}):"
        current_value = num_rows

    new_value = simpledialog.askinteger(f"Modifica {variable_name.capitalize()}", prompt, initialvalue=current_value)

    if new_value is not None:
        if variable_name == "cell_size" and 3 <= new_value <= 40:
            cell_size = new_value
            path_cell_size = cell_size // 2
        elif variable_name == "num_cols" and 2 <= new_value <= max_value:
            num_cols = new_value
        elif variable_name == "num_rows" and 2 <= new_value <= max_value:
            num_rows = new_value
        else:
            mess.showerror ("Errore", "Numero inserito non valido")
    else:
        mess.showerror ("Errore", "Numero inserito non valido")

def start_game():
    global draw_path, current_step, tipo_euristica
    
    if posizione_start and posizione_goal:
        current_step = 0
        
        if tipo_euristica == 1 or tipo_euristica == 2:
            calculate_path(tipo_euristica)
            draw_path = True
        else:
            mess.showwarning("Attenzione", "Devi selezionare un'euristica.")
            draw_path = False
    else:
        mess.showwarning("Attenzione", "Devi selezionare sia la casella di partenza che quella di destinazione.")

def reset_game():
    global obstacle_positions, posizione_start, posizioni_goals, count_goal
    obstacle_positions = generate_obstacle(N_OBSTACLE)
    posizione_start = None
    posizioni_goals = []
    count_goal = 0

def quit_game():
    pygame.quit()
    sys.exit() 

# Funzioni di creazione matrici: griglia e ostacoli
def crea_griglia(num_cols, num_rows, obstacle_positions):
    griglia = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    for col, row in obstacle_positions:
        griglia[row][col] = 1

    return griglia

def generate_obstacle(num_obstacles):
    global posizioni_goals
    obstacle_positions = set()

    for _ in range(num_obstacles):
        while True:
            col = random.randint(0, num_cols - 1)
            row = random.randint(0, num_rows - 1)
            if (col, row) not in obstacle_positions and (col, row) not in posizioni_goals:
                break
            
        obstacle_positions.add((col, row))

    return obstacle_positions
                
# Funzioni di disegno: griglia e ostacoli
def disegna_griglia(surface, num_cols, num_rows, cell_size, line_color):
    for col in range(num_cols):
        for row in range(num_rows):
            left = col * cell_size
            top = row * cell_size
            pygame.draw.rect(surface, line_color, (left, top, cell_size, cell_size), 1)

def disegna_ostacoli(surface, obstacle_positions, cell_size, obstacle_color):
    for col, row in obstacle_positions:
        left = col * cell_size
        top = row * cell_size
        pygame.draw.rect(surface, obstacle_color, (left, top, cell_size, cell_size)) 

class Node:
    def __init__(self, position):
        self.position = position  
        self.parent = None        
        self.g_cost = 0           
        self.h_cost = 0          
        self.f_cost = 0           

def successors(node, griglia, type_euristic):
    col, row = node.position
    successors = []
    if type_euristic == 1:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    elif type_euristic == 2:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dir_col, dir_row in directions:
        neighbor_col, neighbor_row = col + dir_col, row + dir_row

        if 0 <= neighbor_col < num_cols and 0 <= neighbor_row < num_rows:
            if griglia[neighbor_row][neighbor_col] != 1: 
                successors.append(Node((neighbor_col, neighbor_row)))

    return successors

# Euristiche
def chebyshev_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return max(dx, dy)

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def order_posizioni_goals_by_distance(posizione_start, posizioni_goals, tipo_euristica):
    posizioni_goals.sort(key=lambda point: distance_to_point(point, posizione_start, tipo_euristica))
    ordered_goals = [posizioni_goals[0]]
    remaining_goals = posizioni_goals[1:]
    
    for _ in range(len(remaining_goals)):
        nearest_point = min(remaining_goals, key=lambda point: distance_to_point(point, ordered_goals[-1], tipo_euristica))
        ordered_goals.append(nearest_point)
        remaining_goals.remove(nearest_point)

    return ordered_goals

def distance_to_point(point1, point2, tipo_euristica):
    if tipo_euristica == 1:
        return euclidean_distance(point1, point2)
    elif tipo_euristica == 2:
        return chebyshev_distance(point1, point2)
    else:
        return 0

# Ricerca del percorso
def find_path(start, target, griglia, type_euristic):
    open_set = []    
    explored_nodes = set()

    start_node = Node(start)
    target_node = Node(target)

    open_set.append(start_node)

    num_cols = len(griglia[0])
    num_rows = len(griglia)

    g_scores = [[float('inf')] * num_cols for _ in range(num_rows)]
    g_scores[start[1]][start[0]] = 0  

    while open_set:
        current_node = min(open_set, key=lambda node: node.f_cost)

        open_set.remove(current_node)
        explored_nodes.add(current_node.position)

        if current_node.position == target_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]
        
        neighbors = successors(current_node, griglia, type_euristic)

        for neighbor in neighbors:
            if neighbor.position not in explored_nodes:
                col, row = neighbor.position
                if type_euristic == 1:
                    tentative_g_cost = g_scores[current_node.position[1]][current_node.position[0]] + euclidean_distance(current_node.position, neighbor.position)
                elif type_euristic == 2:
                    tentative_g_cost = g_scores[current_node.position[1]][current_node.position[0]] + chebyshev_distance(current_node.position, neighbor.position)
                
                if tentative_g_cost < g_scores[row][col]:
                    neighbor.parent = current_node
                    g_scores[row][col] = tentative_g_cost
                    neighbor.g_cost = tentative_g_cost
                    if type_euristic == 1:
                        neighbor.h_cost = euclidean_distance(neighbor.position, target_node.position)
                    elif type_euristic == 2:
                        neighbor.h_cost = chebyshev_distance(neighbor.position, target_node.position)
                    neighbor.f_cost = neighbor.g_cost + neighbor.h_cost

                    if neighbor not in open_set:
                        open_set.append(neighbor)

    return []

def calculate_path(tipo_euristica):
    global path, draw_path, posizioni_goals

    new_posizioni_goals = order_posizioni_goals_by_distance(posizione_start, posizioni_goals, tipo_euristica)
    griglia = crea_griglia(num_cols, num_rows, obstacle_positions)
    
    reachable_posizioni_goals = trova_goal_raggiungibili(posizione_start, new_posizioni_goals, griglia, tipo_euristica)
    
    if posizione_start and reachable_posizioni_goals:
        for posizione_goal in reachable_posizioni_goals:
            path_to_goal = find_path(posizione_start, posizione_goal, griglia, tipo_euristica)
            if path_to_goal:
                break
        
        if not path_to_goal:
            mess.showerror("Errore", "Nessun goal raggiungibile trovata")
        else:
            path = path_to_goal
            draw_path = True

            for i in range(len(reachable_posizioni_goals) - 1):
                path += find_path(reachable_posizioni_goals[i], reachable_posizioni_goals[i+1], griglia, tipo_euristica)

            path += find_path(reachable_posizioni_goals[-1], posizione_start, griglia, tipo_euristica)
    else:
        mess.showerror("Errore", "Nessun goal raggiungibile trovata")

def trova_goal_raggiungibili(posizione_start, posizioni_goals, griglia, tipo_euristica):
    goal_raggiungibili = []
    for posizione_goal in posizioni_goals:
        path = find_path(posizione_start, posizione_goal, griglia, tipo_euristica)
        if path:
            goal_raggiungibili.append(posizione_goal)
    return goal_raggiungibili    
            
def main():
    global current_step, posizione_goal, posizioni_goals
    pygame.init()
    screen = pygame.display.set_mode((schermo_larghezza + 150, schermo_altezza))
    pygame.display.set_caption("Il Mio Gioco")

    start_button = Button("Start", (schermo_larghezza + 20, 10), (110, 50), start_game, GREEN, WHITE, ORANGE)
    quit_button = Button("Quit", (schermo_larghezza + 20, schermo_altezza - 60), (110, 50), quit_game, RED, WHITE, BLACK)
    pos_start_button = Button("Pos.Base", (schermo_larghezza + 20, 70), (110, 50), start_pos, WHITE, BLACK, GRAY)
    pos_goal_button = Button("Pos.Cibo", (schermo_larghezza + 20, 130), (110, 50), goal_pos, WHITE, BLACK, GRAY)
    euristica1_button = Button("Euclidean", (schermo_larghezza + 20, 190), (110, 50), select_euristica1, WHITE, BLACK, GRAY)
    euristica2_button = Button("Chebyshev", (schermo_larghezza + 20, 250), (110, 50), select_euristica2, WHITE, BLACK, GRAY)    
    obstacle_button = Button ("Ostacoli", (schermo_larghezza + 20, 310), (110, 50), get_input, GRAY, BLACK, WHITE)
    reset_button = Button("Reset", (schermo_larghezza + 20, 370), (110, 50), reset_game, GRAY, BLACK, WHITE)
    edit_screen_button = Button("Schermata", (schermo_larghezza + 20, 430), (110, 50), edit_screen, WHITE, BLACK, GRAY)
    increase_speed_button = Button("Speed++", (schermo_larghezza + 20, 490), (110, 50), increase_speed, YELLOW, DARKGREEN, BLACK)
    decrease_speed_button = Button("Speed--", (schermo_larghezza + 20, 550), (110, 50), decrease_speed, YELLOW, DARKGREEN, BLACK)

    buttons = [start_button, quit_button, pos_start_button, pos_goal_button, euristica1_button, euristica2_button, 
               reset_button, obstacle_button, edit_screen_button, increase_speed_button, decrease_speed_button]
    
#Loop Principale       
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            for button in buttons:
                button.handle_event(event)
                button.change_color(pygame.mouse.get_pos())

        screen.fill(BLACK)

        disegna_griglia(screen, num_cols, num_rows, cell_size, WHITE)
        disegna_ostacoli(screen, obstacle_positions, cell_size, GRAY)

        for button in buttons:
            button.draw(screen)
            
        if posizione_start:
            col, row = posizione_start
            left = col * cell_size
            top = row * cell_size
            pygame.draw.rect(screen, GREEN, (left, top, cell_size, cell_size))
        if count_goal > 0:   
            for posizione_goal in posizioni_goals:
                col, row = posizione_goal
                left = col * cell_size
                top = row * cell_size
                pygame.draw.rect(screen, RED, (left, top, cell_size, cell_size))
        
        if draw_path and current_step < len(path):
            c = 0
            prev_step = None
            all_goal = posizioni_goals.copy()
            for step in path[:current_step]:
                color = Colori[c]
                col, row = step
                left = col * cell_size
                top = row * cell_size
                if step in all_goal and step != prev_step:
                    all_goal.remove(step)
                    if c < len(Colori)-1:
                        c += 1
                        prev_step = step
                    else: 
                        c = 0
                        prev_step = step
                pygame.draw.rect(screen, color, (left + (cell_size - path_cell_size) / 2, top + (cell_size - path_cell_size) / 2, path_cell_size, path_cell_size))
            current_step += 1

            pygame.time.delay(delay)

        pygame.display.flip()

    pygame.quit()


# Avvio del programma
if __name__ == "__main__":
    path_calculation_thread = threading.Thread(target=calculate_path)
    path_calculation_thread.daemon = True
    path_calculation_thread.start()

    main()