from math import log
from noeud_de_decision_pt5 import NoeudDeDecision_PT5

class ID3_PT5:
    """ Algorithme ID3.

        This is an updated version from the one in the book (Intelligence Artificielle par la pratique).
        Specifically, in construit_arbre_recur(), if donnees == [] (line 70), it returns a terminal node with the predominant class of the dataset -- as computed in construit_arbre() -- instead of returning None.
        Moreover, the predominant class is also passed as a parameter to NoeudDeDecision().
    """

    def construit_arbre(self, donnees):
        """ Construit un arbre de décision à partir des données d'apprentissage.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :return: une instance de NoeudDeDecision correspondant à la racine de\
            l'arbre de décision.
        """

        # Nous devons extraire les domaines de valeur des
        # attributs, puisqu'ils sont nécessaires pour
        # construire l'arbre.
        attributs = {}
        for donnee in donnees:
            for attribut, valeur in donnee[1].items():
                valeurs = attributs.get(attribut)
                if valeurs is None:
                    valeurs = set()
                    attributs[attribut] = valeurs
                valeurs.add(valeur)
        # Find the predominant class
        classes = set([row[0] for row in donnees])
        predominant_class_counter = -1
        for c in classes:
            if [row[0] for row in donnees].count(c) >= predominant_class_counter:
                predominant_class_counter = [row[0] for row in donnees].count(c)
                predominant_class = c
        # Set default tags (1 or 2) for each training point. The tags will be useful for classification.
        for patient in donnees:
            patient[1]['etiquette']='1';
        arbre = self.construit_arbre_recur(donnees, attributs, predominant_class)
        return arbre

    def construit_arbre_recur(self, donnees, attributs, predominant_class,level=0):
        """ Construit rédurcivement un arbre de décision à partir
            des données d'apprentissage et d'un dictionnaire liant
            les attributs à la liste de leurs valeurs possibles.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :param attributs: un dictionnaire qui associe chaque\
            attribut A à son domaine de valeurs a_j.
            :return: une instance de NoeudDeDecision correspondant à la racine de\
            l'arbre de décision.
        """
        def classe_unique(donnees):
            """ Vérifie que toutes les données appartiennent à la même classe. """

            if len(donnees) <=1:
                return True
            premiere_classe = donnees[0][0]
            for donnee in donnees:
                if donnee[0] != premiere_classe:
                    return False
            return True

        if donnees == []:
            return NoeudDeDecision_PT5(None, [str(predominant_class), dict()], str(predominant_class))

        # Si toutes les données restantes font partie de la même classe,
        # on peut retourner un noeud terminal.
        elif classe_unique(donnees) or level>=10: # Also set a maximal depth 
            return NoeudDeDecision_PT5(None, donnees, str(predominant_class))

        else: #Continue
            # Find the attribute and value with minimal entropy
            split = self.trouve_split(donnees,attributs)
            for patient in donnees: #Set tags to the training points according to the splitting attribute and value
                if patient[1][split[0]] < split[1]:
                    patient[1]['etiquette']='1'
                else:
                    patient[1]['etiquette']='2'

            partitions = self.partitionne(donnees)

            enfants = {}
            for valeur, partition in partitions.items():
                attributs = {} #Same set of attributes but we remove the values tha are not relevant in each side of the node
                for donnee in partition:
                    for attribut, valeur in donnee[1].items():
                        valeurs = attributs.get(attribut)
                        if valeurs is None:
                            valeurs = set()
                            attributs[attribut] = valeurs
                        valeurs.add(valeur)
                enfants[valeur] = self.construit_arbre_recur(partition,
                                                             attributs,
                                                             predominant_class,level+1)

            return NoeudDeDecision_PT5(split, donnees, str(predominant_class), enfants)

    def partitionne(self, donnees, attribut='etiquette', valeurs=['1','2']):
        """ Partitionne les données sur les valeurs a_j de l'attribut A.

            :param list donnees: les données à partitioner.
            :param attribut: l'attribut A de partitionnement.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: un dictionnaire qui associe à chaque valeur a_j de\
            l'attribut A une liste l_j contenant les données pour lesquelles A\
            vaut a_j.
        """
        partitions = {valeur: [] for valeur in valeurs}

        for donnee in donnees:
            partition = partitions[donnee[1][attribut]]
            partition.append(donnee)

        return partitions

    def p_aj(self, donnees, attribut, valeur):
        """ p(a_j) - la probabilité que la valeur de l'attribut A soit a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :return: p(a_j)
        """
        # Nombre de données.
        nombre_donnees = len(donnees)

        # Permet d'éviter les divisions par 0.
        if nombre_donnees == 0:
            return 0.0

        # Nombre d'occurrences de la valeur a_j parmi les données.
        nombre_aj = 0
        for donnee in donnees:
            if donnee[1][attribut] == valeur:
                nombre_aj += 1
        # p(a_j) = nombre d'occurrences de la valeur a_j parmi les données /
        #          nombre de données.
        return nombre_aj / nombre_donnees

    def p_ci_aj(self, donnees, attribut, valeur, classe):
        """ p(c_i|a_j) - la probabilité conditionnelle que la classe C soit c_i\
            étant donné que l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :param classe: la valeur c_i de la classe C.
            :return: p(c_i | a_j)
        """
        # Nombre d'occurrences de la valeur a_j parmi les données.
        donnees_aj = [donnee for donnee in donnees if donnee[1][attribut] == valeur]
        nombre_aj = len(donnees_aj)

        # Permet d'éviter les divisions par 0.
        if nombre_aj == 0:
            return 0

        # Nombre d'occurrences de la classe c_i parmi les données pour lesquelles
        # A vaut a_j.
        donnees_ci = [donnee for donnee in donnees_aj if donnee[0] == classe]
        nombre_ci = len(donnees_ci)

        # p(c_i|a_j) = nombre d'occurrences de la classe c_i parmi les données
        #              pour lesquelles A vaut a_j /
        #              nombre d'occurrences de la valeur a_j parmi les données.
        return nombre_ci / nombre_aj

    def h_C_aj(self, donnees, attribut, valeur):
        """ H(C|a_j) - l'entropie de la classe parmi les données pour lesquelles\
            l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :return: H(C|a_j)
        """
        # Les classes attestées dans les exemples.
        classes = list(set([donnee[0] for donnee in donnees]))

        # Calcule p(c_i|a_j) pour chaque classe c_i.
        p_ci_ajs = [self.p_ci_aj(donnees, attribut, valeur, classe)
                    for classe in classes]

        # Si p vaut 0 -> plog(p) vaut 0.
        return -sum([p_ci_aj * log(p_ci_aj, 2.0)
                    for p_ci_aj in p_ci_ajs
                    if p_ci_aj != 0])

    def h_C_A(self, donnees, attribut='etiquette', valeurs = ['1','2']):
        """ H(C|A) - l'entropie de la classe après avoir choisi de partitionner\
            les données suivant les valeurs de l'attribut A.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: H(C|A)
        """
        # Calcule P(a_j) pour chaque valeur a_j de l'attribut A.
        p_ajs = [self.p_aj(donnees, attribut, valeur) for valeur in valeurs]
        # Calcule H_C_aj pour chaque valeur a_j de l'attribut A.
        h_c_ajs = [self.h_C_aj(donnees, attribut, valeur)
                   for valeur in valeurs]

        return sum([p_aj * h_c_aj for p_aj, h_c_aj in zip(p_ajs, h_c_ajs)])

    def trouve_split(self, donnees, attributs):
        """ Returns a tuple containing the pair of attribute and value which reduce the entropy the most
        """
        entropie_min = 1
        paire = ('','')
        for attribut in attributs:
            for valeur in attributs[attribut]:
                for patient in donnees:
                    if float(patient[1][attribut]) < float(valeur) :
                        patient[1]['etiquette'] = '1'
                    else :
                        patient[1]['etiquette'] = '2'
                entropie = self.h_C_A(donnees)
                if entropie <= entropie_min:
                    entropie_min= entropie
                    paire= (attribut,valeur)
        return paire
