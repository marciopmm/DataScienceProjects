if __name__ == '__main__':
    import RuiRijoScraping

    url = 'https://www.ruirijo.pt/veiculos/carros/usados/'
    ruiRijo = RuiRijoScraping.RuiRijoScraping(url)
    soup = ruiRijo.get_data()