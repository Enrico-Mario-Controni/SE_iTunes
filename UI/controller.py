import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        try:
            durata= int(self._view.txt_durata.value)
            self.grafo= self._model.get_graph(durata)
            self._view.lista_visualizzazione_1.clean()
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f"numero nodi: {self.grafo.number_of_nodes()}\n "
                                                               f"numero archi: {self.grafo.number_of_edges()}"))


            self._view.dd_album.options=[ft.dropdown.Option(text=self._model.id_map[nodo], key=nodo) for nodo in self.grafo.nodes()]

            self._view.page.update()

        except ValueError:
            self._view.lista_visualizzazione_1.clean()
            self._view.lista_visualizzazione_1.controls.append(ft.Text("Numero non valido"))
            self._view.page.update()



    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        # TODO

        self.valore=int(self._view.dd_album.value)

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        # TODO
        contatore_minuti, contatore_componenti= self._model.get_connected_components(self.valore)

        self._view.lista_visualizzazione_2.clean()


        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"numero componenti connesse: {contatore_componenti}\n"
                                                                    f"minuti totali: {contatore_minuti} "))

        self._view.page.update()



    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO
        try:
            dTOT= int(self._view.txt_durata_totale.value)
            best_cammino, best_durata_cammino, best_durata= (self._model.call_ricorsione(self.valore, dTOT))
            self._view.lista_visualizzazione_3.clean()
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f"travati {best_durata_cammino} album, con durata massima {best_durata}"))
            for el in best_cammino:
                self._view.lista_visualizzazione_3.controls.append(ft.Text(f"-{self._model.id_map[el]}"))

            self._view.page.update()

        except ValueError:
            self._view.lista_visualizzazione_3.clean()
            self._view.lista_visualizzazione_3.controls.append(ft.Text("Numero non valido"))
            self._view.page.update()
