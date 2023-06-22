import pandas as pd
from sklearn.tree import ExtraTreeRegressor
from tpot import TPOTRegressor  

class MLModel:
    def select_best_model(self, cv, X_train, y_train):
        """
        Utiliza AutoML para identificar o melhor modelo de regressão.
        :cv: define a validação cruzada
        :X_train: especificações da base de treino
        :y_train: variável alvo da base de treino (target)
        """

        # define busca do melhhor modelo de regressão
        model = TPOTRegressor(generations=5, 
                              population_size=50, 
                              scoring='r2', 
                              cv=cv,
                              verbosity=2,
                              random_state=1,
                              n_jobs=-1)
        model.fit(X_train, y_train)
        model.export('best_model.py')

        # Display resultados do AutoML
        resultado = pd.DataFrame(model.evaluated_individuals_)
        resultado.columns = list(map(lambda x: x[0], resultado.columns.str.split('(')))
        return print(resultado.T)
    
    def model_training(self, X_train, y_train):
        """
        Cria pipeline de treinamento do melhor modelo encontrado na etapa de busca.
        :X_train: especificações da base de treino
        :y_train: variável alvo da base de treino (target)
        """

        best_pipeline = ExtraTreeRegressor(bootstrap=False, 
                                            max_features=0.25,
                                            min_samples_leaf=1,
                                            min_samples_split=5,
                                            n_estimators=100)
        best_pipeline = best_pipeline.fit(X_train, y_train)
        return best_pipeline