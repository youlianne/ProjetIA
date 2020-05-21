class NoeudDeDecision_PT5:
    """ Un noeud dans un arbre de décision.

        This is an updated version from the one in the book (Intelligence Artificielle par la pratique).
        Specifically, if we can not classify a data point, we return the predominant class (see lines 53 - 56).
    """

    def __init__(self, attribut, donnees, p_class, enfants=None):
        """
            :param attribut: l'attribut de partitionnement du noeud et sa valeur de partitionnement sous forme de tuple (``None`` si\
            le noeud est un noeud terminal).
            :param list donnees: la liste des données qui tombent dans la\
            sous-classification du noeud.
            :param enfants: un dictionnaire associant un fils (sous-noeud) à\
            chaque valeur de l'attribut du noeud (``None`` si le\
            noeud est terminal).
        """

        self.attribut = attribut
        self.donnees = donnees
        self.enfants = enfants
        self.p_class = p_class

    def terminal(self):
        """ Vérifie si le noeud courant est terminal. """

        return self.enfants is None

    def classe(self):
        """ Si le noeud est terminal, retourne la classe des données qui\
            tombent dans la sous-classification (dans ce cas, toutes les\
            données font partie de la même classe.
        """

        if self.terminal():
            return self.donnees[0][0]

    def classifie(self, donnee):
        """ Classifie une donnée à l'aide de l'arbre de décision duquel le noeud\
            courant est la racine.

            :param donnee: la donnée à classifier.
            :return: la classe de la donnée selon le noeud de décision courant.
        """

        rep = ''
        if self.terminal():
            rep += 'Alors {}'.format(self.classe().upper())
        else:
            valeur = self.attribut[1]
            if donnee[self.attribut[0]] < valeur:
                enfant = self.enfants['1']
                rep += 'Si {} < {}, '.format(self.attribut[0], valeur.upper())
            else:
                enfant = self.enfants['2']
                rep += 'Si {} >= {}, '.format(self.attribut[0], valeur.upper())
            try:
                rep += enfant.classifie(donnee)
            except:
                rep += self.p_class
        return rep

    def repr_arbre(self, level=0):
        """ Représentation sous forme de string de l'arbre de décision duquel\
            le noeud courant est la racine.
        """

        rep = ''
        if self.terminal():
            rep += '---'*level
            rep += 'Alors {}\n'.format(self.classe().upper())
            """rep += '---'*level
            rep += 'Décision basée sur les données:\n'
            for donnee in self.donnees:
                rep += '---'*level
                rep += str(donnee) + '\n'"""

        else:
            for valeur, enfant in self.enfants.items():
                rep += '---'*level
                if valeur == '1':
                    rep += 'Si {} < {}: \n'.format(self.attribut[0], self.attribut[1].upper())
                else:
                    rep += 'Si {} >= {}: \n'.format(self.attribut[0], self.attribut[1].upper())
                rep += enfant.repr_arbre(level+1)

        return rep

    def __repr__(self):
        """ Représentation sous forme de string de l'arbre de décision duquel\
            le noeud courant est la racine.
        """

        return str(self.repr_arbre(level=0))


    def generation_regle(self, chemin=[]):
        """ Generation des regles sous forme de string """
        if self.terminal():
            regle = []
            chemin.append(('target',self.classe()))
            regle.append(chemin)
            return regle


        else:
            regles = []
            for valeur, enfant in self.enfants.items():
                chem = chemin.copy()
                chem.append((self.attribut[0], valeur))
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


    def justifie_exemple(self, exemple, regles, conflict = []):
        resultat = self.classifie(exemple)
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

    def diagnostic(self,regles,patient, diag =[]):
        if self.classifie(patient)[-1] == '0':
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
