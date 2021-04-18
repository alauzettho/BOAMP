import pandas as pd

# This file will generate a step 1 clean csv dataset from the dataAquitaine CSV

#########################################################################################################
# Import CSV and remove first column
df_dataAquitaine = pd.read_csv("/home/alauzettho/BOAMP/ScriptsParseDateRegion/dataAquitaine_0.csv")
print('------------------- DATA AQUITAINE IMPORTED -------------------')
print(df_dataAquitaine.shape) #337 Index, 56650 lignes


#########################################################################################################
# Remove Index that contains at most two values
df_dataAquitaine = df_dataAquitaine.dropna(axis = 1, thresh = 2)


#########################################################################################################
# Remove Index that we know contains useless data
# TODO
listIndexToDrop = [ 'Unnamed: 0', 'TEL', 'MEMBRE_JURY', 'MODIF_RNEC', 'LIEU_PRINCIPAL', 'INFO_COMPL',\
                    'ANNONCE_ANTERIEUR.REFERENCE_PUBLICATION.PUBLICATION_PAPIER.TYPE_EDITION',
                    'TITULAIRE.TEL', 'TYPE_PROCEDURE.RESTREINT.ACCELERE', 'URL_REGLES_NATIONALES',
                    'MODIFICATION.CPV.INIT.PRINCIPAL', 'CARACTERISTIQUES.TITRE', 'DECISION.RENSEIGNEMENT.INFO_VALEUR',
                    'MODIFICATION.CPV.LIRE.PRINCIPAL', 'TITULAIRE',
                    'DECISION.RENSEIGNEMENT.CONCOURS_NB_PARTICIPANT_ETR', 'TITULAIRE.CODE_IDENT_NATIONAL',
                    'TITULAIRE.PAYS', 'DECISION.RENSEIGNEMENT.NB_MARCHE_ATTRIBUE', 'DELEGATION.DUREE_MOIS',
                    'DECISION.PUBLICATION_JOUE.DATE_PUBLICATION', 'DECISION.PUBLICATION_JOUE.NUM_ANNONCE',
                    'DECISION.PUBLICATION_JOUE.ANNEE', 'EXPLICATION.#text', 'METHODE_VERIFICATION',
                    'TYPE_PROCEDURE.NEGOCIE.ACCELERE', 'LANGUES.AUTRES', 'LANGUES.LANGUE',
                    'DECISION.TITULAIRE.TEL', 'ADRESSES_COMPLEMENTAIRES.ADRESSE.TEL', 'TITULAIRE.MEL',
                    'NB_CANDIDATS.NOMS_PARTICIPANTS_SELECTIONNES', 'MODIFICATION.SUPPRIMER', 'BESOIN_TVX',
                    'MEMBRE_JURY.#text', 'REFERENCE_PUBLICATION', 'TYPE_PROCEDURE.AUTRE',
                    'CARACTERISTIQUES.TABLE.TR', 'DECISION.RENSEIGNEMENT',
                    'LOI_COMPTE_AUTRE_PAYS.#text', 'ENCHERE_ELECTRONIQUE_OUI', 'DECISION.AUTRES_INFORMATIONS',
                    'FAX', 'ADRESSES_COMPLEMENTAIRES.ADRESSE.FAX', 'DECISION.TITULAIRE.FAX', 'MODIFICATION.LOT.#text',
                    'LOTS_RESERVE_POUVOIR_ADJUDICATEUR', 'CARACTERISTIQUES.RECONDUCTIONS.NB_RECONDUCTIONS_MIN',
                    'FONDS_COMMUNAUTAIRES_OUI', 'DESCRIPTION', 'ETUDES_CONCOURS', 'TYPE_PROCEDURE.OUVERT.ACCELERE',
                    'DECISION.RENSEIGNEMENT.TRANCHE_CONDITIONNELLE.#text', 'CODE_NUTS.#text', 'TITULAIRE.CODE_NUTS']

