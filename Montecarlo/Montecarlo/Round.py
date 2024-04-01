import taller_sc as pse


class Round:
    """
        Clase que representa una ronda de un juego entre equipos.
    """

    def __init__(self, teams):
        """
            Inicializa una nueva ronda con los equipos proporcionados.

            Args:
                teams (list): Lista de equipos participantes en la ronda.
        """
        self.teams = teams
        self.womenScore = {0.3: 10,
                           0.68: 9,
                           0.95: 8,
                           1: 0}
        self.menScore = {0.2: 10,
                         0.53: 9,
                         0.93: 8,
                         1: 0}

    def simulateRound(self):
        """
        Simula una ronda del juego.

        Returns:
            Player: El jugador ganador de la ronda.
        """
        #print("------------------------Nuevo Round---------------")
        winnerPlayers = []
        for team in self.teams:
            team = self.updateLuckAndBonus(team)
            luckiestOne = team.players[self.getMaxLuck(team.players)]
            luckiestOne.increaseLuck()
            luckiestOne, team = self.validateLuckiestShot(luckiestOne, team)
            team.players[self.getIndex(luckiestOne)] = luckiestOne
            team = self.playRound(team)
            max_score_player = max(team.players, key=lambda x: x.score)
            winnerPlayers.append(max_score_player)
        self.setWinnerTeam()
        winnerPlayers = self.checkScores(winnerPlayers)
        winnerPlayers[0].increaseExperience()
        self.updateData(winnerPlayers)
        return winnerPlayers[0]

    def updateLuckAndBonus(self, team):
        """
        Actualiza la suerte y los bonos de los jugadores en el equipo.

        Args:
            team (Team): Equipo al que pertenecen los jugadores.

        Returns:
            Team: Equipo actualizado.
        """
        for player in team.players:
            player.updateBonus()
            player.defineLuck(1 + ((3-1)* pse.numbersMonteCarlo.get()) )
        return team

    def getMaxLuck(self, players):
        """
        Obtiene el índice del jugador con la mayor suerte en el equipo.

        Args:
            players (list): Lista de jugadores del equipo.

        Returns:
            int: Índice del jugador con la mayor suerte.
        """
        aux = 0
        pos = 0
        for i in range(len(players)):
            if players[i].luck > aux:
                aux = players[i].luck
                pos = i
        return pos

    def validateLuckiestShot(self, luckiestOne, team):
        """
        Valida el tiro del jugador más afortunado.

        Args:
            luckiestOne (Player): Jugador más afortunado.
            team (Team): Equipo al que pertenece el jugador.

        Returns:
            tuple: Tupla que contiene al jugador más afortunado actualizado y al equipo actualizado.
        """
        if luckiestOne.consecutiveShot == 0:
            for player in team.players:
                player.restartConsecutiveShot()
            luckiestOne.increaseConsecutiveShot()
            auxScore = self.getScore(luckiestOne.gender)
            if luckiestOne.simulateShot(auxScore, False):
                    team.increaseScore(auxScore)
        else:
            auxScore = self.getScore(luckiestOne.gender)
            if luckiestOne.increaseConsecutiveShot():
                team.increaseScore(auxScore)
            else:
                if luckiestOne.simulateShot(auxScore, False):
                    team.increaseScore(auxScore)
        return luckiestOne, team

    def getScore(self, gender):
        """
        Obtiene la puntuación de un tiro para un género específico.

        Args:
            gender (str): Género del jugador ("W" para mujer, "M" para hombre).

        Returns:
            int: Puntuación del tiro.
        """
        
        shot = pse.numbersMonteCarlo.get()
        if gender == "W":
            for prob, score in sorted(self.womenScore.items()):
                if shot <= prob:
                    return score
        else:
            for prob, score in sorted(self.menScore.items()):
                if shot <= prob:
                    return score

    def getIndex(self, luckiestOne):
        """
        Obtiene el índice del jugador en la lista de jugadores.

        Args:
            luckiestOne (Player): Jugador cuyo índice se desea obtener.

        Returns:
            int: Índice del jugador en la lista de jugadores.
        """
        return int(luckiestOne.id[0]) - 1

    def playRound(self, team):
        """
        Simula el juego de una ronda para un equipo.

        Args:
            team (Team): Equipo que participa en la ronda.

        Returns:
            Team: Equipo actualizado después de la ronda.
        """
        for player in team.players:
            score = self.getScore(player.gender)
            while player.simulateShot(score):
                team.increaseScore(score)
                score = self.getScore(player.gender)
            result = 2
            if(pse.numbersMonteCarlo.get() < 0.5):
                result = 1
            player.readjustResistance(result)
        return team



    def setWinnerTeam(self):
        """
        Establece el equipo ganador de la ronda.
        """
        aux = max(self.teams, key=lambda x: x.score)
        for team in self.teams:
            if team.letter == aux.letter:
                team.increaseRoundsWon()


    def checkScores(self, winnerPlayers):
        """
        Comprueba la puntuación de los jugadores ganadores.

        Args:
            winnerPlayers (list): Lista de jugadores ganadores.

        Returns:
            list: Lista de jugadores ganadores ordenada por puntuación.
        """
        if winnerPlayers[0].score > winnerPlayers[1].score:
            return [winnerPlayers[0], winnerPlayers[1]]
        elif winnerPlayers[0].score < winnerPlayers[1].score:
            return [winnerPlayers[1], winnerPlayers[0]]
        else:
            for player in winnerPlayers:
                player.increaseScore(self.getScore(player.gender))
            return self.checkScores(winnerPlayers)


    def updateData(self, winnerPlayers):
        """
        Actualiza los datos del equipo con los jugadores ganadores.

        Args:
            winnerPlayers (list): Lista de jugadores ganadores.
        """
        for team in self.teams:
            for i, player in enumerate(team.players):
                for winner in winnerPlayers:
                    if player.id == winner.id:
                        team.players[i] = winner