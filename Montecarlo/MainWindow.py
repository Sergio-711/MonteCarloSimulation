import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import ttk

class MainWindow(tk.Toplevel):
    """
    Clase para la ventana principal de la aplicación del simulador Montecarlo.
    """

    def __init__(self, parent, games):
        """
        Inicializa la ventana principal.

        Args:
            parent: El widget padre al que pertenece esta ventana.
            games (list): Lista de objetos Game que representan los juegos simulados.
        """
        super().__init__(parent)
        self.title("Simulador Montecarlo")
        self.geometry("400x200")

        self.games = games

        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Combo box para seleccionar el juego
        self.gameComboBox = ttk.Combobox(main_frame, values=["Juego " + str(game.id) for game in self.games])
        self.gameComboBox.pack()

        # Botón para mostrar información del juego seleccionado
        self.acceptButton = ttk.Button(main_frame, text="Mostrar", command=self.start_graph)
        self.acceptButton.pack()

        # Etiquetas para mostrar información del juego seleccionado
        self.winnerLabel = ttk.Label(main_frame, text="")
        self.winnerLabel.pack()
        self.winnerPlayerLabel = ttk.Label(main_frame, text="")
        self.winnerPlayerLabel.pack()
        self.luckiestLabel = ttk.Label(main_frame, text="")
        self.luckiestLabel.pack()
        self.mostExperienceLabel = ttk.Label(main_frame, text="")
        self.mostExperienceLabel.pack()

    def start_graph(self):
        """
        Método para mostrar información y gráficas del juego seleccionado en el combo box.
        """
        selectedGame = self.gameComboBox.get()
        aux = selectedGame.split(" ")
        actualGame = next((game for game in self.games if game.id == int(aux[1])), None)
        if actualGame:
            # Obtener los scoreByGame de los jugadores del actualGame
            scoreByGameTeamA = [player.scoreByGame for player in actualGame.teams[0].players]
            scoreByGameTeamB = [player.scoreByGame for player in actualGame.teams[1].players]

            # Mostrar el equipo ganador
            winner = "Empate" if actualGame.actualWinnerTeam == "" else f"Equipo ganador: {actualGame.actualWinnerTeam.letter}"
            self.winnerLabel.config(text=winner)

            # Mostrar al jugador ganador
            winnerPlayer = actualGame.winnerPlayer
            self.winnerPlayerLabel.config(text="El jugador ganador fue: " + winnerPlayer.id)

            # Mostrar al jugador con más suerte
            luckiestOne = actualGame.luckiestPlayer
            self.luckiestLabel.config(text="El jugador con más suerte: " + luckiestOne.id)

            # Mostrar al jugador con más experiencia
            mostXP = actualGame.playerWithMostXP
            self.mostExperienceLabel.config(text="El jugador con más experiencia: " + mostXP.id)

            # Obtener los nombres de los jugadores
            playerNamesA = [f"Jugador {i+1}" for i in range(len(scoreByGameTeamA))]
            playerNamesB = [f"Jugador {i+1}" for i in range(len(scoreByGameTeamB))]

            # Crear la figura y los subplots para las dos gráficas
            fig, axs = plt.subplots(2)

            # Graficar los scoreByGame del equipo A
            axs[0].bar(playerNamesA, scoreByGameTeamA)
            axs[0].set_title("Score por juego - Equipo A")
            axs[0].set_xlabel("Jugador")
            axs[0].set_ylabel("Score")

            # Graficar los scoreByGame del equipo B
            axs[1].bar(playerNamesB, scoreByGameTeamB)
            axs[1].set_title("Score por juego - Equipo B")
            axs[1].set_xlabel("Jugador")
            axs[1].set_ylabel("Score")

            # Ajustar el espacio entre subplots
            plt.tight_layout()

            # Mostrar las gráficas
            plt.show()
        else:
            print("No se encontró el juego seleccionado.")