df_dataAquitaine = df_dataAquitaine.drop(columns = listIndexToDrop)


#########################################################################################################
# DEP_PRESTATION

listOfDepToRemove = df_dataAquitaine['DEP_PRESTATION'].dropna().unique().tolist()
listOfDepToRemove.pop(0)
listOfDepToRemove.pop(0)
listOfDepToRemove.pop(3)
listOfDepToRemove.pop(3)

df_dataAquitaine = df_dataAquitaine[~df_dataAquitaine['DEP_PRESTATION'].isin(listOfDepToRemove)]


#########################################################################################################
# Remove other countries and delete PAYS index

df_dataAquitaine = df_dataAquitaine[df_dataAquitaine['PAYS'].isna()]
df_dataAquitaine = df_dataAquitaine.drop(columns = ['PAYS'])


#########################################################################################################
# Remove three tows where devise is USD or CHF

df_dataAquitaine = df_dataAquitaine.drop(index = df_dataAquitaine[df_dataAquitaine['IDWEB'] == '17-138043'].index)
df_dataAquitaine = df_dataAquitaine.drop(index = df_dataAquitaine[df_dataAquitaine['IDWEB'] == '17-143205'].index)
df_dataAquitaine = df_dataAquitaine.drop(index = df_dataAquitaine[df_dataAquitaine['IDWEB'] == '17-149423'].index)


#########################################################################################################
# Remove @DEVISE as prices are only in EUR

listIndexToDrop = [
        'CARACTERISTIQUES.VALEUR_TOTALE.@DEVISE',
        'LOTS.LOT.VALEUR.@DEVISE',
        'CARACTERISTIQUES.VALEUR.@DEVISE',
        'DECISION.RENSEIGNEMENT.ESTIMATION_INITIALE.@DEVISE',
        'DECISION.RENSEIGNEMENT.MONTANT.@DEVISE',
        'CARACTERISTIQUES.VALEUR_MIN.@DEVISE',
        'CARACTERISTIQUES.VALEUR_MAX.@DEVISE',
        'ACCORD_CADRE.VALEUR.@DEVISE',
        'DECISION.RENSEIGNEMENT.MONTANT_MAXI.@DEVISE',
        'VALEUR_TOTALE.@DEVISE',
        'DECISION.RENSEIGNEMENT.OFFRE_BASSE.@DEVISE',
        'DECISION.RENSEIGNEMENT.OFFRE_ELEVEE.@DEVISE',
        'ACCORD_CADRE.VALEUR_MIN.@DEVISE',
        'ACCORD_CADRE.VALEUR_MAX.@DEVISE',
        'DECISION.RENSEIGNEMENT.CONCOURS_PRIME.@DEVISE',
        'DECISION.RENSEIGNEMENT.MONTANT_MINI.@DEVISE',
        'DECISION.RENSEIGNEMENT.SOUSTRAITANCE_OUI.VALEUR.@DEVISE',
        'VALEUR.@DEVISE',
        'VALEUR_AVT.@DEVISE',
        'VALEUR_APR.@DEVISE',
        'DOCUMENT_PAYANT_OUI.VALEUR.@DEVISE',
        'DECISION.RENSEIGNEMENT.REDEVANCE_VALEUR.@DEVISE',
        'DECISION.RENSEIGNEMENT.AVANTAGE_VALEUR.@DEVISE',
        'OFFRE_BASSE.@DEVISE',
        'OFFRE_ELEVEE.@DEVISE',
        'LOTS.LOT.VALEUR_MIN.@DEVISE',
        'LOTS.LOT.VALEUR_MAX.@DEVISE']

df_dataAquitaine = df_dataAquitaine.drop(columns = listIndexToDrop)
print(df_dataAquitaine.shape)


#########################################################################################################
# Rename #text to COUT for prices

