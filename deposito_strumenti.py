import csv
from operator import attrgetter

from strumento import Strumento
from prestito import Prestito

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = {}
        self.prestiti = {}
        self._ultimo_id_strumento = 0
        self._ultimo_id_prestito = 0

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            with open(file_path, "r", encoding='utf-8') as file:
                reader = csv.reader(file)
                for riga in reader:
                    if not riga:
                        continue
                    codice, tipo, marca, anno, valore = [campo.strip() for campo in riga]

                    strumento = Strumento(codice, tipo, marca, anno, valore)
                    self.strumenti[codice] = strumento

                    if codice.startswith('S') and codice[1:].isdigit():
                        num = int(codice[1:])
                        if num > self._ultimo_id_strumento:
                            self._ultimo_id_strumento = num
        except FileNotFoundError:
            return FileNotFoundError(f"Errore: File '{file_path}' non trovato.")


    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        self._ultimo_id_strumento += 1
        codice = "S" + str(self._ultimo_id_strumento)

        nuovo_strumento = Strumento(codice, tipo, marca, anno_acquisto, valore)
        self.prestiti[codice] = nuovo_strumento
        return nuovo_strumento


    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        lista_strumenti = list(self.strumenti.values())
        return sorted(lista_strumenti, key=attrgetter('marca'))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        if id_strumento not in self.strumenti:
            raise Exception(f"Errore: Lo strumento con codice '{id_strumento}' non esiste nel sistema.")

        for prestito in self.prestiti.values():
            if prestito.id_strumento == id_strumento:
                raise Exception(f"Errore: Lo strumento '{id_strumento}' è già attualmente in prestito.")

        self._ultimo_id_prestito += 1
        codice_prestito = "P" + str(self._ultimo_id_prestito)

        prestito = Prestito(codice_prestito, data, id_strumento, cognome_allievo)
        self.prestiti[codice_prestito] = prestito
        return prestito


    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        if id_prestito not in self.prestiti:
            raise Exception(f"Errore: Il prestito con codice '{id_prestito}' non esiste.")

