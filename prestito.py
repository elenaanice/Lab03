class Prestito:
    def __init__(self, codice, data, id_strumento, cognome_allievo):
        self.codice = codice
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"Prestito {self.codice}: Strumento {self.id_strumento} a {self.cognome_allievo} il {self.data}"

    def __repr__(self):
        return self.__str__()
