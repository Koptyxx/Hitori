from upemtk import *
from random import randint

def lire_grille(nom_fichier):
    lst=[]
    f=open(nom_fichier, "r")
    contenu=f.readlines()
    for elem in contenu:
        c=elem.split()
        lst.append(c)
    f.close()
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            lst[i][j]=int(lst[i][j])
    return lst
    
def ecrire_grille(grille,nom_fichier):
    f=open(nom_fichier, "w")
    x=0
    for ligne in grille:
        if x>0:
            f.write("/n")
        for i in range(len(ligne)-1):
            f.write(str(ligne[i] + ' '))
        x+=1
    f.close()
    
def affiche_grille(ldl):
    for i in range(len(ldl)):
        lst=ldl[i]*1
        for j in range(len(lst)):
            lst[j]=str(lst[j])
        s=" "
        print(s.join(lst))
        

def sans_conflit(grille, noircies):
    for i in range(len(grille)-1):
        for j in range(len(grille[i])-1):
            if j<len(grille[i])-1 and i<len(grille)-1 and (grille[i][j]==grille[i][j+1] or grille[i][j]==grille[i+1][j]) and grille[i][j] not in noircies:
                return False 
    return True



def Sans_voisines_noircies(grille, noircies):
    for ligne in range(len(grille)):
        for colonne in range(len(grille[ligne])):

            if (ligne, colonne) not in noircies:
                continue

            if (ligne, colonne) in noircies:
                print('j')
                if ligne>0 and (ligne-1, colonne) in noircies:
                    return False
                if ligne<len(grille) and (ligne+1, colonne) in noircies:
                    return False

                if colonne>0 and (ligne, colonne-1) in noircies:
                    return False
                if colonne<len(grille[ligne]) and (ligne, colonne+1) in noircies:
                    return False
    return True
    
    
def limite_grille(grille, ligne, colonne):
    '''renvoit True si la case est dans le plateau, False sinon'''
    return ((0<=ligne<len(grille)) and 0<=colonne<len(grille[ligne]))


def voisins(ligne, colonne):
    return [(ligne+1, colonne), 
            (ligne,colonne+1), 
            (ligne-1, colonne), 
            (ligne, colonne-1)]


def colorier(grille, ligne, colonne, c_nouv):
    '''fonction récursive permettant de propager un nombre'''
    c_prec=grille[ligne][colonne]
    if c_prec==c_nouv:
        return
    grille[ligne][colonne]=c_nouv
    for vi, vj in voisins(ligne, colonne):
        if (limite_grille(grille, vi, vj) and grille[vi][vj]==c_prec):
            colorier(grille, vi, vj, c_nouv)
            
def connexe(plateau, noircies):
    '''créer un plateau et le remplit en fonction de la noirceur des cases, la fonction 'colorie' récursivement les zones non noircies, si les zones blanches forment une zone, elle renvoie True, False sinon.'''
    plateau2=[]
    for ligne in range(len(plateau)):
        plateau2.append([])
        for colonne in range(len(plateau[ligne])):
            if (ligne, colonne) in noircies:
                plateau2[ligne].append(0)
            else:
                plateau2[ligne].append(1)
    c_nouv=2
    rand_colonne=randint(0, len(plateau2[0])-1)
    ligne=randint(0, len(plateau)-1)
    while plateau2[ligne][rand_colonne]!=1:
        rand_colonne=randint(0, len(plateau2))
    colorier(plateau2, ligne, rand_colonne, c_nouv)
    for ligne in range(len(plateau2)):
        for colonne in range(len(plateau2[ligne])):
            if plateau2[ligne][colonne]==1:
                return False
    return True


def come_back(grille, grille2, noircies, ligne, colonne):
    ax, ay, bx, by=case_vers_pixel(ligne, colonne)
    if grille2[ligne][colonne]==0:
        rectangle(ay, ax, by, bx, tag='jeu')
        texte(ligne*taille_case+taille_case/3+.5, colonne* taille_case+taille_case/3+.5, grille[ligne][colonne])

def creer_grille(grille, dico):
    efface('jeu')
    taille_case=600/len(grille)
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            rectangle(j*taille_case, i*taille_case,(j+1)*taille_case, (i+1)*taille_case,remplissage=dico[grille[i][j]],tag='jeu')
            
