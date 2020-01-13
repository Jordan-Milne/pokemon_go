import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn_pandas import DataFrameMapper, CategoricalImputer, FunctionTransformer
from sklearn.preprocessing import StandardScaler, LabelBinarizer, PolynomialFeatures
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectPercentile
from sklearn.pipeline import make_pipeline
import catboost as cb

import pickle


df = pd.read_csv('data/pokemon_go.csv')

target = 'pokedex_id'
y = df[target]
X = df.drop(target, axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

df.info()

mapper = DataFrameMapper([
     # ('latitude',[CategoricalImputer(), LabelBinarizer()]),
     # ('longitude',[CategoricalImputer(), LabelBinarizer()]),
     # (['local_time'],[SimpleImputer(), StandardScaler()]),
     (['close_to_water'], StandardScaler()),
     ('city',LabelBinarizer()),
     ('weather',LabelBinarizer()),
     (['temperature'],StandardScaler()),
     (['population_density'], StandardScaler()),
     ], df_out=True)

Z_train = mapper.fit_transform(X_train)
Z_test = mapper.transform(X_test)

select = SelectPercentile(percentile=40)
select.fit(Z_train, y_train)
Z_train = select.transform(Z_train)
Z_test = select.transform(Z_test)


model = LogisticRegression(solver='lbfgs')
model.fit(Z_train, y_train)
model.predict(X_test)

# model = cb.CatBoostClassifier(
#     iterations=100,
#     learning_rate=0.5,
# )
#
# model.fit(
#     Z_train, y_train,
#     eval_set=(Z_test, y_test),
#     verbose=False,
#     plot=False,
# )

model.score(Z_test, y_test)


# pipe = make_pipeline(mapper, model)
# pipe.fit(X_train, y_train)
# pipe.score(X_test, y_test)
# pickle.dump(pipe, open('pipe.pkl', 'wb'))
