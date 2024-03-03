import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from sklearn.ensemble import RandomForestClassifier as rfc
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
import MissingDict as md

class Predictor:
    
    def predict(self, pathToCsv, home, away, day_of_week, hour, is_home=True):
        matches = pd.read_csv(pathToCsv, index_col=0)
        matches['data'] = pd.to_datetime(matches['data'])
        matches['cod_time'] = matches['time'].astype('category').cat.codes
        matches['cod_local'] = matches['local'].astype('category').cat.codes
        matches['cod_opo'] = matches['oponente'].astype('category').cat.codes
        matches['hora'] = matches['horário'].str.replace(":\d+", "", regex=True).astype('int')
        matches['cod_dia'] = matches['data'].dt.dayofweek
        matches["target"] = (matches["resultado"] == "V").astype("int")
        
        predictors = ['cod_time', 'cod_local', 'cod_opo', 'hora', 'cod_dia']
        cols = ['gp', 'gc', 'tc', 'cag', 'dist', 'fk', 'pb', 'pt']
        new_cols = [f'{c}_rolling' for c in cols]

        matches_rolling = matches.groupby('time').apply(lambda x: self.rolling_averages(x, cols, new_cols))
        matches_rolling = matches_rolling.droplevel('time')
        matches_rolling.index = range(matches_rolling.shape[0])

        combined, precision, rf = self.make_predictions(matches_rolling, predictors)

        map_values = {
            "Vitoria Guimaraes": "Vitória",
            "Famalicao": "Famalicão",
            "Maritimo": "Marítimo",
            "Pacos de Ferreira": "Paços",
            "Belenenses SAD": "B-SAD",
            "Vitoria Setubal": "Vitória Setúbal"
        }
        mapping = md.MissingDict(**map_values)

        awayTeam = mapping[away]

        codTime = matches_rolling[matches_rolling['time'] == home]['cod_time'].unique()
        codOponente = matches_rolling[matches_rolling['oponente'] == awayTeam]['cod_opo'].unique()
        codDia = matches_rolling[matches_rolling['dia'] == day_of_week]['cod_dia'].unique()

        next_game = pd.DataFrame.from_dict(data={'cod_time': codTime, 'cod_local': [1 if home else 0], 'cod_opo': codOponente, 'hora': hour, 'cod_dia': codDia})

        real_pred = rf.predict(next_game)

        return True if real_pred[0] == 1 else False
        
    def rolling_averages(self, group, cols, new_cols):
        group = group.sort_values("data")
        rolling_stats = group[cols].rolling(3, closed='left').mean()
        group[new_cols] = rolling_stats
        group = group.dropna(subset=new_cols)

        return group
    
    def make_predictions(self, data, predictors):
        test_date = datetime.datetime.today() - relativedelta(months=3)
        train = data[data['data'] < test_date]
        test = data[data['data'] > test_date]

        rf = rfc(n_estimators=50, min_samples_split=10, random_state=1)
        rf.fit(train[predictors], train['target'])
        preds = rf.predict(test[predictors])
        combined = pd.DataFrame(dict(actual=test['target'], predictd=preds), index=test.index)
        precision = precision_score(test['target'], preds)

        return combined, precision, rf
    