rename_dict = {
    'CARACTERISTIQUES.VALEUR_TOTALE.#text' : 'CARACTERISTIQUES.VALEUR_TOTALE.COUT' ,
    'LOTS.LOT.VALEUR.#text' : 'LOTS.LOT.VALEUR.COUT' ,
    'CARACTERISTIQUES.VALEUR.#text' : 'CARACTERISTIQUES.VALEUR.COUT' ,
    'DECISION.RENSEIGNEMENT.ESTIMATION_INITIALE.#text' : 'DECISION.RENSEIGNEMENT.ESTIMATION_INITIALE.COUT' ,
    'DECISION.RENSEIGNEMENT.MONTANT.#text' : 'DECISION.RENSEIGNEMENT.MONTANT.COUT' ,
    'CARACTERISTIQUES.VALEUR_MIN.#text' : 'CARACTERISTIQUES.VALEUR_MIN.COUT' ,
    'CARACTERISTIQUES.VALEUR_MAX.#text' : 'CARACTERISTIQUES.VALEUR_MAX.COUT' ,
    'ACCORD_CADRE.VALEUR.#text' : 'ACCORD_CADRE.VALEUR.COUT' ,
    'DECISION.RENSEIGNEMENT.MONTANT_MAXI.#text' : 'DECISION.RENSEIGNEMENT.MONTANT_MAXI.COUT' ,
    'VALEUR_TOTALE.#text' : 'VALEUR_TOTALE.COUT' ,
    'DECISION.RENSEIGNEMENT.OFFRE_BASSE.#text' : 'DECISION.RENSEIGNEMENT.OFFRE_BASSE.COUT' ,
    'DECISION.RENSEIGNEMENT.OFFRE_ELEVEE.#text' : 'DECISION.RENSEIGNEMENT.OFFRE_ELEVEE.COUT' ,
    'ACCORD_CADRE.VALEUR_MIN.#text' : 'ACCORD_CADRE.VALEUR_MIN.COUT' ,
    'ACCORD_CADRE.VALEUR_MAX.#text' : 'ACCORD_CADRE.VALEUR_MAX.COUT' ,
    'DECISION.RENSEIGNEMENT.CONCOURS_PRIME.#text' : 'DECISION.RENSEIGNEMENT.CONCOURS_PRIME.COUT' ,
    'DECISION.RENSEIGNEMENT.MONTANT_MINI.#text' : 'DECISION.RENSEIGNEMENT.MONTANT_MINI.COUT' ,
    'DECISION.RENSEIGNEMENT.SOUSTRAITANCE_OUI.VALEUR.#text' : 'DECISION.RENSEIGNEMENT.SOUSTRAITANCE_OUI.VALEUR.COUT' ,
    'VALEUR.#text' : 'VALEUR.COUT' ,
    'VALEUR_AVT.#text' : 'VALEUR_AVT.COUT' ,
    'VALEUR_APR.#text' : 'VALEUR_APR.COUT' ,
    'DOCUMENT_PAYANT_OUI.VALEUR.#text' : 'DOCUMENT_PAYANT_OUI.VALEUR.COUT' ,
    'DECISION.RENSEIGNEMENT.REDEVANCE_VALEUR.#text' : 'DECISION.RENSEIGNEMENT.REDEVANCE_VALEUR.COUT' ,
    'DECISION.RENSEIGNEMENT.AVANTAGE_VALEUR.#text' : 'DECISION.RENSEIGNEMENT.AVANTAGE_VALEUR.COUT' ,
    'OFFRE_BASSE.#text' : 'OFFRE_BASSE.COUT' ,
    'OFFRE_ELEVEE.#text' : 'OFFRE_ELEVEE.COUT' ,
    'LOTS.LOT.VALEUR_MIN.#text' : 'LOTS.LOT.VALEUR_MIN.COUT' ,
    'LOTS.LOT.VALEUR_MAX.#text' : 'LOTS.LOT.VALEUR_MAX.COUT'}

df_dataAquitaine = df_dataAquitaine.rename(columns = rename_dict)


