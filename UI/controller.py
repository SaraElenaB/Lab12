import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self.anni = []
        self.nazioni = []

    #----------------------------------------------------------------------------------------------------------------------------------
    def fillDDYear(self):

        self.anni = self._model.getAllYears()
        for a in self.anni:
            self._view.ddyear.options.append( ft.dropdown.Option(a) )

    def fillDDNation(self):

        self.nazioni = self._model.getAllNazioni()
        for n in self.nazioni:
            self._view.ddcountry.options.append( ft.dropdown.Option(n))

    # ----------------------------------------------------------------------------------------------------------------------------------
    def handle_graph(self, e):

        anno = self._view.ddyear.value
        nazione = self._view.ddcountry.value

        if anno == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text( f"Attenzione, inserire un anno per continuare!"))
            self._view.update_page()
            return

        if nazione == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text( f"Attenzione, inserire una nazione per continuare!"))
            self._view.update_page()
            return

        self._model.buildGraph(anno, nazione)
        numNodi, numEdges = self._model.getDetailsGraph()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato!"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {numNodi} \nNumero di archi: {numEdges}"))
        self._view.update_page()

    # ----------------------------------------------------------------------------------------------------------------------------------
    def handle_volume(self, e):

        self._view.txtOut2.controls.clear()
        for t in self._model.getInfoVolumeVendita():
            self._view.txtOut2.controls.append( ft.Text( f"{t[0]} --> {t[1]}"))

        self._view.update_page()

    # ----------------------------------------------------------------------------------------------------------------------------------
    def handle_path(self, e):

        print("called function 1")
        numArchiMax = self._view.txtN.value
        if numArchiMax == "":
            self._view.txtOut3.controls.clear()
            self._view.txtOut3.controls.append( ft.Text( f"Attenzione, inserire una numero massimo di lunghezza di percorso per continuare!"))
            self._view.update_page()
            return

        try:
            numArchiMaxInt = int(numArchiMax)
        except ValueError:
            self._view.txtOut3.controls.clear()
            self._view.txtOut3.controls.append(ft.Text(f"Attenzione, inserire una numero intero di lunghezza di percorso per continuare!"))
            self._view.update_page()
            return

        if numArchiMaxInt < 2:
            self._view.txtOut3.controls.clear()
            self._view.txtOut3.controls.append( ft.Text(f"Attenzione, inserire una numero intero maggiore di 2 per continuare!"))
            self._view.update_page()
            return

        bestPath, bestCost = self._model.getCamminoOttimo(numArchiMaxInt)
        self._view.txtOut3.controls.clear()
        self._view.txtOut3.controls.append( ft.Text(f" E'stato trovato un cammino ottimo con costo massimo: {bestCost}"))
        for i in range( len(bestPath)-1 ):
            u = bestPath[i]
            v = bestPath[i+1]
            peso = self._model._grafo[u][v]["weight"]
            self._view.txtOut3.controls.append(ft.Text(f"{u} --> {v} : {peso}"))
        self._view.update_page()

    # ----------------------------------------------------------------------------------------------------------------------------------