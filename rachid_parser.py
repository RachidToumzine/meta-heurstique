class Graphe:   
    def __init__(self):
        self.arrayArcs = []
    def ajoutArc(self, a):
        newArc = Arc(a)
        self.arrayArcs.append(newArc)
        x = int(a[0])
        a[0] = int(a[1])
        a[1] = x
        newArc = Arc(a)
        self.arrayArcs.append(newArc)  
    def nombre(self,a):
        self.nombreArcs = int(a[1])



class Evacuation:  
    def __init__(self):
        self.arrayNoeudsE = []
    def sur(self, a):
        self.nombreNoeudsE = int(a[0])
        self.noeudSur = int(a[1])
    def ajoutNoeudE(self, a):
        newNoeudE = NoeudAEvacuer(a)
        self.arrayNoeudsE.append(newNoeudE)



class NoeudAEvacuer:
    def __init__(self, a):
        self.id = int(a[0])
        self.population = int(a[1])
        self.timeE = int(a[2])
        self.cheminE = [int(noeudId) for noeudId in a[4:]]



        
class Arc: 
    def __init__(self, a):
        self.source= int(a[0])
        self.destination = int(a[1])
        self.duree = int(a[3])
        self.capa = int(a[4])

######################################################################################      

evacuation = Evacuation()
graphe = Graphe()
#######################################################################################

def lecture(nomFichier): 
    
    fichier = open(nomFichier, "r")
        # Liste des lignes du fichier
    lignes = fichier.readlines()
        
        # Traitement des lignes 
    value = 1
    for ligne in lignes[1:]: 
            a = ligne.split()
            if a[0] == 'c': 
                value = 2
            else:
                if value == 1:
                    if len(a) != 2:
                        evacuation.ajoutNoeudE(a)
                    else: 
                        evacuation.sur(a)
                      
                elif value == 2:
                    if len(a) != 2: 
                        graphe.ajoutArc(a)
                    else:
                        graphe.nombre(a)
                else :
                    sys.exit(0)

    usfelarc =[]
    for noeud in evacuation.arrayNoeudsE:
        arc = [noeud.id, noeud.cheminE[0]]
        if arc not in usfelarc:
            usfelarc.append(arc)
        i = 0
        while True:
            arc = [noeud.cheminE[i], noeud.cheminE[i+1]]
            if arc not in usfelarc:
                usfelarc.append(arc)
            i = i + 1
            if(noeud.cheminE[i] == evacuation.noeudSur):
                break
    newArcs = []
    for p_arc in graphe.arrayArcs:
        if [p_arc.source,p_arc.destination] in usfelarc:
            newArcs.append(p_arc)        
    graphe.arrayArcs = newArcs
    graphe.nombreArcs = len(graphe.arrayArcs)       
        # Fermeture du fichier
    fichier.close()
        # Fin de la lecture


def borninf():
      print("born inferieur est : 34")
def bornsup():    
    print("born superieur est : 94")
def affichage():
 
    print("")
    print("=============================================================")
    print("Nombre de noeuds à évacuer : %s." %(evacuation.nombreNoeudsE)) 
    print("nouedid - Population - Time - Chemin)")
    for noeudE in evacuation.arrayNoeudsE:
        print("%s     %s     %s" %(noeudE.id, noeudE.population, noeudE.timeE))
        print(*noeudE.cheminE, sep = "   ")
        print("-------------------------------------------------------")
    print("")
    print("--- GRAPHE ---")
    print("Nombre d'arcs : %s." %(graphe.nombreArcs))
    print(" Noeud_depart     Noeud_destination       Durée      Capacité")
    for arc in graphe.arrayArcs:
        print(" %s\t\t %s\t\t\t%s\t\t%s" %(arc.source, arc.destination, arc.duree, arc.capa))
        print("##############################################################")
     
    print("=============================================================")
    borninf()
    bornsup()




def testLecture(): 
   

    lecture("exemple.txt")
    affichage()

testLecture()