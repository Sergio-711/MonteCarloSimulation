import taller_sc as pse

from Player import Player


class Team:
    """
    Clase que representa un equipo en un juego.

    Atributos:
        letter (str): Letra identificadora del equipo.
        players (list): Lista de jugadores que pertenecen al equipo.
        score (int): Puntuación total del equipo.
        roundsWon (int): Número de rondas ganadas por el equipo.
        finalGameWon (int): Número de juegos finales ganados por el equipo.
        scoreByRound (int): Puntuación acumulada en una ronda por el equipo.
    """

    def __init__(self, letter):
        """
        Inicializa un objeto Team con la letra identificadora dada.

        Args:
            letter (str): Letra identificadora del equipo.
        """
        self.letter = letter
        self.players = []
        for i in range(0, 5):
            resistance = int(25 +((45 - 25) * pse.numbersMonteCarlo.get()))
            self.players.append(Player(str(i + 1) + letter, resistance, 10, self.getGender()))
        self.score = 0
        self.roundsWon = 0
        self.finalGameWon = 0
        self.scoreByRound = 0
    
    def getGender(self):
        if pse.numbersMonteCarlo.get() < 0.5:
            return "W"
        return "M"
        

    def restartScoreByPlayer(self):
        """
        Reinicia la puntuación de los jugadores del equipo.
        """
        self.scoreByRound = 0
        for player in self.players:
            player.restartScore()

    def restartRoundsWon(self):
        """
        Reinicia el contador de rondas ganadas por el equipo.
        """
        self.roundsWon = 0

    def increaseWinCounter(self):
        """
        Incrementa el contador de juegos finales ganados por el equipo.
        """
        self.finalGameWon += 1

    def increaseRoundsWon(self):
        """
        Incrementa el contador de rondas ganadas por el equipo.
        """
        self.roundsWon += 1

    def increaseScore(self, score):
        """
        Incrementa la puntuación del equipo.

        Args:
            score (int): Puntuación a agregar.
        """
        self.scoreByRound += score
        self.score += score
    
    def restartScoreByGame(self ):
        """
        Reinicia las estadísticas de los jugadores del equipo.
        """
        for player in self.players:
            player.restartScoreByGame()

    def restartSkills(self ):
        """
        Reinicia las estadísticas de los jugadores del equipo.
        """
        for player in self.players:
            player.restartStats()

    def getLuckiestPlayer(self):
        """
        Devuelve el jugador más afortunado del equipo.

        Returns:
            Player: Objeto Player que representa al jugador más afortunado.
        """
        return max(self.players, key=lambda x: x.finalLuck)

    def printPlayers(self): #Temporal
        """
        Imprime las estadísticas de los jugadores del equipo.
        """
        for player in self.players:
            print(player.__str__())

    def __str__(self):
        print("Team: ",self.letter, " - score: ", self.score, "- scoreByRound: ", self.scoreByRound, "- roundsWon: ", self.roundsWon)
        self.printPlayers()