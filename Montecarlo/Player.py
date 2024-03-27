class Player:
    """
        clase que representa un jugador en el juego de arquería.

        Atributos:
            id (int): Identificador único del jugador.
            resistance (int): Resistencia actual del jugador.
            experience (int): Experiencia acumulada por el jugador.
            gender (str): Género del jugador.
            luck (int): Nivel de suerte del jugador.
            initialExperience (int): Experiencia inicial del jugador al inicio del juego.
            initialResistance (int): Resistencia inicial del jugador al inicio del juego.
            score (int): Puntuación total del jugador.
            roundResistance (int): Resistencia del jugador en una ronda particular.
            consecutiveShot (int): Número de tiros consecutivos por la suerte del jugador.
            bufferExperience (int): Experiencia acumulada para determinar si se pierde resistencia.
            remainingRoundsOfBonus (int): Número de rondas restantes con la disminución de resistencia en 1.
            wonRound (int): Número de rondas ganadas por el jugador.
            finalLuck (int): Nivel final de suerte alcanzado por el jugador.
            scoreByGame (int): Puntuación acumulada por el jugador en un juego.
            finalWonRound (int): Puntación de cada ronda ganada.
        """

    def __init__(self, id, resistance, experience, gender):
        """
            Inicializa un objeto Player con los atributos dados.

            Args:
                id (int): Identificador único del jugador.
                resistance (int): Resistencia inicial del jugador.
                experience (int): Experiencia inicial del jugador.
                gender (str): Género del jugador.
        """
        self.id = id
        self.resistance = resistance
        self.experience = experience
        self.luck = 0
        self.gender = gender
        self.initialExperience = experience
        self.initialResistance = resistance
        self.score = 0
        self.roundResistance = resistance
        self.consecutiveShot = 0
        self.bufferExperience = 0
        self.remainingRoundsOfBonus = 0
        self.wonRound = 0
        self.finalWonRound = 0
        self.finalLuck = 0
        self.scoreByGame = 0
        self.finalScore = 0


    def readjustResistance(self, loss):
        """
                Reduce la resistencia, conforme avanzan las rondas.

                Args: loss (int): la resistencia a disminuir del jugador

        """
        
        if self.remainingRoundsOfBonus > 0:
            self.roundResistance -= 1
            self.resistance = self.roundResistance
        else:
            self.roundResistance -= loss
            self.resistance = self.roundResistance


    def defineLuck(self, luck):
        """
        Define el nivel de suerte del jugador.

        Args:
            luck (int): Nivel de suerte.
        """
        self.luck = luck

    def increaseScore(self, score):
        """
        Incrementa la puntuación del jugador.

        Args:
            score (int): Puntuación a agregar.
        """
        self.score += score
        self.scoreByGame += score
        self.finalScore += score

    def decreaseResistance(self):
        """
                Reduce la resistencia del jugador con cada tiro.

                Returns:
                    bool: True si la resistencia se reduce satisfactoriamente, 
                    False si no se puede reducir más.
        """
        if self.resistance - 5 >= 0:
            self.resistance -= 5
            return True
        else:
            return False

    def increaseLuck(self):
        """
        Incrementa el nivel de suerte final del jugador.
        """
        self.finalLuck += 1

    def increaseConsecutiveShot(self):
        """
        Incrementa el número de tiros consecutivos exitosos del jugador.

        Returns:
            bool: True si se alcanza la tercera consecutiva, 
            False de lo contrario.
        """
        self.consecutiveShot += 1
        if self.consecutiveShot == 3:
            self.consecutiveShot = 0
            return True
        else:
            return False

    def increaseExperience(self):
        """
        Incrementa la experiencia del jugador después de ganar una ronda, 
        además valida los puntos de XP actuales.
        """
        self.finalWonRound += 1
        self.wonRound += 1
        self.experience += 3
        self.bufferExperience += 3
        if self.bufferExperience == 9:
            self.remainingRoundsOfBonus = 3
            self.bufferExperience = 0

    def updateBonus(self):
        """
        Actualiza la variable de Bonus conforme pasan las rondas.
        """
        if self.remainingRoundsOfBonus > 0:
            self.remainingRoundsOfBonus -= 1


    def simulateShot(self, score, status = True):
        """
        Simula un tiro en el juego y actualiza el estado del jugador.

        Args:
            score (int): Puntuación obtenida en el tiro.
            status (bool): Opcional, valida si el resultado se le va 
                a sumar al score individual

        Returns:
            bool: True si el tiro fue exitoso y la resistencia se reduce 
            (si corresponde), False de lo contrario.
        """
        if self.decreaseResistance() and status:
            self.increaseScore(score)
            return True
        elif self.decreaseResistance():
            return True
        else:
            return False

    def restartScore(self):
        """
        Reinicia la puntuación del jugador después de cada ronda.
        """
        self.score = 0

    def restartConsecutiveShot(self):
        """
        Reinicia el contador de tiros consecutivos del jugador.
        """
        self.consecutiveShot = 0

    def restartStats(self):
        """
                Reinicia todas las estadísticas del jugador 
                al inicio de un nuevo juego.
        """
        self.wonRound = 0
        self.experience = self.initialExperience
        self.resistance = self.initialResistance
        self.roundResistance = self.initialResistance
        self.consecutiveShot = 0
        self.bufferExperience = 0
        self.finalLuck = 0
        self.remainingRoundsOfBonus = 0
    
    def restartScoreByGame(self):        
        self.scoreByGame = 0

    def __str__(self):
        return "id ", self.id, " - resistance ", self.resistance, " - score ", self.score, " - experience ", self.experience, " - gender ", self.gender, " - bufferExperience ", self.bufferExperience, " - remainingRounds ", self.remainingRoundsOfBonus, " - consecutive", self.consecutiveShot, " - luck", self.luck, " - roundsWon", self.wonRound, "- finalLuck", self.finalLuck, "- scoreByGame", self.scoreByGame, " - totalRoundsWon", self.finalWonRound, " - finalScore", self.finalScore
