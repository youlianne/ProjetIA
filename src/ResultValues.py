from id3 import ID3
from id3_pt5 import ID3_PT5
from traitement import traitement_donnees

class ResultValues():

    def __init__(self):
        id3 = ID3()
        # Import data
        donnee_train = traitement_donnees.import_donnee(self,"../Data/train_bin.csv")
        donnee_test = traitement_donnees.import_donnee_test(self,"../Data/test_public_bin.csv")
        self.faits_initiaux = donnee_train
        
        # Task 1 : Build tree
        self.arbre = id3.construit_arbre(donnee_train)
        print(self.arbre)

        # Task 2 : Precision of the tree
        n = 0
        p = 0
        for donnee in donnee_test :
            model_result = self.classifie(donnee, self.arbre)
            if model_result[-1] == donnee['target']:
                p = p+1
            n = n+1
        print("Precision : " + str (p/n))

        # Task 3 : generate rules
        self.regles = self.generation_regle(self.arbre)
            # Print rules
        r = 0
        for regle in self.regles:
            r += 1
            print(str(r) + ') ' + self.ecrit_regle(regle))
            # Justification of an example using the rules
        conflict = []
        print(self.justifie_exemple(donnee_test[1], self.regles, self.arbre, conflict)) #any patient can be used as an example, we just chose to only print one
            # Rules precision (should be the same as the precision of the tree they come from)
        n_ex = 0
        for ex in donnee_test:
            justification  = self.arbre.justifie_exemple(ex, self.regles, conflict) #justification can be printed in case someone wants to see the justification for each patient of the test data
            n_ex += 1
        print('Taux de succes des justifications : ' + str(1 - len(conflict)/n_ex))
      
        #Task 4 : try to help the patients classified as sick by the tree
        d=[]
        for patient in donnee_test:
            self.arbre.diagnostic(self.regles,patient, d)
        print ('On a pu aider ' + str(len(d)) + ' patients en changeant 2 parametres au maximum.')
        
        # Task 5
        id3_pt5= ID3_PT5()
            #Import continuous data
        donnee_train_continue = traitement_donnees.import_donnee(self,"../Data/train_continuous.csv")
        donnee_test_continue = traitement_donnees.import_donnee_test(self,"../Data/test_public_continuous.csv")
            #Build continous tree
        self.arbre_advance = id3_pt5.construit_arbre(donnee_train_continue)
        print(self.arbre_advance)
            #Accuracy of the continuous tre
        n = 0
        p = 0
        for donnee in donnee_test_continue :
            model_result = self.arbre_advance.classifie(donnee)
            if model_result[-1] == donnee['target']:
                p = p+1
            n = n+1
        print("Precision : " + str(p/n))

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]

    def generation_regle(self, noeud, chemin=[]):
        """ Generation des regles sous forme de string """
        if noeud.terminal():
            regle = []
            chemin.append(('target',noeud.classe()))
            regle.append(chemin)
            return regle

        else:
            regles = []
            for valeur, enfant in noeud.enfants.items():
                chem = chemin.copy()
                chem.append((noeud.attribut, valeur))
                regles+=enfant.generation_regle(chem)
            return regles


    def ecrit_regle(self, sequence):
        regle = ''
        for element in sequence :
            if element[0] != 'target':
                regle = regle + 'Si ' + element[0] + ' = ' + element[1] + ', '
            else :
                regle = regle + 'Alors ' + element[1] + '.'
        return regle


    def justifie_exemple(self, exemple, regles, noeud, conflict = []):
        resultat = noeud.classifie(exemple)
        r = 0
        for regle in regles:
            r += 1
            verif = 0
            for param in regle :
                if exemple[param[0]] == param[1] and param[0] != 'target':
                    verif += 1
            if verif == len(regle)-1:
                if exemple['target'] == resultat[-1]:
                    return 'Le resultat est ' + resultat[-1] + ' car : ' + self.ecrit_regle(regle) + ' (regle numero ' + str(r) + ')'
                else :
                    conflict.append(1)
                    return 'D\'apres la regle numero ' + str(r) + ' ('+ self.ecrit_regle(regle) + '), le patient est classifie ' + resultat[-1] + ' mais son etat reel est ' + str(exemple['target'])+'.'
        return 'Aucune justification trouvee...'

    def diagnostic(self,regles,patient, noeud, diag =[]):
        if noeud.classifie(patient)[-1] == '0':
            return 'le patient n\'est pas malade donc on ne fait pas de diagnostic'
        for regle in regles:
            diff = 0
            if regle[-1][1]=='0':
                stock= 'si l\'on modifie '
                for param in regle:
                    if patient[param[0]]!= param[1] and param[0]!='target' and param[0]!='sex' and param[0]!='age':
                        diff +=1
                        stock += param[0].upper() + ' a ' + str(param[1]).upper() + ' , '
                if diff <= 2:
                    diag.append(1)
                    return  stock + 'alors le patient sera classifie comme 0' + ' d\'apres la regle ' + self.ecrit_regle(regle)
        return 'diagnostic impossible car il y a trop d\'attributs a changer'