#########################################################################################################
# Remove prices Index that have too few values

listIndexToDrop = [ 'LOTS.LOT.VALEUR_MAX.COUT',
                    'LOTS.LOT.VALEUR_MIN.COUT',
                    'OFFRE_ELEVEE.COUT',
                    'OFFRE_BASSE.COUT',
                    'DECISION.RENSEIGNEMENT.AVANTAGE_VALEUR.COUT',
                    'DECISION.RENSEIGNEMENT.REDEVANCE_VALEUR.COUT']

df_dataAquitaine = df_dataAquitaine.drop(columns = listIndexToDrop)


#########################################################################################################
# Clean LIEU: remove Index, keep empty lines

df_dataAquitaine = df_dataAquitaine.drop(columns = ['LIEU_EXEC_LIVR', 'LIEU_EXEC_LIVR.VILLE', 'LIEU_EXEC_LIVR.ADRESSE'])
print(df_dataAquitaine.shape)


#########################################################################################################
# Classes

df_classe1 = df_dataAquitaine[['CLASSES.CLASSE','IDWEB']].dropna(axis = 0)

CodeArray = []
LibeArray = []

for i in range(0, len(df_classe1.index)) :
    values = df_classe1['CLASSES.CLASSE'].iloc[i].split('OrderedDict')[1].split(',')
    CODE = values[1].replace(')', '').replace(']', '').replace('"', '').replace("'", '')
    LIBE = values[3].replace(')', '').replace(']', '').replace('"', '').replace("'", '')[1:]
    CodeArray.append(CODE)
    LibeArray.append(LIBE)

# Fillna
df_classe1['CLASSES.CLASSE.CODE'] = CodeArray
df_classe1['CLASSES.CLASSE.LIBELLE'] = LibeArray
df_dataAquitaine['CLASSES.CLASSE.CODE'] = df_dataAquitaine['CLASSES.CLASSE.CODE'].fillna(df_classe1['CLASSES.CLASSE.CODE']).fillna(0).astype(int)
df_dataAquitaine['CLASSES.CLASSE.LIBELLE'] = df_dataAquitaine['CLASSES.CLASSE.LIBELLE'].fillna(df_classe1['CLASSES.CLASSE.LIBELLE'])

# Drop Useless Column
df_dataAquitaine = df_dataAquitaine.drop(columns = 'CLASSES.CLASSE')

print(df_dataAquitaine.shape)


#########################################################################################################
# Clean ADRESS

indexToDrop = [ 'ADRESSES_COMPLEMENTAIRES.ADRESSE.URL', 'ADRESSES_COMPLEMENTAIRES.ADRESSE.CORRESPONDANT',
                'ADRESSES_COMPLEMENTAIRES.ADRESSE.POSTE', 'ADRESSES_COMPLEMENTAIRES.ADRESSE.CONTACT',
                'ADRESSES_COMPLEMENTAIRES.ADRESSE.CODE_IDENT_NATIONAL', 'ADRESSES_COMPLEMENTAIRES.ADRESSE.CODE_NUTS',
                'ADRESSES_COMPLEMENTAIRES.ADRESSE.PAYS', 'ADRESSES_COMPLEMENTAIRES.ADRESSE.MEL',
                'ADRESSE', 'ADRESSES_COMPLEMENTAIRES.ADRESSE.VILLE', 'ADRESSES_COMPLEMENTAIRES.ADRESSE.ADRESSE',
                'ADRESSES_COMPLEMENTAIRES.ADRESSE']

df_dataAquitaine = df_dataAquitaine.drop(columns = indexToDrop)
print(df_dataAquitaine.shape)


#########################################################################################################
# Remove value where CP not in Aquitaine and Removes nan
df_dataAquitaine = df_dataAquitaine[~df_dataAquitaine['ADRESSES_COMPLEMENTAIRES.ADRESSE.CP'].str.contains('33 06', na = False)]

