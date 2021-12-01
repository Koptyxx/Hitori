from random import randint
import os
os.chdir(r"C:\Users\\Gamer\Desktop\\AP2\\Projet AP2")


'''def sans_conflit(grille, noircies):
    for i in range(len(grille)-1):
        for j in range(len(grille[i])-1):
            if j<len(grille[i])-1 and i<len(grille)-1 and (grille[i][j]==grille[i][j+1] or grille[i][j]==grille[i+1][j]) and grille[i][j] not in noircies:
                print(grille[i][j])
                return False 
    return True'''
    
def sans_conflit(grille, noircies):
    colonne=[]
    ligne=[]
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            ligne.append(grille[i][j])
            if (i, j) in noircies:
                ligne.remove(grille[i][j])
            if ligne.count(grille[i][j])>1:
                
                
                return False
        ligne=[]
    for a in range(len(grille)):
        for b in range(len(grille[a])):
            colonne.append(grille[b][a])
            if (b, a) in noircies:
                colonne.remove(grille[b][a])
        for k in range(len(colonne)):
            if colonne.count(colonne[k])>1:
                print((a, k))
                print(colonne[k])
                return False
        colonne=[]
    return True




def Sans_voisines_noircies(grille, noircies):
    for ligne in range(len(grille)):
        for colonne in range(len(grille[ligne])):

            if (ligne, colonne) not in noircies:
                continue

            if (ligne, colonne) in noircies:
                
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
    rand_ligne=randint(0, len(plateau2)-1)
    while plateau2[rand_ligne][rand_colonne]!=1:
        rand_colonne=randint(0, len(plateau2[0])-1)
    colorier(plateau2, rand_ligne, rand_colonne, c_nouv)
    for ligne1 in range(len(plateau2)):
        for colonne1 in range(len(plateau2[ligne1])):
            if plateau2[ligne1][colonne1]==1:
                return False
    return True
    
def ligne_cellule(grille, i, j):
    grille2=grille*1
    ligne=grille2[i]
    cellule=ligne[j]
    ligne.pop(j)
    return ligne
    
def colonne_cellule(grille, i , j):
    grille3=grille*1
    colonne=[]
    print(grille3)
    for k in range(len(grille3)):
        
        colonne.append(grille3[k][j])
    colonne.pop(j)
    return colonne

def solveur_naif(i, j, grille, noircies):
    print(noircies)
    ligne = grille[i] #ligne 127 à 131 : set up des comparatifs
    colonne=[]
    for k in range(len(grille)):
        colonne.append(grille[k][j])
    cellule=grille[i][j]
    if i>len(grille)-2 and j>len(grille[i])-2:
        
        return None                             #Si les indices dépassent la grille et que l'on a toujours pas trouvé de solutions, il n'y a plus de solutions possible.
    if Sans_voisines_noircies(grille, noircies)==False or connexe(grille,noircies)==False: #Si l'une des règles 2 et 3 enfreinte alors grille invalide.
        
        return None
    if Sans_voisines_noircies(grille, noircies)==True and connexe(grille, noircies)==True and sans_conflit(grille, noircies)==True: #Si grille valide, on return la solution
        #print('test')
        return noircies
    
    else:
        
        if ligne.count(cellule)==1 and colonne.count(cellule)==1: #Si aucune case n'est en conflit on continue sans noircir la case.
            
            if j==len(grille[i])-1:
                res=solveur_naif(i+1, 0, grille, noircies)
            else:
                res=solveur_naif(i, j+1, grille, noircies)
        else: #Sinon on continue en noircicant la case
            noircies.add((i, j))
            if j==len(grille[i])-1:
                res=solveur_naif(i+1, 0, grille, noircies)
            else:
              res=solveur_naif(i, j+1, grille, noircies)
            if res is not None: #Si une solution est trouvé on la renvoi
                return res
            else: # sinon on rend à nouveau visible la cellule (i, j) et on cherche une solution à partir de la cellule suivante
                noircies.remove((i, j))
                if j==len(grille[i])-1:
                    res=solveur_naif(i+1, 0, grille, noircies)
                else:
                    res=solveur_naif(i, j+1, grille, noircies)
                if res is not None: #si une solution est trouvée on la renvoie, sinon c’est qu’il ne peut exister de solution depuis la configuration actuelle, il faut donc renvoyer None.
                    return res
                else:
                    return None
def affiche_grille(ldl):
    for i in range(len(ldl)):
        lst=ldl[i]*1
        for j in range(len(lst)):
            lst[j]=str(lst[j])
        s=" "
        print(s.join(lst))
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
    
grille1=[[9, 3,16 , 0], [4, 6, 2, 3], [7, 6, 8, 1], [1, 7, 1, 4]]

grille=lire_grille('niveau1.txt')
grille5=lire_grille('niveau5.txt')
affiche_grille(grille1)
noircies=set()

#print(sans_conflit(grille, noircies))

print(solveur_naif(0 ,0 , grille1, noircies))




test=set()
test1=set()
test1.add((0, 1))
test1.update([(1, 1), (1, 2), (1, 3)])
'''
test2=set()
test2.add((0, 0))
print(test1)'''
#print(connexe(grille1, test1))

#A FAIRE : + de IF !!!!!!!!!!!!!!!!!!!!