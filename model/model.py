from database.dao import  DAO
import networkx as nx

class Model:

    def __init__(self):
        self.G= nx.Graph()
        self.id_map = {}

    def get_graph(self, durata):

        secondi= durata * 60
        millisecondi= secondi * 1000

        lista_nodi= DAO.get_nodes(millisecondi)

        for nodo in lista_nodi:
            self.id_map[nodo[0]] = nodo[1]
            self.G.add_node(nodo[0])

        lista_edges= DAO.get_edges(millisecondi)

        for arco in lista_edges:
            if arco not in self.G.edges():
                self.G.add_edge(arco[0], arco[1])

        return self.G

    def get_connected_components(self,nodo):

        connections= nx.node_connected_component(self.G,nodo)

        contatore_componenti=0

        contatore_minuti=0

        self.dizionario_connessi={}

        for el in connections:

            contatore_componenti +=1

            contatore_minuti += sum(DAO.get_connected_time(el)) #cosi non da errore per il decimal[...]

            self.dizionario_connessi[el]= sum(DAO.get_connected_time(el))

        return contatore_minuti, contatore_componenti




    def call_ricorsione(self, album_partenza, dTOT):

        self.album_iniziale = set(nx.node_connected_component(self.G, album_partenza))
        best_cammino, best_durata_cammino, best_durata = self.ricorsione(dTOT, album_partenza, [album_partenza],0)


        return best_cammino, best_durata_cammino, best_durata



    def ricorsione(self, dTOT, album_corrente, lista_parziale, somma_durata_album):

        somma_corrente = somma_durata_album + self.dizionario_connessi[album_corrente]

        best_cammino = lista_parziale
        best_durata_cammino=len(lista_parziale)
        best_durata= somma_corrente

        for nodo in self.G.neighbors(album_corrente):

            if nodo in self.album_iniziale and nodo not in lista_parziale:


                nuova_somma= somma_corrente + self.dizionario_connessi[nodo]

                if nuova_somma > dTOT:
                    continue

                cammino, durata_cammino, durata =self.ricorsione( dTOT, nodo, lista_parziale + [nodo], somma_corrente)

                if durata > best_durata or (durata == best_durata and durata_cammino > best_durata_cammino):

                    best_cammino = cammino
                    best_durata_cammino = len(cammino)
                    best_durata= durata


            else:
                continue

        return best_cammino, best_durata_cammino, best_durata











