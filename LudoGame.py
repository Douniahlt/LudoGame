import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import math
from PIL import Image, ImageTk  # Pour gérer l'image du menu

class LudoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu de Ludo")
        self.root.geometry("800x750")
        
        # Afficher d'abord l'écran d'accueil
        self.show_menu()
    
    def show_menu(self):
        """Affiche l'écran d'accueil avec l'image"""
        # Nettoyer l'écran
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Créer un frame pour le menu
        menu_frame = tk.Frame(self.root, width=800, height=750)
        menu_frame.pack(fill=tk.BOTH, expand=True)
        
        # Charger l'image
        try:
            menu_image = Image.open("ludo_board.png")
            menu_image = menu_image.resize((600, 600), Image.LANCZOS)
            self.menu_photo = ImageTk.PhotoImage(menu_image)
            
            # Afficher l'image
            image_label = tk.Label(menu_frame, image=self.menu_photo)
            image_label.pack(pady=20)
        except Exception as e:
            print(f"Erreur lors du chargement de l'image: {e}")
            error_label = tk.Label(menu_frame, text="Image non trouvée", font=("Arial", 24))
            error_label.pack(pady=50)
        
        # Bouton pour commencer le jeu
        start_button = tk.Button(
            menu_frame,
            text="COMMENCER",
            command=self.start_game,
            font=("Arial", 20, "bold"),
            bg="#FF6B6B",  # Rouge vif comme les pions rouges
            fg="white",
            padx=30,
            pady=15,
            relief=tk.RAISED,
            bd=5,  # Bordure plus épaisse
            activebackground="#E05555",  # Couleur quand on clique
            cursor="hand2"  # Curseur main au survol
        )
        start_button.pack(pady=10)
    
    def start_game(self):
        """Démarre le jeu en initialisant tous les éléments"""
        # Supprimer tous les widgets existants
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Initialiser le jeu comme dans le code original
        # Couleurs du jeu
        self.colors = {
            "red": "#FF6B6B",
            "green": "#88D498",
            "blue": "#90CCF4",
            "yellow": "#F7DC6F",
            "white": "#FFFFFF",
            "border": "#000000",
            "highlight": "#FF5722",
            "bg_color": "#F5F5F5"  # Couleur de fond du plateau
        }
        
        # État du jeu
        self.players = []
        self.current_player = 0
        self.dice_value = 0
        self.game_started = False
        self.consecutive_sixes = 0
        
        # Configuration du plateau
        self.board_size = 600
        self.cell_size = self.board_size // 15
        
        # Positions des cases étoile (cases protégées)
        self.star_positions = [
            (2, 6),   # Chemin rouge
            (6, 2),   # Chemin vert
            (12, 8),  # Chemin bleu
            (8, 12)   # Chemin jaune
        ]
        
        # Zone de "maison" finale pour chaque couleur
        self.home_final_paths = {
            "red": [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)],
            "green": [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6)],
            "blue": [(13, 7), (12, 7), (11, 7), (10, 7), (9, 7), (8, 7)],
            "yellow": [(7, 13), (7, 12), (7, 11), (7, 10), (7, 9), (7, 8)]
        }
        
        # Création du canvas pour le plateau
        self.canvas = tk.Canvas(self.root, width=self.board_size, height=self.board_size, bg=self.colors["bg_color"])
        self.canvas.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        
        # Message de statut
        self.status_label = tk.Label(
            self.root, 
            text="Bienvenue au jeu de Ludo! Commencez une nouvelle partie.",
            font=("Arial", 12),
            padx=10,
            pady=5
        )
        self.status_label.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
        
        # Label pour afficher la valeur du dé
        self.dice_text = tk.StringVar()
        self.dice_text.set("Dé: -")
        self.dice_label = tk.Label(
            self.root,
            textvariable=self.dice_text,
            font=("Arial", 14, "bold"),
            bg="#E1F5FE",
            width=8,
            padx=10,
            pady=5,
            relief=tk.RIDGE
        )
        self.dice_label.place(relx=0.35, rely=0.8, anchor=tk.CENTER)
        
        # Label pour le joueur actuel
        self.player_text = tk.StringVar()
        self.player_text.set("Joueur: -")
        self.player_label = tk.Label(
            self.root,
            textvariable=self.player_text,
            font=("Arial", 14, "bold"),
            bg="#FFF9C4",
            width=18,
            padx=10,
            pady=5,
            relief=tk.RIDGE
        )
        self.player_label.place(relx=0.65, rely=0.8, anchor=tk.CENTER)
        
        # Boutons
        # Bouton pour démarrer une nouvelle partie
        self.new_game_button = tk.Button(
            self.root, 
            text="NOUVELLE PARTIE", 
            command=self.setup_game,
            font=("Arial", 14, "bold"),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED
        )
        self.new_game_button.place(relx=0.25, rely=0.9, anchor=tk.CENTER)
        
        # Bouton pour lancer le dé (initialement désactivé)
        self.dice_button = tk.Button(
            self.root,
            text="LANCER LE DÉ",
            command=self.roll_dice,
            state=tk.DISABLED,
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED
        )
        self.dice_button.place(relx=0.75, rely=0.9, anchor=tk.CENTER)
        
        # Dessiner le plateau vide initial
        self.draw_empty_board()
    
    # Le reste du code est identique à votre code original
    def draw_empty_board(self):
        """Dessine le plateau de jeu vide"""
        # Effacer le canvas
        self.canvas.delete("all")
        
        # Tailles
        board_size = self.board_size
        cell_size = self.cell_size
        
        # Dessiner le quadrillage du plateau
        for i in range(16):
            # Lignes horizontales
            self.canvas.create_line(0, i * cell_size, board_size, i * cell_size, fill="black")
            # Lignes verticales
            self.canvas.create_line(i * cell_size, 0, i * cell_size, board_size, fill="black")
        
        # Dessiner les zones de base (coins colorés)
        # Zone rouge (en haut à gauche)
        self.canvas.create_rectangle(0, 0, 6 * cell_size, 6 * cell_size, fill=self.colors["red"], outline="black")
        # Zone verte (en haut à droite)
        self.canvas.create_rectangle(9 * cell_size, 0, 15 * cell_size, 6 * cell_size, fill=self.colors["green"], outline="black")
        # Zone bleue (en bas à gauche)
        self.canvas.create_rectangle(0, 9 * cell_size, 6 * cell_size, 15 * cell_size, fill=self.colors["blue"], outline="black")
        # Zone jaune (en bas à droite)
        self.canvas.create_rectangle(9 * cell_size, 9 * cell_size, 15 * cell_size, 15 * cell_size, fill=self.colors["yellow"], outline="black")
        
        # Dessiner le centre
        self.canvas.create_rectangle(6 * cell_size, 6 * cell_size, 9 * cell_size, 9 * cell_size, fill="white", outline="black")
        
        # Dessiner les chemins colorés vers le centre
        # Chemin rouge (de gauche vers le centre)
        for i in range(6):
            self.canvas.create_rectangle((i+1) * cell_size, 7 * cell_size, (i+2) * cell_size, 8 * cell_size, fill="#FFCDD2", outline="black")
        
        # Chemin vert (du haut vers le centre)
        for i in range(6):
            self.canvas.create_rectangle(7 * cell_size, (i+1) * cell_size, 8 * cell_size, (i+2) * cell_size, fill="#C8E6C9", outline="black")
        
        # Chemin bleu (de droite vers le centre)
        for i in range(6):
            self.canvas.create_rectangle((13-i) * cell_size, 7 * cell_size, (14-i) * cell_size, 8 * cell_size, fill="#BBDEFB", outline="black")
        
        # Chemin jaune (du bas vers le centre)
        for i in range(6):
            self.canvas.create_rectangle(7 * cell_size, (13-i) * cell_size, 8 * cell_size, (14-i) * cell_size, fill="#FFF9C4", outline="black")
        
        # Dessiner le chemin de jeu (cases blanches)
        path_coords = [
            # Ligne du haut (de gauche à droite)
            [(i, 6) for i in range(1, 6)],
            [(6, i) for i in range(1, 6)],
            [(7, i) for i in range(0, 6)],
            [(8, i) for i in range(1, 6)],
            [(i, 6) for i in range(9, 14)],
            
            # Ligne de droite (de haut en bas)
            [(14, i) for i in range(7, 14)],
            [(13, 8) for i in range(1)],
            [(12, 8) for i in range(1)],
            [(11, 8) for i in range(1)],
            [(10, 8) for i in range(1)],
            [(9, 8) for i in range(1)],
            [(8, i) for i in range(9, 14)],
            
            # Ligne du bas (de droite à gauche)
            [(i, 14) for i in range(7, 0, -1)],
            [(6, i) for i in range(13, 8, -1)],
            [(5, 8) for i in range(1)],
            [(4, 8) for i in range(1)],
            [(3, 8) for i in range(1)],
            [(2, 8) for i in range(1)],
            [(1, 8) for i in range(1)],
            [(0, i) for i in range(7, 0, -1)]
        ]
        
        # Aplatir la liste
        path_coords = [coord for sublist in path_coords for coord in sublist]
        
        # Dessiner les cases du chemin
        for x, y in path_coords:
            if (x, y) not in self.star_positions:  # Éviter les cases étoiles
                self.canvas.create_rectangle(
                    x * cell_size, y * cell_size, 
                    (x+1) * cell_size, (y+1) * cell_size, 
                    fill="white", outline="black"
                )
        
        # Dessiner les cases étoiles
        for x, y in self.star_positions:
            self.canvas.create_rectangle(
                x * cell_size, y * cell_size, 
                (x+1) * cell_size, (y+1) * cell_size, 
                fill="gold", outline="black"
            )
            self.draw_star(
                (x + 0.5) * cell_size, 
                (y + 0.5) * cell_size, 
                cell_size // 3
            )
        
        # Dessiner les cases de départ
        start_positions = {
            "red": (1, 6),
            "green": (8, 1),
            "blue": (13, 8),
            "yellow": (6, 13)
        }
        
        # Dessiner un cercle pour chaque case de départ
        for color, (x, y) in start_positions.items():
            self.canvas.create_oval(
                (x + 0.2) * cell_size, (y + 0.2) * cell_size,
                (x + 0.8) * cell_size, (y + 0.8) * cell_size,
                fill=self.colors[color], outline="black", width=2
            )
        
        # Dessiner les bases (emplacements de départ des pions)
        home_positions = {
            "red": [(2, 2), (2, 4), (4, 2), (4, 4)],
            "green": [(10, 2), (10, 4), (12, 2), (12, 4)],
            "blue": [(2, 10), (2, 12), (4, 10), (4, 12)],
            "yellow": [(10, 10), (10, 12), (12, 10), (12, 12)]
        }
        
        # Dessiner un cercle pour chaque emplacement de base
        for color, positions in home_positions.items():
            for x, y in positions:
                self.canvas.create_oval(
                    (x + 0.1) * cell_size, (y + 0.1) * cell_size,
                    (x + 0.9) * cell_size, (y + 0.9) * cell_size,
                    fill="white", outline="black", width=2
                )
        
        # Dessiner des triangles pour indiquer les directions
        # Flèche pour le rouge
        self.draw_triangle(0.5 * cell_size, 7.5 * cell_size, cell_size * 0.4, "right", "red")
        # Flèche pour le vert
        self.draw_triangle(7.5 * cell_size, 0.5 * cell_size, cell_size * 0.4, "down", "green")
        # Flèche pour le bleu
        self.draw_triangle(14.5 * cell_size, 7.5 * cell_size, cell_size * 0.4, "left", "blue")
        # Flèche pour le jaune
        self.draw_triangle(7.5 * cell_size, 14.5 * cell_size, cell_size * 0.4, "up", "yellow")
    
    def draw_triangle(self, x, y, size, direction, color):
        """Dessine un triangle pointant dans une direction donnée"""
        if direction == "right":
            points = [
                x - size/2, y - size/2,
                x - size/2, y + size/2,
                x + size/2, y
            ]
        elif direction == "down":
            points = [
                x - size/2, y - size/2,
                x + size/2, y - size/2,
                x, y + size/2
            ]
        elif direction == "left":
            points = [
                x + size/2, y - size/2,
                x + size/2, y + size/2,
                x - size/2, y
            ]
        elif direction == "up":
            points = [
                x - size/2, y + size/2,
                x + size/2, y + size/2,
                x, y - size/2
            ]
        
        self.canvas.create_polygon(points, fill=self.colors[color], outline="black")
    
    def draw_star(self, x, y, size=10):
        """Dessine une étoile à 5 branches"""
        points = []
        for i in range(10):
            # Angle en radians
            angle = math.pi/2 + i * 2 * math.pi / 10
            # Rayon externe ou interne
            radius = size if i % 2 == 0 else size/2
            # Calculer les coordonnées
            px = x + radius * math.cos(angle)
            py = y + radius * math.sin(angle)
            points.append(px)
            points.append(py)
        
        # Dessiner l'étoile
        self.canvas.create_polygon(points, fill="gold", outline="orange")
    
    def setup_game(self):
        """Configuration d'une nouvelle partie"""
        # Demander le nombre de joueurs
        player_count = simpledialog.askinteger("Configuration", "Nombre de joueurs humains (1-4):", 
                                              minvalue=1, maxvalue=4)
        if player_count is None:
            return
        
        # Liste des couleurs disponibles
        available_colors = ["red", "green", "blue", "yellow"]
        color_names = {
            "red": "Rouge",
            "green": "Vert",
            "blue": "Bleu",
            "yellow": "Jaune"
        }
        
        # Initialiser les joueurs
        self.players = []
        
        # Définir les positions de départ pour chaque couleur
        path_starts = {
            "red": (1, 6),     # Position de départ du chemin rouge (à gauche)
            "green": (8, 1),   # Position de départ du chemin vert (en haut)
            "blue": (13, 8),   # Position de départ du chemin bleu (à droite)
            "yellow": (6, 13)  # Position de départ du chemin jaune (en bas)
        }
        
        # Définir les coordonnées des zones de départ (bases)
        home_positions = {
            "red": [(2, 2), (2, 4), (4, 2), (4, 4)],
            "green": [(10, 2), (10, 4), (12, 2), (12, 4)],
            "blue": [(2, 10), (2, 12), (4, 10), (4, 12)],
            "yellow": [(10, 10), (10, 12), (12, 10), (12, 12)]
        }
        
        # Ajouter les joueurs humains et IA
        for i in range(4):
            color = available_colors[i]
            player_type = "human" if i < player_count else "ai"
            
            # Créer les pions dans leur base
            pawns = []
            for j, pos in enumerate(home_positions[color]):
                pawns.append({
                    "id": j,
                    "position": pos,
                    "status": "home",  # home, path, safe
                    "path_position": -1
                })
            
            # Ajouter le joueur à la liste
            self.players.append({
                "type": player_type,
                "color": color,
                "pawns": pawns,
                "home": 0,  # Nombre de pions arrivés à la destination finale
                "start_position": path_starts[color]
            })
        
        # Réinitialiser l'état du jeu
        self.current_player = 0
        self.dice_value = 0
        self.game_started = True
        self.consecutive_sixes = 0
        
        # Activer le bouton de dé
        self.dice_button.config(state=tk.NORMAL)
        
        # Dessiner le plateau vide
        self.draw_empty_board()
        
        # Dessiner les pions
        self.update_board()
        
        # Mettre à jour l'interface
        self.update_ui()
        
        # Message de début de partie
        player_info = ", ".join([
            f"{color_names[player['color']]} ({('Vous' if player['type']=='human' else 'IA')})" 
            for player in self.players
        ])
        
        self.show_status_message(f"La partie commence! Joueurs: {player_info}", duration=4000)
        messagebox.showinfo(
            "Nouvelle partie", 
            f"La partie commence !\n\nOrdre des joueurs: {player_info}\n\nJoueur 1 ({color_names[self.players[0]['color']]}) commence."
        )
    
    def update_board(self):
        """Met à jour l'affichage du plateau avec les pions"""
        # Redessiner les pions de chaque joueur
        for player in self.players:
            for pawn in player["pawns"]:
                self.draw_pawn(pawn, player["color"])
    
    def draw_pawn(self, pawn, color):
        """Dessine un pion à sa position"""
        if pawn["status"] == "safe":
            return  # Ne pas dessiner les pions arrivés
            
        x, y = pawn["position"]
        cell = self.cell_size
        
        # Calcul des coordonnées du centre de la cellule
        center_x = (x + 0.5) * cell
        center_y = (y + 0.5) * cell
        
        # Taille du pion
        radius = cell // 3
        
        # Dessiner le pion (cercle coloré avec bordure noire)
        self.canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill=self.colors[color], outline="black", width=2,
            tags=f"pawn_{color}_{pawn['id']}"
        )
        
        # Ajouter un petit cercle blanc au centre pour l'effet 3D
        inner_radius = radius // 2
        self.canvas.create_oval(
            center_x - inner_radius, center_y - inner_radius,
            center_x + inner_radius, center_y + inner_radius,
            fill="white", outline="",
            tags=f"pawn_{color}_{pawn['id']}_inner"
        )
    
    def roll_dice(self):
        """Lance le dé et gère le tour du joueur actuel"""
        # Lancer le dé (1-6)
        self.dice_value = random.randint(1, 6)
        
        # Mettre à jour l'affichage du dé
        self.dice_text.set(f"Dé: {self.dice_value}")
        
        # Désactiver le bouton de dé pendant le traitement du tour
        self.dice_button.config(state=tk.DISABLED)
        
        # Ajouter un effet visuel pour le lancement du dé
        self.animate_dice(5, self.dice_value)
    
    def animate_dice(self, iterations, final_value):
        """Anime le lancement du dé avec un effet visuel"""
        if iterations > 0:
            # Afficher une valeur aléatoire
            temp_value = random.randint(1, 6)
            self.dice_text.set(f"Dé: {temp_value}")
            # Continuer l'animation
            self.root.after(100, lambda: self.animate_dice(iterations - 1, final_value))
        else:
            # Afficher la valeur finale
            self.dice_text.set(f"Dé: {final_value}")
            # Gérer le tour après l'animation
            self.play_turn()
    
    def play_turn(self):
        """Gère le tour du joueur actuel"""
        player = self.players[self.current_player]
        
        # Vérifier si le joueur peut faire un mouvement
        movable_pawns = self.get_movable_pawns(player)
        
        if not movable_pawns:
            # Si aucun pion ne peut être déplacé, montrer un message et passer au joueur suivant
            self.show_status_message("Aucun mouvement possible")
            self.root.after(1500, self.next_player)
            return
            
        if player["type"] == "human":
            # Pour un joueur humain, on active les pions qu'il peut déplacer
            self.show_status_message("Sélectionnez un pion à déplacer")
            
            # Activer les clics sur le canvas pour sélectionner un pion
            self.canvas.bind("<Button-1>", self.on_canvas_click)
            
            # Mettre en évidence les pions jouables
            self.highlight_movable_pawns(movable_pawns)
        else:
            # Pour un joueur IA, on joue automatiquement après un court délai
            self.show_status_message("L'ordinateur réfléchit...")
            self.root.after(1000, lambda: self.ai_play_turn(player))
    
    def get_movable_pawns(self, player):
        """Retourne la liste des pions qui peuvent être déplacés"""
        movable_pawns = []
        
        # Si le dé donne 6, on peut sortir un pion de la maison
        if self.dice_value == 6:
            # Vérifier s'il y a un pion à la maison
            home_pawns = [p for p in player["pawns"] if p["status"] == "home"]
            if home_pawns:
                # Vérifier si la case de départ est occupée par un pion du même joueur
                start_pos = player["start_position"]
                start_pos_occupied = False
                
                for p in player["pawns"]:
                    if p["status"] == "path" and p["position"] == start_pos:
                        start_pos_occupied = True
                        break
                
                # Si la case de départ n'est pas occupée, on peut sortir un pion
                if not start_pos_occupied:
                    for pawn in home_pawns:
                        movable_pawns.append(pawn)
        
        # On peut déplacer les pions qui sont déjà sur le chemin
        for pawn in player["pawns"]:
            if pawn["status"] == "path":
                # Vérifier si le déplacement est possible
                new_path_position = pawn["path_position"] + self.dice_value
                
                # Si le pion atteint la fin du parcours, vérifier s'il peut y entrer
                if new_path_position >= 50:  # Fin du parcours standard
                    # Calculer la position finale
                    steps_beyond = new_path_position - 49
                    if steps_beyond <= 6:  # Le pion peut entrer dans sa maison finale
                        movable_pawns.append(pawn)
                else:
                    # Calculer la nouvelle position
                    new_pos = self.calculate_position(player["color"], new_path_position)
                    
                    # Vérifier s'il y a collision avec un pion du même joueur
                    collision = False
                    for other_pawn in player["pawns"]:
                        if (other_pawn != pawn and other_pawn["status"] == "path" and 
                            other_pawn["position"] == new_pos and new_pos not in self.star_positions):
                            collision = True
                            break
                    
                    if not collision:
                        movable_pawns.append(pawn)
        
        return movable_pawns
    
    def show_status_message(self, message, duration=2000):
        """Affiche un message d'état temporaire"""
        # Mettre à jour le label
        self.status_label.config(text=message)
        
        # Configurer un nouveau timer si une durée est spécifiée
        if hasattr(self, 'status_message_timer') and self.status_message_timer:
            self.root.after_cancel(self.status_message_timer)
            
        if duration > 0:
            self.status_message_timer = self.root.after(
                duration, 
                lambda: self.status_label.config(text="")
            )
    
    def highlight_movable_pawns(self, pawns):
        """Met en évidence les pions qui peuvent être déplacés"""
        # Redessiner le plateau pour effacer les mises en évidence précédentes
        self.draw_empty_board()
        self.update_board()
        
        # Dessiner un cercle de mise en évidence autour des pions jouables
        for pawn in pawns:
            x, y = pawn["position"]
            cell = self.cell_size
            center_x = (x + 0.5) * cell
            center_y = (y + 0.5) * cell
            
            # Dessiner un cercle plus grand autour du pion
            self.canvas.create_oval(
                center_x - cell//2, center_y - cell//2,
                center_x + cell//2, center_y + cell//2,
                outline=self.colors["highlight"], width=3, dash=(5, 3),
                tags="highlight"
            )
            
            # Effet clignotant (animation)
            self.blink_highlight(center_x, center_y, cell//2, 0)

    def blink_highlight(self, x, y, radius, state):
        """Crée un effet clignotant pour les pions sélectionnables"""
        # Arrêter l'animation si le joueur a déjà joué
        if not self.canvas.find_withtag("highlight"):
            return
            
        # Alterner entre deux états (visible/invisible)
        if state == 0:
            # Dessiner le cercle
            highlight = self.canvas.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                outline=self.colors["highlight"], width=3, dash=(5, 3),
                tags="highlight"
            )
            next_state = 1
        else:
            # Supprimer tous les cercles
            self.canvas.delete("highlight")
            next_state = 0
        
        # Programmer la prochaine étape de l'animation
        self.root.after(500, lambda: self.blink_highlight(x, y, radius, next_state))
    
    def on_canvas_click(self, event):
        """Gère les clics sur le canvas pour sélectionner un pion"""
        player = self.players[self.current_player]
        
        # Ne traiter les clics que si c'est un joueur humain
        if player["type"] != "human":
            return
            
        # Convertir les coordonnées du clic en indices de cellule
        cell_x = event.x // self.cell_size
        cell_y = event.y // self.cell_size
        
        # Vérifier si un pion déplaçable a été cliqué
        movable_pawns = self.get_movable_pawns(player)
        for pawn in movable_pawns:
            x, y = pawn["position"]
            if abs(x - cell_x) <= 0.5 and abs(y - cell_y) <= 0.5:  # Tolérance de clic
                # Désactiver les clics sur le canvas
                self.canvas.unbind("<Button-1>")
                self.canvas.delete("highlight")
                
                # Déplacer le pion
                self.move_pawn(player, pawn)
                return
        
        # Si on clique ailleurs, afficher un message
        self.show_status_message("Sélectionnez un pion entouré en orange")
    
    def ai_play_turn(self, player):
        """Implémentation pour le tour d'un joueur IA"""
        # Obtenir la liste des pions qui peuvent être déplacés
        movable_pawns = self.get_movable_pawns(player)
        
        if not movable_pawns:
            # Si aucun pion ne peut être déplacé, passer au joueur suivant
            self.show_status_message(f"L'ordinateur {player['color']} ne peut pas jouer")
            self.next_player()
            return
        
        # Stratégie simple pour l'IA:
        # 1. Si on peut sortir un pion (dé=6 et pion à la maison), le faire
        # 2. Si on peut capturer un pion adverse, le faire
        # 3. Déplacer le pion le plus avancé sur le chemin
        
        # Priorité 1: Sortir un pion si possible
        if self.dice_value == 6:
            home_pawns = [p for p in movable_pawns if p["status"] == "home"]
            if home_pawns:  # Vérifier qu'il reste des pions à la maison
                pawn_to_move = home_pawns[0]  # Prendre le premier pion à la maison
                color_names = {"red": "Rouge", "green": "Vert", "blue": "Bleu", "yellow": "Jaune"}
                self.show_status_message(f"L'ordinateur {color_names[player['color']]} sort un pion")
                self.move_pawn(player, pawn_to_move)
                return
        
        # Priorité 2: Capturer un pion adverse si possible
        for pawn in movable_pawns:
            if pawn["status"] == "path":
                # Simuler le déplacement pour voir s'il y a capture
                new_path_position = pawn["path_position"] + self.dice_value
                
                # Si le pion termine son parcours, le déplacer
                if new_path_position >= 50:  # Fin du parcours standard
                    color_names = {"red": "Rouge", "green": "Vert", "blue": "Bleu", "yellow": "Jaune"}
                    self.show_status_message(f"L'ordinateur {color_names[player['color']]} place un pion à la maison")
                    self.move_pawn(player, pawn)
                    return
                
                # Calculer la nouvelle position
                new_pos = self.calculate_position(player["color"], new_path_position)
                
                # Vérifier s'il y a des pions adverses à cette position
                # et que ce n'est pas une case étoile (protégée)
                if new_pos not in self.star_positions:
                    for other_player in self.players:
                        if other_player["color"] != player["color"]:
                            for other_pawn in other_player["pawns"]:
                                other_x, other_y = other_pawn["position"]
                                new_x, new_y = new_pos
                                
                                if other_x == new_x and other_y == new_y and other_pawn["status"] == "path":
                                    # On peut capturer un pion!
                                    color_names = {"red": "Rouge", "green": "Vert", "blue": "Bleu", "yellow": "Jaune"}
                                    self.show_status_message(f"L'ordinateur {color_names[player['color']]} capture un pion {color_names[other_player['color']]}")
                                    self.move_pawn(player, pawn)
                                    return
        
        # Priorité 3: Déplacer le pion le plus avancé
        most_advanced_pawn = None
        highest_position = -1
        
        for pawn in movable_pawns:
            if pawn["status"] == "path" and pawn["path_position"] > highest_position:
                highest_position = pawn["path_position"]
                most_advanced_pawn = pawn
        
        if most_advanced_pawn:
            color_names = {"red": "Rouge", "green": "Vert", "blue": "Bleu", "yellow": "Jaune"}
            self.show_status_message(f"L'ordinateur {color_names[player['color']]} avance un pion")
            self.move_pawn(player, most_advanced_pawn)
            return
        
        # Si on arrive ici, choisir un pion au hasard
        random_pawn = random.choice(movable_pawns)
        color_names = {"red": "Rouge", "green": "Vert", "blue": "Bleu", "yellow": "Jaune"}
        self.show_status_message(f"L'ordinateur {color_names[player['color']]} joue au hasard")
        self.move_pawn(player, random_pawn)
    
    def move_pawn(self, player, pawn):
        """Déplace un pion"""
        color_names = {
            "red": "Rouge",
            "green": "Vert",
            "blue": "Bleu",
            "yellow": "Jaune"
        }
        
        # Si le pion est à la maison et que le dé est 6, le sortir
        if pawn["status"] == "home" and self.dice_value == 6:
            pawn["status"] = "path"
            pawn["path_position"] = 0
            pawn["position"] = player["start_position"]
            
            # Message pour le joueur
            if player["type"] == "human":
                self.show_status_message(f"Vous avez sorti un pion!")
            
            # Vérifier si une capture est possible
            self.check_capture(player, pawn)
            
            # Mettre à jour le plateau avec animation
            self.animate_move(pawn, player["color"])
            
            # Donner un autre tour au joueur (car il a fait 6)
            self.root.after(1000, self.next_player)
            return
        
        # Si le pion est déjà sur le chemin, le déplacer
        if pawn["status"] == "path":
            new_path_position = pawn["path_position"] + self.dice_value
            
            # Vérifier si le pion a terminé le tour complet et entre dans sa maison finale
            if new_path_position >= 50:  # Fin du parcours standard
                # Calculer combien de pas au-delà de la case 50
                steps_beyond = new_path_position - 49
                
                if steps_beyond <= 6:  # Le pion peut entrer dans sa maison finale
                    # Calculer la position dans le chemin final
                    final_path = self.home_final_paths[player["color"]]
                    final_index = steps_beyond - 1
                    
                    if final_index >= len(final_path):  # Le pion est arrivé à la fin
                        pawn["status"] = "safe"
                        player["home"] += 1
                        
                        # Message pour le joueur
                        if player["type"] == "human":
                            self.show_status_message(f"Bravo! Un de vos pions est arrivé à la maison!")
                        
                        # Vérifier si le joueur a gagné
                        if player["home"] == 4:
                            self.end_game(self.current_player)
                            return
                    else:
                        # Placer le pion sur le chemin final
                        pawn["position"] = final_path[final_index]
                else:
                    # Le pion reste où il est (pas assez de points pour entrer complètement)
                    new_path_position = pawn["path_position"]
            else:
                # Calculer la nouvelle position sur le plateau
                pawn["path_position"] = new_path_position
                pawn["position"] = self.calculate_position(player["color"], new_path_position)
                
                # Message pour le joueur
                if player["type"] == "human":
                    self.show_status_message(f"Vous avez déplacé un pion de {self.dice_value} cases")
                
                # Vérifier si une capture est possible
                self.check_capture(player, pawn)
            
            # Mettre à jour le plateau avec animation
            self.animate_move(pawn, player["color"])
        
        # Passer au joueur suivant si le dé n'est pas 6
        if self.dice_value != 6:
            self.root.after(1000, self.next_player)
        else:
            # Si c'est 6, donner un autre tour au joueur (sauf si 3 fois consécutives)
            if hasattr(self, 'consecutive_sixes') and self.consecutive_sixes >= 2:
                self.show_status_message("3 fois 6 consécutifs! Votre tour est terminé.")
                self.consecutive_sixes = 0
                self.root.after(1000, self.next_player)
            else:
                # Réactiver le bouton de dé
                self.root.after(1000, lambda: self.dice_button.config(state=tk.NORMAL))
                # Incrémenter le compteur de 6 consécutifs
                self.consecutive_sixes = self.consecutive_sixes + 1 if hasattr(self, 'consecutive_sixes') else 1
    
    def animate_move(self, pawn, color):
        """Anime le déplacement d'un pion"""
        # Redessiner le plateau
        self.draw_empty_board()
        self.update_board()
        
        # Faire clignoter le pion déplacé si encore sur le plateau
        if pawn["status"] != "safe":
            x, y = pawn["position"]
            cell = self.cell_size
            center_x = (x + 0.5) * cell
            center_y = (y + 0.5) * cell
            
            # Effet de surbrillance temporaire
            radius = cell // 3
            highlight = self.canvas.create_oval(
                center_x - radius - 5, center_y - radius - 5,
                center_x + radius + 5, center_y + radius + 5,
                outline="white", width=3, dash=(5, 2),
                tags="move_highlight"
            )
            
            # Faire disparaître l'effet après un court délai
            self.root.after(800, lambda: self.canvas.delete("move_highlight"))
    
    def check_capture(self, player, pawn):
        """Vérifie si un pion peut en capturer un autre"""
        x, y = pawn["position"]
        captured = False
        
        # Vérifier si le pion est sur une case étoile (protégée)
        if (x, y) in self.star_positions:
            return False  # Pas de capture possible sur les cases étoile
        
        # Vérifier s'il y a des pions adverses à la même position
        for other_player in self.players:
            if other_player["color"] != player["color"]:
                for other_pawn in other_player["pawns"]:
                    other_x, other_y = other_pawn["position"]
                    
                    if other_x == x and other_y == y and other_pawn["status"] == "path":
                        # Capture: renvoyer le pion à sa base
                        other_pawn["status"] = "home"
                        other_pawn["path_position"] = -1
                        
                        # Retrouver la position de base pour ce pion
                        home_positions = {
                            "red": [(2, 2), (2, 4), (4, 2), (4, 4)],
                            "green": [(10, 2), (10, 4), (12, 2), (12, 4)],
                            "blue": [(2, 10), (2, 12), (4, 10), (4, 12)],
                            "yellow": [(10, 10), (10, 12), (12, 10), (12, 12)]
                        }
                        
                        other_pawn["position"] = home_positions[other_player["color"]][other_pawn["id"]]
                        
                        # Indiquer qu'une capture a eu lieu
                        captured = True
                        
                        # Montrer un message
                        color_names = {
                            "red": "Rouge",
                            "green": "Vert",
                            "blue": "Bleu",
                            "yellow": "Jaune"
                        }
                        self.show_status_message(
                            f"🎯 Le pion {color_names[player['color']]} a capturé un pion {color_names[other_player['color']]}!",
                            duration=2000
                        )
        
        return captured
    
    def calculate_position(self, color, path_position):
        """Calcule la position sur le plateau en fonction de la position sur le chemin"""
        # Chemins pour chaque couleur
        paths = {
            "red": [
                # Départ rouge (1, 6) et parcours
                (1, 6), (2, 6), (3, 6), (4, 6), (5, 6),
                (6, 5), (6, 4), (6, 3), (6, 2), (6, 1),
                (7, 1), (8, 1), (9, 1), (10, 1), (11, 1),
                (12, 1), (13, 1), (14, 1), (14, 2), (14, 3),
                (14, 4), (14, 5), (14, 6), (14, 7), (13, 7),
                (12, 7), (11, 7), (10, 7), (9, 7), (8, 7),
                (7, 7), (7, 8), (7, 9), (7, 10), (7, 11),
                (7, 12), (7, 13), (7, 14), (6, 14), (5, 14),
                (4, 14), (3, 14), (2, 14), (1, 14), (1, 13),
                (1, 12), (1, 11), (1, 10), (1, 9), (1, 8),
                (1, 7)  # Position finale pour rentrer dans la maison
            ],
            "green": [
                # Départ vert (8, 1) et parcours
                (8, 1), (8, 2), (8, 3), (8, 4), (8, 5),
                (9, 6), (10, 6), (11, 6), (12, 6), (13, 6),
                (14, 6), (14, 7), (13, 7), (12, 7), (11, 7),
                (10, 7), (9, 7), (8, 7), (7, 7), (7, 8),
                (7, 9), (7, 10), (7, 11), (7, 12), (7, 13),
                (7, 14), (6, 14), (5, 14), (4, 14), (3, 14),
                (2, 14), (1, 14), (1, 13), (1, 12), (1, 11),
                (1, 10), (1, 9), (1, 8), (1, 7), (1, 6),
                (2, 6), (3, 6), (4, 6), (5, 6), (6, 5),
                (6, 4), (6, 3), (6, 2), (6, 1), (7, 1),
                (7, 6)  # Position finale pour rentrer dans la maison
            ],
            "blue": [
                # Départ bleu (13, 8) et parcours
                (13, 8), (12, 8), (11, 8), (10, 8), (9, 8),
                (8, 9), (8, 10), (8, 11), (8, 12), (8, 13),
                (8, 14), (7, 14), (6, 14), (5, 14), (4, 14),
                (3, 14), (2, 14), (1, 14), (1, 13), (1, 12),
                (1, 11), (1, 10), (1, 9), (1, 8), (1, 7),
                (1, 6), (2, 6), (3, 6), (4, 6), (5, 6),
                (6, 5), (6, 4), (6, 3), (6, 2), (6, 1),
                (7, 1), (8, 1), (9, 1), (10, 1), (11, 1),
                (12, 1), (13, 1), (14, 1), (14, 2), (14, 3),
                (14, 4), (14, 5), (14, 6), (14, 7), (13, 7),
                (8, 7)  # Position finale pour rentrer dans la maison
            ],
            "yellow": [
                # Départ jaune (6, 13) et parcours
                (6, 13), (5, 14), (4, 14), (3, 14), (2, 14),
                (1, 14), (1, 13), (1, 12), (1, 11), (1, 10),
                (1, 9), (1, 8), (1, 7), (1, 6), (2, 6),
                (3, 6), (4, 6), (5, 6), (6, 5), (6, 4),
                (6, 3), (6, 2), (6, 1), (7, 1), (8, 1),
                (9, 1), (10, 1), (11, 1), (12, 1), (13, 1),
                (14, 1), (14, 2), (14, 3), (14, 4), (14, 5),
                (14, 6), (13, 7), (12, 7), (11, 7), (10, 7),
                (9, 7), (8, 7), (7, 7), (7, 8), (7, 9),
                (7, 10), (7, 11), (7, 12), (7, 13), (7, 14),
                (7, 7)  # Position finale pour rentrer dans la maison
            ]
        }
        
        # Si la position dépasse la longueur du chemin, retourner la dernière position
        if path_position >= len(paths[color]):
            return paths[color][-1]
        
        return paths[color][path_position]
    
    def next_player(self):
        """Passe au joueur suivant"""
        # Réinitialiser l'état du canevas
        self.canvas.unbind("<Button-1>")
        self.canvas.delete("highlight")
        
        # Si le joueur a fait 6, il rejoue (mais seulement s'il n'a pas déjà rejoué 3 fois)
        if self.dice_value == 6:
            # Pour éviter les boucles infinies, on limite à 3 lancers consécutifs
            if hasattr(self, 'consecutive_sixes') and self.consecutive_sixes < 3:
                self.show_status_message(f"Vous avez fait 6, vous rejouez! (Tour {self.consecutive_sixes})")
                # Réactiver le bouton de dé pour le même joueur
                self.dice_button.config(state=tk.NORMAL)
                # Mettre à jour l'interface
                self.update_ui()
                return
            else:
                # Reset compteur après 3 six consécutifs
                self.consecutive_sixes = 0
        else:
            # Réinitialiser le compteur de 6 consécutifs
            self.consecutive_sixes = 0
        
        # Passer au joueur suivant
        self.current_player = (self.current_player + 1) % len(self.players)
        
        # Mettre à jour l'interface
        self.update_ui()
        
        # Réactiver le bouton de dé pour le joueur humain
        player = self.players[self.current_player]
        if player["type"] == "human":
            self.dice_button.config(state=tk.NORMAL)
            color_names = {"red": "Rouge", "green": "Vert", "blue": "Bleu", "yellow": "Jaune"}
            self.show_status_message(f"C'est à votre tour, joueur {color_names[player['color']]}!")
        else:
            # Si le prochain joueur est une IA, jouer automatiquement après un délai
            self.dice_button.config(state=tk.DISABLED)  # Désactiver le bouton pendant que l'IA joue
            color_names = {"red": "Rouge", "green": "Vert", "blue": "Bleu", "yellow": "Jaune"}
            self.show_status_message(f"L'ordinateur {color_names[player['color']]} va jouer...")
            self.root.after(1500, self.roll_dice)
    
    def update_ui(self):
        """Met à jour l'interface utilisateur"""
        if not self.game_started:
            self.dice_text.set("Dé: -")
            self.player_text.set("Joueur: -")
            return
            
        player = self.players[self.current_player]
        color_names = {
            "red": "Rouge",
            "green": "Vert",
            "blue": "Bleu",
            "yellow": "Jaune"
        }
        
        # Mettre à jour le texte du joueur actuel
        if player["type"] == "human":
            self.player_text.set(f"Joueur: {color_names[player['color']]}")
        else:
            self.player_text.set(f"Ordinateur: {color_names[player['color']]}")
        
        # Mettre à jour la couleur de fond du label du joueur
        self.player_label.config(bg=self.colors[player["color"]])
        
        # Ajuster la couleur du texte pour assurer la lisibilité
        text_color = "black" if player["color"] in ["green", "yellow"] else "white"
        self.player_label.config(fg=text_color)
    
    def end_game(self, winner_index):
        """Termine la partie avec un gagnant"""
        winner = self.players[winner_index]
        color_names = {
            "red": "Rouge",
            "green": "Vert",
            "blue": "Bleu",
            "yellow": "Jaune"
        }
        
        # Message de félicitations
        victory_message = f"🎉 FÉLICITATIONS ! 🎉\n\nLe joueur {color_names[winner['color']]} a gagné !"
        
        if winner["type"] == "human":
            victory_message += "\n\nBravo, vous avez battu les ordinateurs !"
        else:
            victory_message += "\n\nL'ordinateur vous a battu. Meilleure chance la prochaine fois !"
            
        messagebox.showinfo("Fin de la partie", victory_message)
        
        # Désactiver le bouton de dé
        self.dice_button.config(state=tk.DISABLED)
        self.game_started = False
        
        # Montrer un message dans le label de statut
        self.show_status_message(f"Partie terminée! {color_names[winner['color']]} a gagné!", duration=-1)


def main():
    root = tk.Tk()
    root.title("Jeu de Ludo")
    
    # Centrer la fenêtre sur l'écran
    window_width = 800
    window_height = 750
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    game = LudoGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()