listOfDepToRemove = df_dataAquitaine['ADRESSES_COMPLEMENTAIRES.ADRESSE.CP'].dropna().unique().tolist()
listOfIntDepToRemove = [int(x) for x in listOfDepToRemove]

listDepKepp = [40, 47, 33, 64]

remove_indices = []
for i in range(len(listOfIntDepToRemove)) :
    if listOfIntDepToRemove[i] // 1000 not in listDepKepp :
        remove_indices.append(i)

listOfDepToRemove = [i for j, i in enumerate(listOfDepToRemove) if j not in remove_indices]

df_dataAquitaine = df_dataAquitaine[df_dataAquitaine['ADRESSES_COMPLEMENTAIRES.ADRESSE.CP'].isin(listOfDepToRemove) \
    | df_dataAquitaine['ADRESSES_COMPLEMENTAIRES.ADRESSE.CP'].isnull()]

print(df_dataAquitaine.shape)


#########################################################################################################
# ANNONCE ANTERIEUR
listIndexToDrop = [ 'ANNONCE_ANTERIEUR.REFERENCE.IDWEB',
                    'ANNONCE_ANTERIEUR.REFERENCE.DATE_ENVOI',
                    'ANNONCE_ANTERIEUR.REFERENCE_PUBLICATION',
                    'ANNONCE_ANTERIEUR.REFERENCE_PUBLICATION.PUBLICATION_ELECTRONIQUE.DATE_PUBLICATION',
                    'ANNONCE_ANTERIEUR.REFERENCE_PUBLICATION.PUBLICATION_ELECTRONIQUE.DATE_FIN_DIFFUSION',
                    'ANNONCE_ANTERIEUR',
                    'ANNONCE_ANTERIEUR.REFERENCE_PUBLICATION.PUBLICATION_PAPIER.NUM_PARUTION',
                    'ANNONCE_ANTERIEUR.REFERENCE_PUBLICATION.PUBLICATION_PAPIER.NUM_ANNONCE',
                    'ANNONCE_ANTERIEUR.REFERENCE_PUBLICATION.PUBLICATION_PAPIER.DATE_PUBLICATION']

df_dataAquitaine = df_dataAquitaine.drop(columns = listIndexToDrop)
print(df_dataAquitaine.shape)


