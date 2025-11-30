import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from imblearn.pipeline import Pipeline # indispensable pour SMOTE
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    StandardScaler, OneHotEncoder, FunctionTransformer
)
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv("CHD.csv", sep=';')

df.head()
df.info()
df.describe()
sns.countplot(x='famhist', data=df)
plt.title("Distribution de la variable famhist")
plt.show()
plt.figure(figsize=(10,5))
sns.heatmap(df.isna(), cbar=False)
plt.title("Visualisation des valeurs manquantes")
plt.show()
# Séparation des variables explicatives et de la cible
X = df.drop("chd", axis=1)
y = df["chd"]

X.head(), y.head()
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.33,
    random_state=123,
    stratify=y # PRECISER QUE X TRAIN XTEST CONTIENT LA MEME REPARTITION QUE LA BASE INTIALE
)

X_train.shape, X_test.shape
numeric_features = ['sbp','ldl','adiposity','obesity','age']
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Pipeline numérique
numeric_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler())
])

numeric_pipeline
# Uniformisation des catégories
df["famhist"] = df["famhist"].str.lower()
df["famhist"] = df["famhist"].str.capitalize()   # donne 'Present' ou 'Absent'
df["famhist"].value_counts()
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

categorical_features = ["famhist"]

categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

categorical_pipeline
from sklearn.compose import ColumnTransformer

numeric_features = ['sbp','ldl','adiposity','obesity','age']
categorical_features = ['famhist']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_pipeline, numeric_features),
        ('cat', categorical_pipeline, categorical_features)
    ]
)

preprocessor
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
model_pca = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("pca", PCA(n_components=5)),
    ("logreg", LogisticRegression(max_iter=1000))
])
model_pca.fit(X_train, y_train)
y_pred_pca = model_pca.predict(X_test)
# On applique seulement le préprocesseur sur les données d’entraînement
X_train_transformed = preprocessor.fit_transform(X_train)
from sklearn.decomposition import PCA

pca = PCA()
pca.fit(X_train_transformed)
pca.explained_variance_ratio_
import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))
plt.plot(np.cumsum(pca.explained_variance_ratio_), marker='o')
plt.xlabel("Nombre de composantes")
plt.ylabel("Cumul de variance expliquée")
plt.title("Cumul de variance expliquée par l'ACP")
plt.grid()
plt.show()
cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
n_components_90 = np.argmax(cumulative_variance >= 0.90) + 1

n_components_90
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

model_no_pca = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("logreg", LogisticRegression(max_iter=1000))
])
model_no_pca.fit(X_train, y_train)
y_pred_no_pca = model_no_pca.predict(X_test)
from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred_no_pca))
from imblearn.over_sampling import SMOTE
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from imblearn.pipeline import Pipeline as ImbPipeline

pipeline_knn = ImbPipeline(steps=[
    ("preprocessing", preprocessor),   # numérique + catégoriel
    ("smote", SMOTE(random_state=123)), # équilibrage classes
    ("pca", PCA(n_components=5)),      # réduction dimension
    ("knn", KNeighborsClassifier())    # modèle KNN
])
param_grid = {
    "knn__n_neighbors": [3, 5, 7, 9, 11, 13, 15]
}
grid = GridSearchCV(
    estimator=pipeline_knn,
    param_grid=param_grid,
    cv=5,
    scoring="f1",
    n_jobs=-1
)

grid.fit(X_train, y_train)
print("Meilleur k :", grid.best_params_)
y_pred_knn = grid.predict(X_test)
print(classification_report(y_test, y_pred_knn))
import joblib

# Sauvegarde du meilleur modèle (exemple : grid pour KNN)
joblib.dump(grid, "Model.pkl")

print("Modèle sauvegardé sous le nom Model.pkl")
#  chargement du modele 
# Sauvegarde du meilleur modèle (exemple : grid pour KNN)
joblib.dump(grid, "Model.pkl")

print("Modèle sauvegardé sous le nom Model.pkl")
joblib.dump(model_pca, "Model.pkl")
joblib.dump(model_no_pca, "Model.pkl")
import sklearn
print(sklearn.__version__)
