from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3

# Les données d'apprentissage.
donnees = [
    ['angine-érythémateuse', {
        'fièvre': 'élevée',
        'amygdales': 'gonflées',
        'ganglions': 'oui',
        'gêne-à-avaler': 'oui',
        'mal-au-ventre': 'non',
        'toux': 'non',
        'rhume': 'non',
        'respiration': 'normale',
        'joues': 'normales',
        'yeux': 'normaux'}
    ],
    ['angine-pultacée', {
        'fièvre': 'élevée',
        'amygdales': 'points-blancs',
        'ganglions': 'oui',
        'gêne-à-avaler': 'oui',
        'mal-au-ventre': 'non',
        'toux': 'non',
        'rhume': 'non',
        'respiration': 'normale',
        'joues': 'normales',
        'yeux': 'normaux'}
    ],
    ['angine-diphtérique', {
        'fièvre': 'légère',
        'amygdales': 'enduit-blanc',
        'ganglions': 'oui',
        'gêne-à-avaler': 'oui',
        'mal-au-ventre': 'non',
        'toux': 'non',
        'rhume': 'non',
        'respiration': 'normale',
        'joues': 'normales',
        'yeux': 'normaux'}
    ],
    ['appendicite', {
        'fièvre': 'légère',
        'amygdales': 'normales',
        'ganglions': 'non',
        'gêne-à-avaler': 'non',
        'mal-au-ventre': 'oui',
        'toux': 'non',
        'rhume': 'non',
        'respiration': 'normale',
        'joues': 'normales',
        'yeux': 'normaux'}
    ],
    ['bronchite', {
        'fièvre': 'légère',
        'amygdales': 'normales',
        'ganglions': 'oui',
        'gêne-à-avaler': 'non',
        'mal-au-ventre': 'non',
        'toux': 'oui',
        'rhume': 'oui',
        'respiration': 'gênée',
        'joues': 'normales',
        'yeux': 'normaux'}
    ],
    ['coqueluche', {
        'fièvre': 'légère',
        'amygdales': 'normales',
        'ganglions': 'non',
        'gêne-à-avaler': 'oui',
        'mal-au-ventre': 'non',
        'toux': 'oui',
        'rhume': 'oui',
        'respiration': 'gênée',
        'joues': 'normales',
        'yeux': 'normaux'}
    ],
    ['pneumonie', {
        'fièvre': 'élevée',
        'amygdales': 'normales',
        'ganglions': 'non',
        'gêne-à-avaler': 'non',
        'mal-au-ventre': 'non',
        'toux': 'oui',
        'rhume': 'non',
        'respiration': 'rapide',
        'joues': 'rouges',
        'yeux': 'normaux'}
    ],
    ['rougeole', {
        'fièvre': 'légère',
        'amygdales': 'normales',
        'ganglions': 'non',
        'gêne-à-avaler': 'oui',
        'mal-au-ventre': 'non',
        'toux': 'oui',
        'rhume': 'oui',
        'respiration': 'normale',
        'joues': 'normales',
        'yeux': 'larmoyants'}
    ],
    ['rougeole', {
        'fièvre': 'légère',
        'amygdales': 'normales',
        'ganglions': 'non',
        'gêne-à-avaler': 'oui',
        'mal-au-ventre': 'non',
        'toux': 'oui',
        'rhume': 'oui',
        'respiration': 'normale',
        'joues': 'taches-rouges',
        'yeux': 'larmoyants'}
    ],
    ['rubéole', {
        'fièvre': 'légère',
        'amygdales': 'normales',
        'ganglions': 'oui',
        'gêne-à-avaler': 'non',
        'mal-au-ventre': 'non',
        'toux': 'non',
        'rhume': 'non',
        'respiration': 'normale',
        'joues': 'taches-rouges',
        'yeux': 'normaux'}
    ],
    ['rubéole', {
        'fièvre': 'non',
        'amygdales': 'normales',
        'ganglions': 'oui',
        'gêne-à-avaler': 'non',
        'mal-au-ventre': 'non',
        'toux': 'non',
        'rhume': 'non',
        'respiration': 'normale',
        'joues': 'taches-rouges',
        'yeux': 'normaux'}
    ],
    ['rubéole', {
        'fièvre': 'non',
        'amygdales': 'normales',
        'ganglions': 'oui',
        'gêne-à-avaler': 'non',
        'mal-au-ventre': 'non',
        'toux': 'non',
        'rhume': 'non',
        'respiration': 'normale',
        'joues': 'normales',
        'yeux': 'normaux'}
    ],
]


id3 = ID3()
arbre = id3.construit_arbre(donnees)
print('Arbre de décision :')
print(arbre)
print()

print('Exemplification :')
print(arbre.classifie({
        'fièvre': 'non',
        'amygdales': 'normales',
        'ganglions': 'oui',
        'gêne-à-avaler': 'non',
        'mal-au-ventre': 'non',
        'toux': 'non',
        'rhume': 'non',
        'respiration': 'normale',
        'joues': 'normales',
        'yeux': 'normaux'}))