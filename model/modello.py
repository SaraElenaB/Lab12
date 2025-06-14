import copy
import itertools
import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):

        self._grafo = nx.Graph()

        self._nodes=[]
        self._bestPath = []
        self._bestCost = 0

    # ----------------------------------------------------------------------------------------------------------------------------------
    def getAllYears(self):
        return DAO.getAllYears()

    def getAllNazioni(self):
        return DAO.getAllNazioni()

    # ----------------------------------------------------------------------------------------------------------------------------------
    def buildGraph(self, anno, nazione):

        self._grafo.clear()
        self._nodes = DAO.getAllNodes(nazione)
        self._grafo.add_nodes_from(self._nodes)

        for n1, n2 in itertools.combinations(self._nodes, 2):
            peso = DAO.getAllEdgesWeight(anno, n1.Retailer_code, n2.Retailer_code)
            if peso:
                self._grafo.add_edge(n1, n2, weight=peso[0])

        return self._grafo

    def getDetailsGraph(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    # ----------------------------------------------------------------------------------------------------------------------------------
    def getInfoVolumeVendita(self):

        listTuple=[]
        for nodo in self._grafo.nodes:
            volume = 0
            for vicino in self._grafo.neighbors(nodo):
                volume += self._grafo[nodo][vicino]["weight"]
            listTuple.append( (nodo, volume) )

        listTuple.sort( key = lambda x: x[1] , reverse=True )
        return listTuple

    # ----------------------------------------------------------------------------------------------------------------------------------
    def getCamminoOttimo(self, numArchiMax):

        self._bestPath = []
        self._bestCost = 0
        parziale = []

        for nodo in self._nodes:
            parziale.append(nodo)
            self._ricorsione( parziale, numArchiMax )
            parziale.pop()

        return self._bestPath, self._bestCost

    # ----------------------------------------------------------------------------------------------------------------------------------
    def _ricorsione(self, parziale, numArchiMax):

        #è ammissibile?
        if len(parziale) == numArchiMax+1: #archi = nodo+1
            if parziale[0] == parziale[-1]:
                # è la migliore?
                costo = int(self.getCosto(parziale))
                if costo > self._bestCost:
                    print(f"Soluzione migliore trovata")
                    self._bestCost = costo
                    self._bestPath = copy.deepcopy(parziale)
        else:
        #continua a cercare il migliore --> ricorsione
            ultimo = parziale[-1]
            for n in self._grafo.neighbors(ultimo):
                #vincoli
                if n == parziale[0] and len(parziale) == numArchiMax:
                    parziale.append(n)
                    self._ricorsione(parziale, numArchiMax)
                    parziale.pop()

                elif n not in parziale:
                    print(f"Ricorsione: {parziale}")
                    parziale.append(n)
                    self._ricorsione(parziale, numArchiMax)
                    parziale.pop()

    # ----------------------------------------------------------------------------------------------------------------------------------
    def getCosto(self, listaNodi):

        print("called funzione costo"
              "")
        costo=0
        for i in range( len(listaNodi)-1):
            if self._grafo.has_edge(listaNodi[i], listaNodi[i + 1]):
                costo += self._grafo[listaNodi[i]][listaNodi[i+1]]["weight"]
        return costo

    #----------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    m = Model()
    m.buildGraph( 2016, "Germany")
    print( m.getDetailsGraph())



