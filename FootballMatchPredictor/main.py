from Portugal_WebScrapper import Portugal_WebScrapper
from Predictor import Predictor
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--home', type=str, help="Home Team - it must be one of the following list: ['Sporting CP', 'Benfica', 'Porto', 'Braga', 'Vitoria Guimaraes', 'Moreirense', 'Arouca', 'Farense', 'Famalicao', 'Gil Vicente FC', 'Portimonense', 'Boavista', 'Casa Pia', 'Estoril', 'Estrela', 'Rio Ave', 'Chaves', 'Vizela', 'Maritimo', 'Pacos de Ferreira', 'Santa Clara', 'Tondela', 'Belenenses SAD', 'Nacional', 'Vitoria Setubal', 'Aves']")
    parser.add_argument('--away', type=str, help="Away Team - it must be one of the following list: ['Sporting CP', 'Benfica', 'Porto', 'Braga', 'Vitoria Guimaraes', 'Moreirense', 'Arouca', 'Farense', 'Famalicao', 'Gil Vicente FC', 'Portimonense', 'Boavista', 'Casa Pia', 'Estoril', 'Estrela', 'Rio Ave', 'Chaves', 'Vizela', 'Maritimo', 'Pacos de Ferreira', 'Santa Clara', 'Tondela', 'Belenenses SAD', 'Nacional', 'Vitoria Setubal', 'Aves']")
    parser.add_argument('--day', type=str, help='Day of week when match will be played ("dom", "seg", "ter", "qua", "qui", "sex", "sáb")')
    parser.add_argument('--hour', type=int, help='Hour when match will be played')
    parser.add_argument('--download', action='store_true', help='Flag to download data from fbref.com')
    
    try:
        args = parser.parse_args()
    except argparse.ArgumentTypeError as e:
        print(f"Invalid argument: {e}")
        exit()

    pathToCsv = 'portugal_matches.csv'
    
    if args.download == True:
        try:
            ws = Portugal_WebScrapper(pathToCsv)            
            ws.get_data()
        except:
            print('Error while getting data')
            exit()
        
    predictor = Predictor()

    try:
        resultHome = predictor.predict(pathToCsv, args.home, args.away, args.day, args.hour, is_home=True)
    except Exception as e:
        print(f"Invalid home team name: {e}")
        exit()

    try:
        resultAway = predictor.predict(pathToCsv, args.away, args.home, args.day, args.hour, is_home=False)
    except:
        print(f"Invalid away team name: {e}")
        exit()

    if resultHome:
        if resultAway:
            print(f'{args.home} vs {args.away} - Draw')
        else:            
            print(f'{args.home} vs {args.away} - {args.home} Wins')cs
    else:
        if resultAway:
            print(f'{args.home} vs {args.away} - {args.away} Wins')            
        else:
            print(f'{args.home} vs {args.away} - Draw')

