import math

# Declaration de la structure des arcs d'evacuation
# evacnodesmap --> dictionnaire { "idnode 1": [ "idnode safe",
#                                               "population",
#                                               "evacuation max rate",
#                                               "evacuation node 1",
#                                               "..."",
#                                               " evacuation node k"],
#                                 "idnode 2": [...]}
evacnodesmap = {}

# Evacedges --> dictionnaire { "idedge 1": ["node 1", "node 2", "duedate", "length", "capacity", [block lists]],
#                              "idedge 2": [...]}
evacedgesplan = {}

# Declaration de la structure globale des noeuds du graphe d'evacuation
# evacplan --> dictionnaire {"idnode 1": [ ["predecessor node 1", "predecessor node 2", ...],
#                                          "successor node",
#                                          ["Start of Evacuation Time at node", "End of Evacuation Time at node", "Start of Evacuation Time at successor", "End of Evacuation Time at successor", "People per Time unit", "Time to evacuate from 'idnode' to Successor", "Maxx Authorized People per Time unit] ],
#                            "idnode 2": [...] }
evacplan = {}

def traiter(src, dst):
    """Fonction de traitement.
 
    Lit et traite ligne par ligne le fichier source (src).
    Les résultats sont ensuite écrit dans le fichier destination (dst). 
    """
    global evacplan
    global evacnodesmap
    global evacedgesplan

    # Lecture de l'entete de declaration des noeuds
    entetenodes = src.readline().rstrip('\n\r').split(" ")
    
    # Lecture de la declaration des noeuds
    nodecount = src.readline().rstrip('\n\r').split(" ")
    redzones = int(nodecount[0])
    safezone = nodecount[1]


    # Evacnodelist --> liste des noeuds utilisés dans le plan d'evacuation
    evacnodelist = []

    # Preparation du fichier destination pour la declaration des noeuds
    dst.write("Declaration des noeuds à évacuer\n")
    dst.write("--------------------------------\n\n")
    
    # Lecture et traitement des lignes des noeuds
    for i in range(redzones):
        nodeline = src.readline().rstrip('\n\r').split(" ")
        evacnodesmap.update({nodeline[0]:[nodeline[0], nodeline[1], nodeline[2]]})

        # Ecriture des informations du noeuds dans le fichier destination
        dst.write("id noeud: %s\n" % evacnodesmap[nodeline[0]][0])
        dst.write("   population: %s / evac. max rate: %s\n" % (evacnodesmap[nodeline[0]][1], evacnodesmap[nodeline[0]][2]))
        dst.write("   noeuds d'evacuation:")
        
        if evacnodelist.count(nodeline[0]) == 0:
                evacnodelist.append(nodeline[0])

        # Preparation du graphe d'evacuation
        # Cas des Red Zones
        if nodeline[0] not in evacplan:
            MaxPopEvacRate = int(nodeline[2])
            EndEvacSucc = math.ceil(int(nodeline[1]) / int(MaxPopEvacRate))
            evacplan.update({nodeline[0]:[[], nodeline[4], [0, EndEvacSucc, 0, EndEvacSucc, MaxPopEvacRate]]})
        
        # Traitement des noeuds du chemin d'evacuation
        evacnodecount = int(nodeline[3])
        for j in range(evacnodecount):
            # noeud courant
            nodek = nodeline[4+j]
            evacnodesmap[nodeline[0]].append(nodek)

            # Noeud predecesseur
            if nodek == safezone and evacnodecount == 1:
                nodekpred = nodeline[0]
            elif j == 0:
                nodekpred = nodeline[0]
            else:
                nodekpred = nodeline[3+j]

            # noeud successeur
            if nodek == safezone:
                nodeksucc = "X"
            else:
                nodeksucc = nodeline[5+j]
            
            # Ecriture des noeuds du chemin d'evacuation dans le fichier destination
            dst.write(" %s" % (evacnodesmap[nodeline[0]][3+j]))

            # Mise a jour de la liste des noeuds utilise dans le cas d'etude
            if evacnodelist.count(nodek) == 0:
                evacnodelist.append(nodek)

            # Mise à jour du graphe d'evacuation avec les noeuds du chemin d'evacuation
            if nodek not in evacplan:
                evacplan.update({nodek:[[nodekpred], nodeksucc, []]})
            elif evacplan[nodek][0].count(nodekpred) == 0:
                evacplan[nodek][0].append(nodekpred)

        # Verification que le dernier noeud correspond bien a la zone safe
        dst.write("\n")
        if evacnodesmap[nodeline[0]][-1] == safezone:
            dst.write("   --> chemin pour evacuation OK\n")
        else:
            dst.write("   --> chemin pour evacuation NOK\n")
        
        dst.write("\n***\n\n")

        
    # Lecture des entetes de declaration des arcs d'evacuation
    enteteedges = src.readline().rstrip('\n\r').split(" ")
    edgescount = src.readline().rstrip('\n\r').split(" ")

    global evacedgesplan
    # Initialisation des edge id
    i = 1

    # Preparation du fichier destination pour la declaration des arcs d'evacuation
    dst.write("Déclaration des arcs d'evacuation\n")
    dst.write("---------------------------------\n\n")
    
    # Lecture et traitement des lignes des arcs
    for restlines in src:
        edgeline = restlines.rstrip('\n\r').split(" ")
        if edgeline == [""]:
            continue
        
        node1 = edgeline[0]
        node2 = edgeline[1]

        # Traitement de la ligne si les noeuds de l'arc sont tous les deux dans evacnodelist
        if (evacnodelist.count(node1) != 0) and (evacnodelist.count(node2) != 0):
            evacedgesplan.update({i:[node1, node2, int(edgeline[2]), int(edgeline[3]), int(edgeline[4])]})

            # Ecriture des arcs de destination
            dst.write("arc id: %s\n" % (i))
            dst.write("   noeud 1: %s\n   noeud 2: %s\n" % (evacedgesplan[i][0], evacedgesplan[i][1]))
            dst.write("   duedate: %s\n" % (evacedgesplan[i][2]))
            dst.write("   time to travel: %s / capacity: %s\n" % (evacedgesplan[i][3], evacedgesplan[i][4]))
            dst.write("\n")

            # Incrementation du edge id
            i = i+1

    # Mise à jour des informations liées aux edges dans evacplan
    for x in evacplan:
        for y in evacedgesplan:
            if evacedgesplan[y][1] == x:
                pass





if __name__ == '__main__':
    # Ouverture du fichier source
    source = open("indata.txt", "r")

    # Ouverture du fichier destination
    destination = open("outdata.txt", "w")

    # ouverture du fichier solution proposé
    solution = open("insol.txt", "r")

    try:
        # Appeler la fonction de traitement
        traiter(source, destination)

        destination.write("\n***\n\n")
        destination.write("Structure 'evacplan' après traitement :\n")
        sorted(evacplan)
        for x in evacplan:
            destination.write("%s: %s\n" % (x, evacplan[x]))
        destination.write("\n")
        destination.write("*** END OF FILE ***\n")

    finally:
        # Fermeture du fichier destination
        destination.close()

        # Fermerture du fichier source
        source.close()