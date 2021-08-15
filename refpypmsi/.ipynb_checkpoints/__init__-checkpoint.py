# -*- coding: utf-8 -*-
# #
# refpypmsi - Implémentation en python de refpmsi
# @https://github.com/denisGustin/refpmsi refpmsi est un package crée par denisGustin
# Ce package est sous license GPL
# #

import os
import pandas as pd

chemin_module = os.path.dirname(os.path.abspath(__file__))+"/../"

def refpypmsi (referentiel = '', periodepmsi = '', ignorer_periode_manquante = True):

    '''
        referentiel - fonction de récupération d'un référenciel

        inputs :
            referentiel, str : nom du référentiel à extraire, la liste des référentiels disponibles est accessible par la commande liste_refpypmsi
            periodepmsi, int : année du référentiel, si l'année n'existe pas où le référentiel n'est pas daté, l'année est ignoré et l'ensemble des données sont retournés. Ce comportement peut être modifié à l'aide de l'option ignorer_periode_manquante.
            ignorer_periode_manquante, boolean : si False, une erreur est renvoyé lorsque l'année sélectionnée n'existe pas, autrement, aucune l'erreur est ignoré et l'ensemble des données disponibles sont renvoyés.

        output :
            Pandas Dataframe : dataframe contenant le référentiel sélectionné
    '''
    
    chemin_refentiel = "/".join([
        chemin_module,
        'inst/referentiels',
        referentiel+".json.gz"
    ])

    if (os.path.exists(chemin_refentiel) == False):
        # Déclenchement de l'erreur
        if referentiel != 'liste_refpmsi':
             # Referentiels attendus
            liste_referentiels = liste_refpypmsi()
            
            raise Exception("Référentiel invalide. Devrait être l'un des suivants : {}".format(
                ", ".join(liste_referentiels)
            ))
        else:
            raise Exception("Liste de référentiels inexistante, essayez de ré-installer le package.")


    # Chargement du référentiel
    donnees_referentiel = pd.read_json(chemin_refentiel)

    # Filtre par année quand nécessaire
    if (periodepmsi != ''):
        if type(periodepmsi) != type(list()):
            periodepmsi = [periodepmsi] # On s'assure que c'est une liste
        periodepmsi = [int(x) for x in periodepmsi] # On s'assure que c'est du int

        if (('anpmsi' not in donnees_referentiel.columns) or (sum(donnees_referentiel["anpmsi"].isin(periodepmsi)) > 0)):
            donnees_referentiel = donnees_referentiel[donnees_referentiel["anpmsi"].isin(periodepmsi)] \
                                    .reset_index(drop = True)
        else:
            if ignorer_periode_manquante == False:
                raise Exception("Année de référentiel invalide.")

    # On retourne le référentiel
    return(donnees_referentiel)

def liste_refpypmsi():
    '''
        liste_refpypmsi - Fonction qui renvoie la liste des référentiels existants

        output :
            Pandas Dataframe : dataframe contenant la liste des référentiels existants
    '''
    
    liste_referentiels = refpypmsi("liste_refpmsi")

    return(liste_referentiels)

def refpmsi(referentiel = '', periodepmsi = '', ignorer_periode_manquante = True, chemin = ''):
    return refpypmsi(referentiel=referentiel, periodepmsi=periodepmsi, ignorer_periode_manquante=ignorer_periode_manquante)

def liste_refpmsi():
    return liste_refpypmsi()
