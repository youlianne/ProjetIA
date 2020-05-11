from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3


# Les données d'apprentissage.
donnees = [
    ['down', {
        'age': 'old',
        'competition': 'no',
        'type': 'software'
    }],
    ['down', {
        'age': 'midlife',
        'competition': 'yes',
        'type': 'software'
    }],
    ['up', {
        'age': 'midlife',
        'competition': 'no',
        'type': 'hardware'
    }],
    ['down', {
        'age': 'old',
        'competition': 'no',
        'type': 'hardware'
    }],
    ['up', {
        'age': 'new',
        'competition': 'no',
        'type': 'hardware'
    }],
    ['up', {
        'age': 'new',
        'competition': 'no',
        'type': 'software'
    }],
    ['up', {
        'age': 'midlife',
        'competition': 'no',
        'type': 'software'
    }],
    ['up', {
        'age': 'new',
        'competition': 'yes',
        'type': 'software'
    }],
    ['down', {
        'age': 'midlife',
        'competition': 'yes',
        'type': 'hardware'
    }],
    ['down', {
        'age': 'old',
        'competition': 'yes',
        'type': 'hardware'
    }],
]

id3 = ID3()
arbre = id3.construit_arbre(donnees)
print('Arbre de décision :')
print(arbre)
print()

print('Exemplification :')
print(arbre.classifie({
        'age': 'midlife',
        'competition': 'no',
        'type': 'hardware'}))