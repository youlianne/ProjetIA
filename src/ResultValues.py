from id3 import ID3
from id3_pt5 import ID3_PT5
from traitement import traitement_donnees

class ResultValues():

    def __init__(self):
        id3 = ID3()
        # Do computations here
        donnee_train = traitement_donnees.import_donnee(self,"../Data/train_bin.csv")
        donnee_test = traitement_donnees.import_donnee_test(self,"../Data/test_public_bin.csv")
        # Task 1
        self.arbre = id3.construit_arbre(donnee_train)
        #print(self.arbre)

        n = 0
        p = 0
        for donnee in donnee_test :
            model_result = self.arbre.classifie(donnee)
            if model_result[-1] == donnee['target']:
                p = p+1
            n = n+1
        print("Precision : ")
        print(p/n)
        # Task 3
        self.faits_initiaux = donnee_train
        self.regles = self.arbre.generation_regle()
            # Affichage des règles
        r = 0
        for regle in self.regles:
            r += 1
            #print(str(r) + ') ' + self.arbre.ecrit_regle(regle))
            # Justification d'un exemple à l'aide des règles
        conflict = []
        n_ex = 0
        for ex in donnee_test:
            justification  = self.arbre.justifie_exemple(ex, self.regles, conflict)
            #print(justification)
            n_ex += 1
        print('Taux de succes des justifications : ' + str(1 - len(conflict)/n_ex))
        d=[]
        for patient in donnee_test:
            self.arbre.diagnostic(self.regles,patient, d)
        print ('On a pu aider ' + str(len(d)) + ' patients en changeant 2 parametres au maximum.')
        # Task 5
        id3_pt5= ID3_PT5()
        donnee_train_continue = traitement_donnees.import_donnee(self,"../Data/train_continuous.csv")
        donnee_test_continue = traitement_donnees.import_donnee_test(self,"../Data/test_public_continuous.csv")
        self.arbre_advance = id3_pt5.construit_arbre(donnee_train_continue)
        print(self.arbre_advance)
        
        #print(self.arbre_advance.classifie(donnee_test_continue[0]))
        
        n = 0
        p = 0
        for donnee in donnee_test_continue :
            print(donnee['thalach'])
            model_result = self.arbre_advance.classifie(donnee)
            if model_result[-1] == donnee['target']:
                p = p+1
            n = n+1
        print("Precision : ")
        print(p/n)

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]
