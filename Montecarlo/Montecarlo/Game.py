from Round import Round

class Game:
    """
    Clase que representa un juego entre equipos.
    """

    def __init__(self, teams, id):
        """
        Inicializa un nuevo juego con los equipos proporcionados.

        Args:
            teams (list): Lista de equipos participantes en el juego.
        """
        self.id = id
        self.teams = teams
        self.actualWinnerPlayer = None
        self.actualWinnerTeam = None
        self.winnerPlayer = None
        self.luckiestPlayer = None
        self.playerWithMostXP = None
        self.winsByGender = {"W": 0, "M": 0}

    def simulateGame(self):
        """
        Simula un juego completo.

        Realiza 10 rondas de juego, actualizando los equipos.
        """
        self.restartScoreByGame()
        for i in range(0, 10):
            round = Round(self.teams)
            self.actualWinnerPlayer = round.simulateRound()
            self.teams = round.teams
            self.increaseWinsByGender(self.actualWinnerPlayer)
            self.restartScoreByPlayer()
        self.getWinnerTeam()
        self.getWinnerPlayer()
        self.getLuckiestPlayer()
        self.getPlayerWithTheMostXP()
        self.restartSkills()

    def increaseWinsByGender(self, winner):
        """
        Incrementa el contador de victorias por género.

        Args:
            winner (Player): Jugador ganador de la ronda.
        """
        self.winsByGender[winner.gender] += 1

    def getWinnerTeam(self):
        """
        Determina el equipo ganador del juego.
        """
        aux = max(self.teams, key=lambda x: x.roundsWon)
        for team in self.teams:
            team.restartRoundsWon()
            if team.letter == aux.letter:
                self.actualWinnerTeam = aux
                team.increaseWinCounter()


    def getWinnerPlayer(self):
        """
        Determina al jugador ganador del juego.
        """
        aux = []
        for team in self.teams:
            aux.append(max(team.players, key=lambda x: x.wonRound))
        self.winnerPlayer = max(aux, key=lambda x: x.score)

    def getLuckiestPlayer(self):
        """
        Determina al jugador más afortunado del juego.
        """
        aux = []
        for team in self.teams:
            aux.append(team.getLuckiestPlayer())
        self.luckiestPlayer = max(aux, key=lambda x: x.finalLuck)

    def getPlayerWithTheMostXP(self):
        """
        Determina al jugador con más experiencia del juego.
        """
        aux = []
        for team in self.teams:
            aux.append(max(team.players, key=lambda x: x.experience))
        self.playerWithMostXP = max(aux, key=lambda x: x.experience)

    def restartScoreByPlayer(self):
        """
        Reinicia la puntuación de los jugadores de los equipos.
        """
        for team in self.teams:
            team.restartScoreByPlayer()

    def restartScoreByGame(self):
        for team in self.teams:
            team.restartScoreByGame()

    def restartSkills(self):
        """
        Reinicia las habilidades de los jugadores de los equipos.
        """
        for team in self.teams:
            team.restartSkills()

