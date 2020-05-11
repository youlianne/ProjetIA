class traitement_donnees:
    """traitement des donnees"""

    def import_donnee(self,filepath):
        from csv import DictReader
        with open(filepath,'r',encoding='UTF-8-sig') as read_obj:
            dict_reader = DictReader(read_obj)
            donnees = list(dict_reader)
            final_donnees = []
            for donnee in donnees:
                sample = donnee['target']
                del donnee['target']
                sample.append(donnee)
                final_donnees.append(sample)
        return final_donnees

    def import_donnee_test(self,filepath):
        from csv import DictReader
        with open(filepath,'r',encoding='UTF-8-sig') as read_obj:
            dict_reader = DictReader(read_obj)
            donnees = list(dict_reader)
        return donnees