#########################################################################################################
listIndexToDrop = [ 'LOTS.LOT.SUP_QUATRE_ANS_JUSTIFICATION', 'LIMITE_ENVOI_INVIT',
                    'DECISION.RENSEIGNEMENT.CONCOURS_NB_PARTICIPANT', 'LOTS.LOT.FONDS_COMMUNAUTAIRES_DESCRIPTION',
                    'LOTS.LOT.DATE_EXECUTION', 'DATE_LIMITE_REPONSE', 'DATE_FIN_DIFFUSION',
                    'LOTS.LOT.DATE_LIVRAISON', 'AUTRE', 'POSTE', 'ACCORD_CADRE.NB_MAX_PARTICIPANTS',
                    'TITULAIRE.URL', 'CARACTERISTIQUES.OPTIONS.DESCRIPTION.#text',
                    'DECISION.RENSEIGNEMENT.SOUSTRAITANCE_OUI.PROPORTION', 'MODIFICATION.TEXTE.LIRE.#text',
                    'DECISION.RENSEIGNEMENT.NB_MOIS', 'MARCHE_PERIODIQUE_OUI.CALENDRIER_PROCHAINS_AVIS',
                    'CONDITIONS', 'ID_CONSULTATION', 'MODIFICATION.DATE.INIT.#text',
                    'DELEGATION.NATURE_CONVENTION', 'MODIFICATION.TEXTE.INIT.#text',
                    'ID_CONSULTATION', 'ACCORD_CADRE.SUP_QUATRE_ANS_JUSTIFICATION', 'DECISION.TITULAIRE.VILLE',
                    'CARACTERISTIQUES.RECONDUCTIONS.NB_RECONDUCTIONS_MAX', 'DECISION.RENSEIGNEMENT.NB_ANNEE',
                    'CARACTERISTIQUES.OPTIONS.DUREE_JOURS', 'MODIFICATION.DATE.LIRE.#text',
                    'DUREE_MOIS', 'INDEMNISATION_PARTICIPANTS', 'ENTITE_ADJUDICATRICE.AUTRE',
                    'DESC_MODIF', 'URL_CONSULTATION', 'PROCEDURES_RECOURS_PRECISIONS',
                    'VALEUR.COUT', 'DELEGATION.DOMAINE.AUTRE', 'MODIFICATION',
                    'VALEUR_AVT.COUT', 'CARACTERISTIQUES.OPTIONS.DUREE_MOIS', 'CRITERES_PARTICIPATION',
                    'VALEUR_APR.COUT', 'LOTS.LOT.DUREE_JOURS', 'URL_INFORMATION', 'EXPLICATION',
                    'DOCUMENT_PAYANT_OUI.VALEUR.COUT', 'PERS_OUVERTURE_OFFRES_OUI', 'DECISION.RENSEIGNEMENT.MONTANT_MINI.COUT',
                    'DELEGATION.AUTRES_PRECISIONS', 'URL_PARTICIPATION', 'ACCORD_CADRE.NB_PARTICIPANTS',
                    'LOTS.LOT.QUANTITE', 'REFERENCE_PUBLICATION.PUBLICATION_JOUE.ANNEE',
                    'TITULAIRE.DENOMINATION', 'SITUATION_JURIDIQUE', 'DATE_LIMITE_OBTENTION_DOCUMENTS',
                    'TITULAIRE.VILLE', 'URL_PROFIL_ACHETEUR', 'DECISION.TITULAIRE.MEL',
                    'DECISION.RENSEIGNEMENT.TRANCHE_FERME', 'DECISION.TITULAIRE.URL', 'DECISION.TITULAIRE.ADRESSE',
                    'TITULAIRE.ADRESSE', 'MEL', 'URL', 'JUSTIFICATIFS_CANDIDAT.P', 'RECOMPENSES_LAUREAT',
                    'TITULAIRE.CP', 'DECISION.RENSEIGNEMENT.MONTANT_MAXI.COUT', 'RECEPT_CANDIDAT',
                    'DELEGATION.TEXTE_APPLICATION', 'DELEGATION.DUREE_AN',
                    'LOTS.LOT.NB_CANDIDATS.NB_MAX_OFFRE',
                    'LOTS.LOT.NB_CANDIDATS.NB_MIN_OFFRE',
                    'LOTS.LOT.NB_CANDIDATS.LIMITATION_CANDIDATS',
                    'LOTS.LOT.NB_CANDIDATS.NB_OFFRE',
                    'DECISION.TITULAIRE.CODE_IDENT_NATIONAL', 'URL_DOCUMENT', 'URL_OUTIL_LOGICIEL',
                    'MODIFICATION.RUB_INIT', 'MODIFICATION.AJOUTER', 'MODIFICATION.APRES_MENTION.#text',
                    'MODIFICATION.TXT_INIT', 'MODIFICATION.LIRE', 'CONTACT', 'MOTIF', 'VILLE', 'ADJUDICATEUR_NUTS',
                    'LOTS.LOT.CODE_NUTS', 'LIEU_EXEC_LIVR.CODE_NUTS', 'DECISION.TITULAIRE.CODE_NUTS',
                    'LIEU_EXEC_LIVR.CODE_NUTS', 'LIEU_EXEC_LIVR.CP']

df_dataAquitaine = df_dataAquitaine.drop(columns = listIndexToDrop)
print(df_dataAquitaine.shape)


#########################################################################################################
# Generate Step 1 file

fileName = "dataAquitaine_1.csv"
df_dataAquitaine.to_csv(fileName)