def pixel_vers_case(x, y):
    return (y//taille_case, x//taille_case) 
    
def placer_grille(grille):
    taille_case=600/len(grille)
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            texte(i*taille_case+taille_case/3+.5, j* taille_case+taille_case/3+.5, grille[i][j])

def case_noircies(grille, grille2, noircies, ligne, colonne, dico):
    
    ligne, colonne=int(ligne), int(colonne)
    if grille2[ligne][colonne]==0:
        grille2[ligne][colonne]=1
        noircies.add((ligne, colonne))
    elif grille2[ligne][colonne]==1:
        grille2[ligne][colonne]=0
        noircies.discard((ligne, colonne))
        i, j=ligne, colonne
        ax, ay, bx, by=case_vers_pixel(ligne, colonne)
        rectangle(ay, ax, by, bx, remplissage=dico[grille[i][j]],tag='jeu')
        placer_grille(grille)
        
def menu():
    couleurs=["green", "midnight blue", "purple", "coral4"]
    rectangle(20,20,580,100, couleur="red",remplissage="red" ,epaisseur=3)
    texte(125,45, "Projet d'AP2 : HITORI", couleur="black")
    texte(100, 250,"Bienvenue sur notre jeu !")
    i=0
    while i<10000000000:
        rectangle(20, 400, 580, 500, couleur=couleurs[i], remplissage=couleurs[i], epaisseur=3)
        texte(38, 430, "Cliquez pour selectionner une grille ! :D", taille=23, couleur="white")
        attente(0.8)
        if i==len(couleurs)-1:
            i=0
            continue
        i+=1
def menu_mode():
    rectangle(20,20,580,100, remplissage="blue")
    texte(115, 40, "Choix du mode de jeu :", couleur="white", taille=27)
    rectangle(100,175,500,230, remplissage="snow")
    texte(200,185,"Mode Manuel")
    rectangle(100,275,500,330, remplissage="snow")
    texte(200,285,"Solveur naïf")
    rectangle(100,375,500,430, remplissage="snow")
    texte(180,385,"Solveur avancé")
    
def menu_grille():
    rectangle(0,0,600,600, remplissage="snow")
    texte(175,15, "Choix de la grille")
    rectangle(80,100,520,150, remplissage="green")
    texte(230,105,"Niveau 1")
    rectangle(80, 200, 520, 250, remplissage="yellow")
    texte(230,205,"Niveau 2")
    rectangle(80, 300, 520, 350, remplissage="orange")
    texte(230, 305, "Niveau 3")
    rectangle(80, 400, 520, 450, remplissage="tomato")
    texte(230, 405, "Niveau 4")
    rectangle(80, 500, 520, 550, remplissage="red")
    texte(230, 505, "Niveau 5")
    
def case_vers_pixel(x, y):
    return x*taille_case, y*taille_case, (x+1)*taille_case-1, (y+1)*taille_case-1
    
def creer_grille2(grille):
    grille2=[]
    for ligne in range(len(grille)):
        grille2.append([])
        for colonne in range(len(grille[ligne])):
            grille2[ligne].append(0)
    return grille2
    
def menu_pause():
    i=0
    rectangle(100,145,500,200, remplissage="snow")
    texte(113,155 ,"Charger une nouvelle grille")
    rectangle(100,245,500,300, remplissage="snow")
    texte(190, 255, "Recommencer")
    rectangle(100,355,500,400, remplissage="snow")
    texte(240, 360, "Quitter")
    while i<1000000000:
        if i%2==0:
            texte(225,15,"PAUSE",couleur="red", taille=30)
        else:
            texte(225,15,"PAUSE",couleur="black", taille=30)
        i+=1
        attente(0.7)
        
def noirceur(grille2, ligne, colonne):
    ax, ay, bx, by=case_vers_pixel(ligne, colonne)
    if grille2[ligne][colonne]==1:
        rectangle(ay, ax, by, bx, remplissage='black', tag='jeu')
    
def menu():
    rectangle(20,20,580,100, couleur="red", epaisseur=3)
    texte(125,45, "Projet d'AP2 : HITORI", couleur="red")
    texte(100, 250,"Bienvenue sur notre jeu !")
    rectangle(20, 400, 580, 500, couleur="green", epaisseur=3)
    texte(38, 430, "Cliquez pour selectionner une grille ! :D", taille=23)
    


def dico_couleurs():
    dico={}
    couleurs=["red", "yellow", "purple", "pink", "green", "grey", "brown", "blue", "orange", "magenta"]
    for i in range(len(couleurs)):
        dico[i]=couleurs[i]
    return dico


grille=lire_grille('niveau1.txt')
print(grille)
grille2=creer_grille2(grille)
noircies=set()
couleurs=dico_couleurs()

cree_fenetre(600,600)
#menu()
taille_case=600/len(grille)
creer_grille(grille, couleurs)
placer_grille(grille)

while True :
    x, y=attend_clic_gauche()
    ligne, colonne=pixel_vers_case(x, y)
    ligne, colonne=int(ligne), int(colonne)
    case_noircies(grille, grille2, noircies, ligne, colonne, couleurs)
    noirceur(grille2, ligne, colonne)
    print(ligne, colonne)
    print(grille2)
    print(noircies)
attente(3)
    
    
attend_fermeture()



    
    
