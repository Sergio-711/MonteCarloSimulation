import matplotlib.pyplot as plt
import sys
import copy
import tkinter as tk
from tkinter import ttk

from Game import Game
from Team import Team
from MainWindow import MainWindow

class Montecarlo:
    """
    Clase que representa un simulador de juegos Montecarlo.
    """

    def __init__(self):
        """
        Inicializa un nuevo simulador Montecarlo.
        """
        self.teams = []
        self.teams.append(Team("A"))
        self.teams.append(Team("B"))
        self.winsByGender = {"W": 0, "M": 0}
        self.scoresHistory = []
        self.games = []

        # Configurar la figura y los ejes para las gráficas
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))

        # Configurar la gráfica de barras para winsByGender
        self.ax1.bar(self.winsByGender.keys(), self.winsByGender.values())
        self.ax1.set_xlabel('Género')
        self.ax1.set_ylabel('Victorias')
        self.ax1.set_title('Victorias por Género')

        # Configurar la gráfica para el historial de puntuaciones por jugador
        self.ax2.set_xlabel('Juego')
        self.ax2.set_ylabel('Puntuación final')
        self.ax2.set_title('Historial de puntuaciones por jugador')

    def startSimulation(self):
        """
        Inicia una nueva simulación Montecarlo, creando 20000 juegos.

        Realiza dos juegos y cuenta las victorias por género.
        """
        for i in range(0, 20000):
            game = Game(self.teams, i + 1)
            game.simulateGame()
            self.games.append(copy.deepcopy(game))
            self.increaseWinsByGender(game.winsByGender)            
            self.updateWinsByGenderGraph()
            self.teams = game.teams
            self.updateScoresHistory()
            self.plotScores(self.ax2)
        plt.show(block=True)

    def increaseWinsByGender(self, winsByGender):
        """
        Aumenta en 1 las victorias por género en el juego actual, si no hay empate.

        Args:
            winsByGender (dict): Diccionario con las victorias por género en el juego.
        """
        max_wins = max(winsByGender.values())
        if list(winsByGender.values()).count(max_wins) == 1:
            max_gender = max(winsByGender, key=winsByGender.get)
            self.winsByGender[max_gender] += 1

    
    def updateScoresHistory(self):
        """
        Actualiza el historial de puntuaciones de los jugadores después de cada juego.
        """
        scoresTeamA = [player.finalScore for player in self.teams[0].players]
        scoresTeamB = [player.finalScore for player in self.teams[1].players]
        self.scoresHistory.append((scoresTeamA, scoresTeamB))

    def updateWinsByGenderGraph(self):
        """
        Actualiza y muestra la gráfica de barras para winsByGender.
        """
        self.ax1.clear()
        self.ax1.bar(self.winsByGender.keys(), self.winsByGender.values())
        self.ax1.set_xlabel('Género')
        self.ax1.set_ylabel('Victorias')
        self.ax1.set_title('Victorias por Género')

        # Actualizar la gráfica
        self.fig.canvas.draw()
        plt.pause(0.01)
    
    def plotScores(self, ax):
        """
        Grafica el historial de puntuaciones de los jugadores después de cada juego.
        """
        ax.clear()
        numPlayers = len(self.teams[0].players)
        for i in range(numPlayers):
            playerScoresTeamA = [game_scores[0][i] for game_scores in self.scoresHistory]
            playerScoresTeamB = [game_scores[1][i] for game_scores in self.scoresHistory]
            ax.plot(range(1, len(playerScoresTeamA) + 1), playerScoresTeamA, label=f"Team A - Player {i+1}")
            ax.plot(range(1, len(playerScoresTeamB) + 1), playerScoresTeamB, label=f"Team B - Player {i+1}")

        ax.set_xlabel("Juego")
        ax.set_ylabel("Puntuación final")
        ax.set_title("Historial de puntuaciones por jugador")
        ax.legend()
        ax.grid(True)
        plt.draw()

def main():
    """
    Función principal para iniciar el simulador Montecarlo.
    """
    monteCarlo = Montecarlo()
    monteCarlo.startSimulation()
    app = tk.Tk()
    window = MainWindow(app, monteCarlo.games)
    # No necesitas llamar a window.pack()
    window.lift()  # Opcional: mostrar la ventana al frente
    app.mainloop()

if __name__ == "__main__":
    main()
