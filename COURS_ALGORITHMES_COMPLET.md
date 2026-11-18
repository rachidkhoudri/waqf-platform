# CONCEPTION ET ANALYSE D'ALGORITHMES
## Support de Cours Complet - 21h

**Niveau :** Master / Ingénierie Informatique  
**Prérequis :** Algorithmique, Structures de données avancées, Programmation  
**Références principales :**
- Cormen, Leiserson, Rivest, Stein - *Introduction to Algorithms* (CLRS), 3e éd., MIT Press
- Kleinberg, Tardos - *Algorithm Design*, Pearson
- Sedgewick, Wayne - *Algorithms*, 4e éd., Addison-Wesley
- Aho, Hopcroft, Ullman - *Data Structures and Algorithms*, Addison-Wesley

---

## TABLE DES MATIÈRES

1. [Introduction à la complexité algorithmique et notions préliminaires](#chapitre-1)
2. [Analyse de la complexité temporelle](#chapitre-2)
3. [Structures de données et complexité](#chapitre-3)
4. [Techniques d'analyse de complexité](#chapitre-4)
5. [Complexité spatiale](#chapitre-5)
6. [Complexité et Preuve de Correction](#chapitre-6)
7. [Optimisation d'algorithmes](#chapitre-7)

---

# CHAPITRE 1 : INTRODUCTION À LA COMPLEXITÉ ALGORITHMIQUE ET NOTIONS PRÉLIMINAIRES <a name="chapitre-1"></a>

## 1.1 Objectifs Pédagogiques
À la fin de ce chapitre, l'étudiant sera capable de :
- Définir formellement un algorithme et l'algorithmique
- Caractériser un problème algorithmique
- Expliquer l'intérêt de l'analyse de complexité
- Distinguer complexité temporelle et spatiale

## 1.2 Contenu Théorique Détaillé

### 1.2.1 Définition d'algorithme et d'algorithmique

**Définition formelle (Knuth, 1973) :** Un algorithme est une suite finie d'instructions non ambiguës, exécutables mécaniquement, qui prend en entrée une instance de problème et produit en sortie la solution correspondante, en terminant après un nombre fini d'étapes.

**Cinq caractéristiques essentielles (Knuth) :**
1. **Finitude** : L'algorithme se termine après un nombre fini d'étapes
2. **Non-ambiguïté** : Chaque instruction est précise et sans équivoque
3. **Entrées** : Zéro ou plusieurs quantités données initialement
4. **Sorties** : Une ou plusieurs quantités produites, en relation avec les entrées
5. **Effectivité** : Chaque instruction est suffisamment basique pour être exécutée en principe par un humain avec papier et crayon

**Algorithmique :** Discipline qui étudie la conception, l'analyse, l'implémentation et l'optimisation des algorithmes.

### 1.2.2 Notion de problème algorithmique et sa résolution

**Problème algorithmique :** Relation entre un ensemble d'entrées (instances) et un ensemble de sorties valides.

**Exemple - Problème de tri :**
- Entrée : Séquence de n nombres ⟨a₁, a₂, ..., aₙ⟩
- Sortie : Permutation ⟨a'₁, a'₂, ..., a'ₙ⟩ telle que a'₁ ≤ a'₂ ≤ ... ≤ a'ₙ

**Résolution :** Passage de la spécification du problème à un algorithme correct et efficace.

### 1.2.3 Pourquoi analyser la complexité ?

**Comparaison d'algorithmes pour un même problème :**

| Algorithme | Tri de 1000 éléments | Tri de 1,000,000 éléments |
|------------|---------------------|--------------------------|
| Tri par insertion O(n²) | ~0.001 s | ~1000 s (16 min) |
| Tri fusion O(n log n) | ~0.0001 s | ~0.2 s |

**L'analyse de complexité permet de :**
- Prédire le comportement sur de grandes entrées
- Comparer des algorithmes indépendamment du matériel
- Identifier les goulots d'étranglement
- Guider la conception d'algorithmes efficaces

### 1.2.4 Notions de base et types de complexité

**Complexité temporelle :** Nombre d'opérations élémentaires en fonction de la taille n de l'entrée.

**Complexité spatiale :** Quantité de mémoire utilisée en fonction de n.

**Modèle de calcul : RAM (Random Access Machine)**
- Mémoire : suite de cellules adressables
- Opérations de base : +, -, ×, /, comparaisons, affectations, accès mémoire → coût unitaire
- Instructions s'exécutent séquentiellement

---

## 1.3 Exercices Résolus

### Exercice 1.1 : Identification d'algorithme
**Énoncé :** Parmi les descriptions suivantes, lesquelles correspondent à un algorithme au sens formel ?

a) "Pour faire un gâteau, mélanger les ingrédients, mettre au four, attendre qu'il soit cuit."
b) "Pour trouver le maximum d'un tableau : initialiser max avec le premier élément, puis pour chaque élément suivant, si il est plus grand que max, le mettre dans max."
c) "Résoudre l'équation x² + 1 = 0 dans ℝ."

**Solution :**
- a) **Non** : Instructions ambiguës ("mélanger", "attendre qu'il soit cuit"), pas de condition d'arrêt précise
- b) **Oui** : Fini, non-ambigu, entrée/sortie définies, effectif
- c) **Non** : Pas de solution dans ℝ, l'algorithme ne terminerait pas ou échouerait

### Exercice 1.2 : Modèle RAM - Coût d'opérations
**Énoncé :** Dans le modèle RAM, donnez le coût en temps des fragments suivants en fonction de n :

```python
# Fragment A
somme = 0
for i in range(n):
    somme += i

# Fragment B
for i in range(n):
    for j in range(n):
        print(i, j)

# Fragment C
i = n
while i > 0:
    i = i // 2
```

**Solution :**
- **Fragment A** : n itérations × O(1) = **O(n)**
- **Fragment B** : n × n itérations × O(1) = **O(n²)**
- **Fragment C** : Division par 2 répétée → ⌊log₂ n⌋ + 1 itérations = **O(log n)**

---

## 1.4 Questions Théoriques avec Réponses Modèles

### Q1.1 : Définissez formellement un algorithme. Donnez les 5 caractéristiques de Knuth.
**Réponse :** Voir section 1.2.1. Un algorithme est une suite finie d'instructions non ambiguës... Les 5 caractéristiques : Finitude, Non-ambiguïté, Entrées, Sorties, Effectivité.

### Q1.2 : Quelle est la différence entre un problème et une instance de problème ?
**Réponse :** Un **problème** est la description générale de la relation entrée/sortie (ex: "tri"). Une **instance** est une entrée concrète (ex: le tableau [5, 2, 8, 1]).

### Q1.3 : Pourquoi la complexité asymptotique est-elle plus pertinente que le temps d'exécution réel pour comparer des algorithmes ?
**Réponse :** Le temps réel dépend du matériel, du langage, du compilateur, de la charge système. La complexité asymptotique capture le comportement intrinsèque de l'algorithme pour de grandes tailles d'entrée, indépendamment de ces facteurs.

### Q1.4 : Dans le modèle RAM, quel est le coût d'un accès à un élément de tableau A[i] ?
**Réponse :** O(1) - coût unitaire, car la mémoire est adressable directement.

---

# CHAPITRE 2 : ANALYSE DE LA COMPLEXITÉ TEMPORELLE <a name="chapitre-2"></a>

## 2.1 Objectifs Pédagogiques
- Maîtriser la notation grand O, Ω, Θ
- Calculer la complexité de boucles imbriquées et fonctions récursives
- Distinguer cas pire, meilleur, moyen
- Identifier les classes de complexité courantes

## 2.2 Contenu Théorique Détaillé

### 2.2.1 Notation grand O, Ω, Θ (Notations de Landau)

**Définitions formelles :**

Soient f(n) et g(n) des fonctions définies sur ℕ → ℝ⁺.

**O(g(n)) = { f(n) | ∃ c > 0, ∃ n₀ ≥ 0 : ∀ n ≥ n₀, 0 ≤ f(n) ≤ c·g(n) }**  
*Majorant asymptotique (borne supérieure)*

**Ω(g(n)) = { f(n) | ∃ c > 0, ∃ n₀ ≥ 0 : ∀ n ≥ n₀, 0 ≤ c·g(n) ≤ f(n) }**  
*Minorant asymptotique (borne inférieure)*

**Θ(g(n)) = { f(n) | ∃ c₁, c₂ > 0, ∃ n₀ ≥ 0 : ∀ n ≥ n₀, 0 ≤ c₁·g(n) ≤ f(n) ≤ c₂·g(n) }**  
*Encadrement asymptotique (borne serrée)*

**Interprétation :**
- f(n) = O(g(n)) : "f croît au plus aussi vite que g"
- f(n) = Ω(g(n)) : "f croît au moins aussi vite que g"
- f(n) = Θ(g(n)) : "f croît à la même vitesse que g"

**Propriétés utiles :**
- Transitivité : f = O(g) et g = O(h) ⇒ f = O(h)
- Réflexivité : f = O(f), f = Θ(f)
- Symétrie : f = Θ(g) ⇔ g = Θ(f)
- Transposition : f = O(g) ⇔ g = Ω(f)

### 2.2.2 Calcul de la complexité

#### Identification des opérations élémentaires
Opérations à coût unitaire dans le modèle RAM :
- Opérations arithmétiques : +, -, ×, /, %
- Comparaisons : <, >, ≤, ≥, ==, !=
- Affectations : x = expr
- Accès mémoire : tableau[i], objet.champ
- Appels de fonction (sans compter le corps)

#### Analyse des boucles

**Boucle simple :**
```python
for i in range(n):          # n itérations
    instruction_O(1)        # coût constant
# Complexité : n × O(1) = O(n)
```

**Boucles imbriquées :**
```python
for i in range(n):          # n itérations
    for j in range(m):      # m itérations
        instruction_O(1)
# Complexité : n × m × O(1) = O(n×m)
# Si m = n : O(n²)
```

**Boucle avec pas variable :**
```python
for i in range(0, n, 2):    # n/2 itérations
    instruction_O(1)
# Complexité : O(n)
```

**Boucle géométrique :**
```python
i = 1
while i < n:                # log₂ n itérations
    i = i * 2
    instruction_O(1)
# Complexité : O(log n)
```

#### Analyse des fonctions récursives

**Méthode de substitution / arbre de récurrence / théorème maître**

**Exemple - Factorielle :**
```python
def fact(n):
    if n <= 1: return 1
    return n * fact(n-1)
```
Récurrence : T(n) = T(n-1) + O(1), T(1) = O(1)  
Solution : T(n) = O(n)

**Exemple - Tri fusion :**
```python
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)  # O(n)
```
Récurrence : T(n) = 2T(n/2) + O(n)  
Par théorème maître : **T(n) = Θ(n log n)**

### 2.2.3 Cas pire, meilleur, moyen

| Algorithme | Meilleur cas | Pire cas | Cas moyen |
|------------|-------------|----------|-----------|
| Recherche linéaire | Θ(1) | Θ(n) | Θ(n) |
| Tri par insertion | Θ(n) | Θ(n²) | Θ(n²) |
| Tri fusion | Θ(n log n) | Θ(n log n) | Θ(n log n) |
| QuickSort | Θ(n log n) | Θ(n²) | Θ(n log n) |
| Recherche dichotomique | Θ(1) | Θ(log n) | Θ(log n) |

**Note :** Le cas moyen suppose une distribution de probabilité sur les entrées (souvent uniforme).

### 2.2.4 Classes de complexité courantes

| Notation | Nom | Exemples |
|----------|-----|----------|
| O(1) | Constante | Accès tableau, push/pop pile |
| O(log n) | Logarithmique | Recherche dichotomique, opérations tas |
| O(√n) | Racine carrée | Test de primalité naïf |
| O(n) | Linéaire | Parcours tableau, recherche linéaire |
| O(n log n) | Linéarithmique | Tri fusion, tri par tas, QuickSort (moyen) |
| O(n²) | Quadratique | Tri bulle, tri insertion, boucles imbriquées |
| O(n³) | Cubique | Multiplication matrices naïve, Floyd-Warshall |
| O(2ⁿ) | Exponentielle | Voyageur de commerce (force brute), sous-ensembles |
| O(n!) | Factorielle | Permutations, TSP exact par énumération |

**Hiérarchie :** O(1) ⊂ O(log n) ⊂ O(√n) ⊂ O(n) ⊂ O(n log n) ⊂ O(n²) ⊂ O(n³) ⊂ O(2ⁿ) ⊂ O(n!)

---

## 2.3 Exercices Résolus

### Exercice 2.1 : Notations asymptotiques
**Énoncé :** Classez les fonctions suivantes par ordre de croissance asymptotique croissante :
n², 2ⁿ, n log n, n³, log n, n, 1, n!, √n, n^log n

**Solution :**
1. **1** = Θ(1)
2. **log n** = Θ(log n)
3. **√n** = Θ(n^0.5)
4. **n** = Θ(n)
5. **n log n** = Θ(n log n)
6. **n²** = Θ(n²)
7. **n³** = Θ(n³)
8. **n^log n** = Θ(n^log n)  [croît plus vite que tout polynôme]
9. **2ⁿ** = Θ(2ⁿ)
10. **n!** = Θ(n!)  [par Stirling : n! ~ √(2πn)(n/e)ⁿ]

### Exercice 2.2 : Analyse de boucles complexes
**Énoncé :** Déterminez la complexité temporelle exacte (en Θ) de :

```python
# A
for i in range(n):
    for j in range(i, n):
        print(i, j)

# B
i = 1
while i < n:
    j = 1
    while j < n:
        j = j * 2
    i = i + 1

# C
for i in range(n):
    for j in range(i*i):
        print(j)
```

**Solution :**

**A :** Σᵢ₌₀ⁿ⁻¹ (n - i) = n + (n-1) + ... + 1 = n(n+1)/2 = **Θ(n²)**

**B :** Boucle externe : n itérations. Boucle interne : log₂ n itérations. Total : **Θ(n log n)**

**C :** Σᵢ₌₀ⁿ⁻¹ i² = (n-1)n(2n-1)/6 = **Θ(n³)**

### Exercice 2.3 : Récurrence - Théorème maître
**Énoncé :** Résolvez les récurrences suivantes par le théorème maître (T(n) = aT(n/b) + f(n)) :

a) T(n) = 4T(n/2) + n²
b) T(n) = 2T(n/2) + n³
c) T(n) = 3T(n/4) + n log n
d) T(n) = 7T(n/2) + n²

**Solution :**

Rappel : n^log_b(a) compare à f(n)
- Cas 1 : f(n) = O(n^{log_b(a) - ε}) → T(n) = Θ(n^{log_b(a)})
- Cas 2 : f(n) = Θ(n^{log_b(a)} log^k n) → T(n) = Θ(n^{log_b(a)} log^{k+1} n)
- Cas 3 : f(n) = Ω(n^{log_b(a) + ε}) + régularité → T(n) = Θ(f(n))

**a)** a=4, b=2 → log₂4 = 2. f(n) = n² = Θ(n² log⁰ n) → **Cas 2, k=0** → T(n) = **Θ(n² log n)**

**b)** a=2, b=2 → log₂2 = 1. f(n) = n³ = Ω(n^{1+ε}) avec ε=1. Régularité : 2(n/2)³ = n³/4 ≤ cn³ pour c=1/2. → **Cas 3** → T(n) = **Θ(n³)**

**c)** a=3, b=4 → log₄3 ≈ 0.79. f(n) = n log n = Ω(n^{0.79+ε}). → **Cas 3** → T(n) = **Θ(n log n)**

**d)** a=7, b=2 → log₂7 ≈ 2.81. f(n) = n² = O(n^{2.81-ε}). → **Cas 1** → T(n) = **Θ(n^{log₂7})** ≈ **Θ(n².⁸¹)**

### Exercice 2.4 : Cas moyen - Recherche linéaire
**Énoncé :** Soit un tableau de n éléments distincts. On cherche un élément x présent dans le tableau. Quelle est la complexité moyenne en nombre de comparaisons ?

**Solution :**
Probabilité que x soit à la position i : 1/n pour chaque i ∈ {1, ..., n}
Comparaisons si x à position i : i
Moyenne = (1/n) × Σᵢ₌₁ⁿ i = (1/n) × n(n+1)/2 = (n+1)/2 = **Θ(n)**

---

## 2.4 Questions Théoriques avec Réponses Modèles

### Q2.1 : Démontrez que n² + 3n + 5 = Θ(n²).
**Réponse :** Il faut trouver c₁, c₂, n₀ > 0 tels que c₁n² ≤ n² + 3n + 5 ≤ c₂n² pour n ≥ n₀.
Pour n ≥ 5 : n² ≤ n² + 3n + 5 ≤ n² + 3n² + 5n² = 9n² (car n ≥ 1 ⇒ n ≤ n², 5 ≤ 5n²)
Donc c₁ = 1, c₂ = 9, n₀ = 5 convient. ✓

### Q2.2 : Est-il vrai que f(n) = O(g(n)) implique g(n) = O(f(n)) ? Justifiez.
**Réponse :** **Faux**. Contre-exemple : f(n) = n, g(n) = n². n = O(n²) mais n² ≠ O(n).
La relation O n'est pas symétrique. C'est Θ qui est symétrique.

### Q2.3 : Donnez la complexité temporelle de l'algorithme suivant et justifiez :
```python
def algo(n):
    i = n
    while i > 0:
        j = i
        while j > 0:
            j = j - 1
        i = i // 2
```
**Réponse :** Boucle externe : log₂ n itérations (division par 2). 
À l'itération k (i = n/2ᵏ), boucle interne : n/2ᵏ itérations.
Total = Σₖ₌₀^{log n} n/2ᵏ = n × Σ(1/2ᵏ) < 2n = **Θ(n)**

### Q2.4 : Expliquez pourquoi le tri par insertion a une complexité Θ(n) au meilleur cas.
**Réponse :** Meilleur cas = tableau déjà trié. La boucle interne (décalage) s'exécute 0 fois à chaque itération. Seules les comparaisons de la boucle externe (n-1 comparaisons) sont effectuées. Donc Θ(n).

---

# CHAPITRE 3 : STRUCTURES DE DONNÉES ET COMPLEXITÉ <a name="chapitre-3"></a>

## 3.1 Objectifs Pédagogiques
- Connaître les opérations de base et leurs complexités pour les structures classiques
- Choisir la structure adaptée selon les opérations fréquentes
- Comprendre l'impact du choix de structure sur la complexité globale

## 3.2 Contenu Théorique Détaillé

### 3.2.1 Tableaux (Arrays)

| Opération | Complexité | Notes |
|-----------|------------|-------|
| Accès A[i] | Θ(1) | Adressage direct |
| Recherche non trié | Θ(n) | Linéaire |
| Recherche trié (dichotomique) | Θ(log n) | Nécessite tri préalable |
| Insertion fin | Θ(1)* | *Amorti si tableau dynamique |
| Insertion début/milieu | Θ(n) | Décalage éléments |
| Suppression | Θ(n) | Décalage éléments |

### 3.2.2 Listes chaînées (Linked Lists)

| Opération | Liste simple | Liste double |
|-----------|-------------|--------------|
| Accès i-ème | Θ(i) | Θ(min(i, n-i)) |
| Recherche | Θ(n) | Θ(n) |
| Insertion début | Θ(1) | Θ(1) |
| Insertion fin | Θ(n)* | Θ(1)* |
| Insertion après nœud connu | Θ(1) | Θ(1) |
| Suppression nœud connu | Θ(n)** | Θ(1) |

*Avec pointeur queue. **Nécessite prédécesseur.

### 3.2.3 Arbres (Trees)

#### Arbre binaire de recherche (BST) - Non équilibré
| Opération | Complexité moyenne | Pire cas |
|-----------|-------------------|----------|
| Recherche | Θ(log n) | Θ(n) |
| Insertion | Θ(log n) | Θ(n) |
| Suppression | Θ(log n) | Θ(n) |
| Min/Max | Θ(log n) | Θ(n) |
| Successeur/Prédécesseur | Θ(log n) | Θ(n) |

#### Arbres équilibrés (AVL, Rouge-Noir, B-arbres)
Toutes les opérations : **Θ(log n)** garanti (hauteur = O(log n))

#### Tas (Heap) - Tas binaire
| Opération | Complexité |
|-----------|------------|
| Construction (heapify) | Θ(n) |
| Insertion | Θ(log n) |
| Extraction min/max | Θ(log n) |
| Peek (min/max) | Θ(1) |
| Augmentation clé | Θ(log n) |

### 3.2.4 Graphes

**Représentations :**
- **Matrice d'adjacence** : Espace Θ(V²), test arête Θ(1), parcours voisins Θ(V)
- **Listes d'adjacence** : Espace Θ(V+E), test arête Θ(deg), parcours voisins Θ(deg)

**Algorithmes classiques :**
| Algorithme | Complexité (Listes adj.) | Complexité (Matrice) |
|------------|-------------------------|---------------------|
| BFS/DFS | Θ(V + E) | Θ(V²) |
| Dijkstra (tas binaire) | Θ((V+E) log V) | Θ(V² log V) |
| Dijkstra (tas Fibonacci) | Θ(V log V + E) | - |
| Bellman-Ford | Θ(VE) | - |
| Floyd-Warshall | Θ(V³) | Θ(V³) |
| Kruskal (tri + UF) | Θ(E log E) | - |
| Prim (tas binaire) | Θ((V+E) log V) | Θ(V²) |
| Composantes fortement connexes (Kosaraju/Tarjan) | Θ(V+E) | - |

### 3.2.5 Table de hachage (Hash Table)

| Opération | Complexité moyenne | Pire cas |
|-----------|-------------------|----------|
| Recherche | Θ(1) | Θ(n) |
| Insertion | Θ(1) | Θ(n) |
| Suppression | Θ(1) | Θ(n) |

*En supposant une bonne fonction de hachage (hypothèse de hachage uniforme).*

---

## 3.3 Exercices Résolus

### Exercice 3.1 : Choix de structure
**Énoncé :** Vous devez maintenir un ensemble d'entiers avec les opérations : insertion, suppression, recherche du minimum, recherche d'un élément donné. Quelle structure choisir pour optimiser chaque cas ?

**Solution :**
- **Tas (Min-Heap)** : Insertion O(log n), Min O(1), Extraction min O(log n), mais recherche élément O(n)
- **Arbre équilibré (AVL/Rouge-Noir)** : Toutes opérations O(log n) - **Meilleur compromis général**
- **Table de hachage + Tas** : Recherche O(1), Min O(1), mais synchronisation complexe
- **Conclusion** : Arbre équilibré pour usage général ; Tas si min fréquent et recherche rare.

### Exercice 3.2 : Complexité BFS vs Matrice vs Listes
**Énoncé :** Graphe dense : E = Θ(V²). Graphe creux : E = Θ(V). Comparez BFS avec les deux représentations.

**Solution :**
| | Graphe creux (E=Θ(V)) | Graphe dense (E=Θ(V²)) |
|---|----------------------|------------------------|
| Listes adj. | Θ(V + V) = Θ(V) | Θ(V + V²) = Θ(V²) |
| Matrice | Θ(V²) | Θ(V²) |

**Conclusion :** Listes d'adjacence préférables pour graphes creux ; Matrice acceptable pour graphes denses ou quand tests d'arêtes fréquents.

### Exercice 3.3 : Construction de tas
**Énoncé :** Prouvez que la construction d'un tas binaire par `heapify` (procédure bottom-up) prend Θ(n) et non Θ(n log n).

**Solution :**
Analyse précise : un nœud à la hauteur h fait au maximum h échanges.
Nombre de nœuds à la hauteur h ≤ ⌈n/2^{h+1}⌉
Coût total ≤ Σₕ₌₀^{⌊log n⌋} h × ⌈n/2^{h+1}⌉ ≤ n Σₕ₌₀^∞ h/2^{h+1} = n × 1 = O(n)
(Somme Σ h/2^h = 2)
Donc **Θ(n)**.

---

## 3.4 Questions Théoriques avec Réponses Modèles

### Q3.1 : Pourquoi une liste chaînée double permet-elle la suppression en O(1) d'un nœud connu alors qu'une liste simple nécessite O(n) ?
**Réponse :** Dans une liste double, le nœud a un pointeur vers son prédécesseur, permettant de relier directement prédécesseur et successeur. Dans une liste simple, il faut parcourir depuis la tête pour trouver le prédécesseur.

### Q3.2 : Quelle est la complexité de la recherche du k-ième plus petit élément dans un BST non équilibré ? Et dans un arbre AVL ?
**Réponse :** BST non équilibré : O(n) pire cas (arbre dégénéré en liste). AVL : O(log n) garanti (hauteur O(log n)).

### Q3.3 : Donnez un exemple où l'utilisation d'une table de hachage serait déconseillée.
**Réponse :** Quand on a besoin d'opérations d'ordre (minimum, maximum, successeur, parcours trié) - les tables de hachage ne maintiennent pas l'ordre. Aussi déconseillées si fonction de hachage médiocre ou attaques par collisions (DoS).

### Q3.4 : Pourquoi Dijkstra avec tas de Fibonacci est-il théoriquement plus rapide qu'avec tas binaire, mais peu utilisé en pratique ?
**Réponse :** Tas Fibonacci : O(V log V + E) vs Tas binaire : O((V+E) log V). Mais constantes cachées énormes, structure complexe, surcoût mémoire. En pratique, tas binaire (ou pairing heap) plus performant.

---

# CHAPITRE 4 : TECHNIQUES D'ANALYSE DE COMPLEXITÉ <a name="chapitre-4"></a>

## 4.1 Objectifs Pédagogiques
- Maîtriser la stratégie "Diviser pour régner" et son analyse
- Comprendre la programmation dynamique : sous-problèmes chevauchants, optimalité
- Analyser les algorithmes gloutons : choix glouton, propriété de choix glouton, sous-structure optimale
- Savoir quand appliquer chaque technique

## 4.2 Contenu Théorique Détaillé

### 4.2.1 Diviser pour Régner (Divide & Conquer)

**Stratégie de base :**
1. **Diviser** : Décomposer le problème en sous-problèmes plus petits de même nature
2. **Régner** : Résoudre récursivement les sous-problèmes (cas de base = assez petit)
3. **Combiner** : Fusionner les solutions des sous-problèmes

**Schéma de récurrence :** T(n) = aT(n/b) + f(n)
- a = nombre de sous-problèmes
- n/b = taille de chaque sous-problème
- f(n) = coût division + combinaison

**Exemples classiques :**

| Algorithme | Récurrence | Complexité |
|------------|------------|------------|
| Tri fusion | T(n) = 2T(n/2) + Θ(n) | Θ(n log n) |
| Recherche dichotomique | T(n) = T(n/2) + Θ(1) | Θ(log n) |
| Multiplication matrices (Strassen) | T(n) = 7T(n/2) + Θ(n²) | Θ(n^{log₂7}) ≈ Θ(n^2.81) |
| Plus grand élément | T(n) = 2T(n/2) + Θ(1) | Θ(n) |

**Analyse du Tri Fusion (Merge Sort) :**
```python
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])      # T(n/2)
    right = merge_sort(arr[mid:])     # T(n/2)
    return merge(left, right)         # Θ(n)
```
Arbre de récursion : hauteur log₂ n, chaque niveau coûte Θ(n) → **Θ(n log n)**

### 4.2.2 Programmation Dynamique (Dynamic Programming)

**Deux propriétés indispensables :**
1. **Sous-structure optimale** : Une solution optimale contient des solutions optimales aux sous-problèmes
2. **Sous-problèmes chevauchants** : Les mêmes sous-problèmes sont résolus plusieurs fois (différence avec Diviser pour Régner)

**Deux approches :**
- **Mémoïsation (Top-down)** : Récursion + table de mémorisation
- **Tabulation (Bottom-up)** : Remplissage itératif de table

#### Exemple 1 : Problème du Sac à Dos (Knapsack 0/1)
**Problème :** n objets, poids wᵢ, valeur vᵢ, capacité W. Maximiser valeur sans dépasser W.

**Récurrence :**
OPT(i, w) = max valeur avec premiers i objets et capacité w
```
OPT(i, w) = 0                          si i = 0 ou w = 0
OPT(i, w) = OPT(i-1, w)                si wᵢ > w
OPT(i, w) = max(OPT(i-1, w), 
                vᵢ + OPT(i-1, w-wᵢ))   sinon
```

**Complexité :** Θ(nW) temps, Θ(nW) espace (ou Θ(W) avec optimisation)
*Note : Pseudo-polynomiale (dépend de W, pas de log W)*

#### Exemple 2 : Plus Court Chemin - Floyd-Warshall
**Problème :** Plus courts chemins entre toutes paires de sommets.
**Récurrence :**
```
dist[i][j]⁽ᵏ⁾ = min(dist[i][j]⁽ᵏ⁻¹⁾, dist[i][k]⁽ᵏ⁻¹⁾ + dist[k][j]⁽ᵏ⁻¹⁾)
```
k = sommets intermédiaires autorisés {1..k}

**Complexité :** Θ(V³) temps, Θ(V²) espace

#### Exemple 3 : Plus Longue Sous-séquence Commune (LCS)
```
LCS(X[1..i], Y[1..j]) = 
  0                              si i=0 ou j=0
  1 + LCS(X[1..i-1], Y[1..j-1])  si X[i] = Y[j]
  max(LCS(X[1..i-1], Y[1..j]), 
      LCS(X[1..i], Y[1..j-1]))   sinon
```
**Complexité :** Θ(mn) temps et espace

### 4.2.3 Algorithmes Gloutons (Greedy Algorithms)

**Principe :** Construire la solution par étapes, faisant à chaque étape le choix qui semble le meilleur **localement** (heuristique), dans l'espoir d'obtenir une solution globalement optimale.

**Deux propriétés pour optimalité :**
1. **Propriété de choix glouton** : Un choix optimal globalement peut être fait en commençant par un choix glouton
2. **Sous-structure optimale** : Le sous-problème restant après un choix glouton a une solution optimale

#### Exemple 1 : Algorithme de Dijkstra (Plus court chemin - source unique)
**Choix glouton :** À chaque étape, extraire le sommet non traité avec distance minimale.
**Preuve d'optimalité :** Par induction + propriété de relaxation. Si on a extrait u avec d[u] minimal, alors d[u] = δ(s, u) (distance réelle).

**Complexité :**
- Tableau simple : Θ(V²)
- Tas binaire : Θ((V+E) log V)
- Tas Fibonacci : Θ(V log V + E)

#### Exemple 2 : Arbre Couvrant de Poids Minimum (MST)
**Kruskal :** Trier arêtes par poids croissant, ajouter si ne crée pas de cycle (Union-Find).
**Prim :** Partir d'un sommet, ajouter arête de poids minimum connectant arbre à nouveau sommet.

**Preuve (Kruskal) :** Propriété de coupe - pour toute coupe, l'arête de poids minimum traverse l'arbre optimal.

#### Exemple 3 : Problème du Voyageur de Commerce (TSP) - Approximation
**TSP métrique (inégalité triangulaire) :** Algorithme du double arbre / Christofides (ratio 3/2).
**TSP général :** Pas d'approximation polynomial sauf si P=NP.

#### Exemple 4 : Codage de Huffman (Compression optimale)
**Choix glouton :** Fusionner les deux symboles de fréquence minimale.
**Optimalité :** Preuve par échange - tout codage optimal peut être transformé pour avoir les deux symboles les plus rares comme frères de profondeur maximale.

---

## 4.3 Exercices Résolus

### Exercice 4.1 : Diviser pour régner - Maximum et Minimum simultanés
**Énoncé :** Trouver le max et le min d'un tableau de n éléments en minimisant les comparaisons.

**Solution :**
Algorithme par paires :
```python
def min_max(arr):
    if len(arr) == 1: return (arr[0], arr[0])
    if len(arr) == 2: 
        return (min(arr), max(arr))  # 1 comparaison
    mid = len(arr) // 2
    min1, max1 = min_max(arr[:mid])
    min2, max2 = min_max(arr[mid:])
    return (min(min1, min2), max(max1, max2))  # 2 comparaisons
```
Récurrence : T(n) = 2T(n/2) + 2, T(2) = 1
Solution : **3n/2 - 2 comparaisons** (vs 2n-2 pour recherche séparée)

### Exercice 4.2 : Programmation dynamique - Produit de matrices
**Énoncé :** Chaîne de matrices A₁×A₂×...×Aₙ. Trouver l'ordre de parenthésage minimisant les multiplications scalaires.

**Solution :**
Dimensions : Aᵢ est pᵢ₋₁ × pᵢ
m[i][j] = coût min pour Aᵢ...Aⱼ
```
m[i][i] = 0
m[i][j] = min_{i≤k<j} (m[i][k] + m[k+1][j] + pᵢ₋₁·pₖ·pⱼ)
```
Complexité : **Θ(n³)** temps, Θ(n²) espace.

### Exercice 4.3 : Glouton - Rendu de monnaie
**Énoncé :** Système de pièces {1, 5, 10, 25}. L'algorithme glouton (prendre la plus grande pièce possible) est-il optimal ?

**Solution :** **Oui** pour ce système canonique.
Preuve : Pour tout montant, le nombre de pièces de 25¢ dans une solution optimale est maximal (sinon on peut remplacer 5×5¢ par 25¢, etc.). Système canonique = glouton optimal.
*Contre-exemple : {1, 3, 4} pour montant 6 : glouton donne 4+1+1=3 pièces, optimal 3+3=2 pièces.*

### Exercice 4.4 : Dijkstra - Exemple pas à pas
**Énoncé :** Appliquez Dijkstra sur le graphe : A→B(4), A→C(2), B→C(1), B→D(5), C→D(8), C→E(10), D→E(2), D→Z(6), E→Z(2). Source A.

**Solution :**
| Étape | Sommet extrait | Distances mises à jour |
|-------|----------------|------------------------|
| Init | - | A=0, autres=∞ |
| 1 | A(0) | B=4, C=2 |
| 2 | C(2) | B=min(4,2+1)=3, D=10, E=12 |
| 3 | B(3) | D=min(10,3+5)=8 |
| 4 | D(8) | E=min(12,8+2)=10, Z=14 |
| 5 | E(10) | Z=min(14,10+2)=12 |
| 6 | Z(12) | Terminé |

Chemin A→C→B→D→E→Z = 12

---

## 4.4 Questions Théoriques avec Réponses Modèles

### Q4.1 : Quelle est la différence fondamentale entre Diviser pour Régner et Programmation Dynamique ?
**Réponse :** Dans **Diviser pour Régner**, les sous-problèmes sont **disjoints** (indépendants) - ex: tri fusion. En **Programmation Dynamique**, les sous-problèmes se **chevauchent** - on résout les mêmes sous-problèmes plusieurs fois, d'où l'intérêt de la mémoïsation/tabulation.

### Q4.2 : Donnez les deux propriétés nécessaires pour qu'un algorithme glouton soit optimal. Illustrer sur l'algorithme de Kruskal.
**Réponse :**
1. **Choix glouton** : Il existe une solution optimale commençant par le choix glouton. Pour Kruskal : l'arête de poids minimum appartient à un MST (propriété de coupe).
2. **Sous-structure optimale** : Après un choix glouton, le sous-problème restant admet une solution optimale. Pour Kruskal : après ajout d'arête (u,v), contracter u,v donne un graphe où le MST complet = arête choisie + MST du graphe contracté.

### Q4.3 : Pourquoi la programmation dynamique du sac à dos est-elle pseudo-polynomiale ?
**Réponse :** Complexité Θ(nW) où W est la capacité numérique (valeur), pas sa taille en bits (log W). Si W est grand (ex: 10⁹), l'algorithme est lent malgré n petit. Un algorithme polynomial serait en O(n^c log^d W).

### Q4.4 : L'algorithme de Dijkstra fonctionne-t-il avec des arêtes de poids négatifs ? Pourquoi ?
**Réponse :** **Non**. L'invariant de Dijkstra (distance finale = distance réelle) suppose qu'ajouter une arête ne peut pas réduire la distance d'un sommet déjà extrait. Avec poids négatifs, un chemin passant par un sommet non extrait pourrait être plus court. Contre-exemple : A→B(1), B→C(-2), A→C(1). Dijkstra extrait C(1) puis B(1) → distance C finale = 1, alors que A→B→C = -1.

---

# CHAPITRE 5 : COMPLEXITÉ SPATIALE <a name="chapitre-5"></a>

## 5.1 Objectifs Pédagogiques
- Mesurer l'espace mémoire utilisé par un algorithme
- Distinguer espace auxiliaire et espace total
- Analyser les compromis temps-espace
- Calculer la complexité spatiale des algorithmes récursifs

## 5.2 Contenu Théorique Détaillé

### 5.2.1 Définition et mesure

**Complexité spatiale S(n) :** Quantité de mémoire (en mots machine) utilisée par un algorithus pour une entrée de taille n.

**Composantes :**
- **Espace d'entrée** : Taille des données d'entrée (souvent non comptée dans l'espace *auxiliaire*)
- **Espace auxiliaire** : Espace additionnel pour variables locales, pile d'appel, structures temporaires
- **Espace de sortie** : Taille de la sortie

**Convention courante :** Complexité spatiale = espace auxiliaire (hors entrée/sortie)

### 5.2.2 Analyse de la complexité spatiale

#### Algorithmes itératifs
Variables scalaires : O(1)
Tableaux/structures alloués : taille allouée

```python
def algo_iter(n):
    a = 0                    # O(1)
    tab = [0] * n            # O(n)
    mat = [[0]*n for _ in range(n)]  # O(n²)
    return sum(tab)
# Espace auxiliaire : O(n²)
```

#### Algorithmes récursifs
Espace = **Profondeur maximale de récursion × Espace par cadre de pile**

```python
def fact(n):
    if n <= 1: return 1
    return n * fact(n-1)
# Profondeur = n, chaque cadre O(1) → Espace = Θ(n)

def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])      # Copie : O(n/2)
    right = merge_sort(arr[mid:])     # Copie : O(n/2)
    return merge(left, right)         # O(n) temporaire
# Profondeur = log n, mais copies à chaque niveau → Espace = O(n log n) naïf
# Optimisé (indices) : O(n) pour tableau temporaire + O(log n) pile = O(n)
```

### 5.2.3 Compromis Temps-Espace (Time-Space Tradeoffs)

| Technique | Gain temps | Coût espace | Exemple |
|-----------|------------|-------------|---------|
| **Mémoïsation** | Évite recalculs | Table O(n) ou O(n²) | Fibonacci, LCS |
| **Tabulation** | Itératif, pas pile | Table O(n) ou O(n²) | Sac à dos, Floyd-Warshall |
| **Précalcul** | Réponse O(1) | Table de lookup | Tables de hachage parfait, précalcul factoriels |
| **Compression** | Moins d'E/S | CPU décompression | BWT, LZ77 |
| **Streaming** | Espace constant | Un seul passage | Algorithmes de flux (reservoir sampling) |

**Exemple classique - Fibonacci :**
| Méthode | Temps | Espace |
|---------|-------|--------|
| Récursif naïf | Θ(φⁿ) | Θ(n) pile |
| Récursif + mémoïsation | Θ(n) | Θ(n) table + Θ(n) pile |
| Itératif (2 variables) | Θ(n) | **Θ(1)** |
| Formule de Binet | Θ(log n)* | Θ(1) |
| Exponentiation matrice | Θ(log n) | Θ(1) |

*Précision flottante limitée.*

### 5.2.4 Complexité spatiale des algorithmes classiques

| Algorithme | Espace auxiliaire | Notes |
|------------|-------------------|-------|
| Tri fusion | Θ(n) | Tableau temporaire pour merge |
| Tri rapide (QuickSort) | Θ(log n) moy., Θ(n) pire | Pile de récursion (optimisable queue) |
| Tri par tas | Θ(1) | En place |
| BFS | Θ(V) | File + tableau visité |
| DFS | Θ(V) | Pile (explicite ou récursion) |
| Dijkstra (tas) | Θ(V) | Tas + distances + précédents |
| Floyd-Warshall | Θ(V²) | Matrice distances |
| Programmation dynamique 1D | Θ(n) ou Θ(W) | Table 1D |
| Programmation dynamique 2D | Θ(n²) ou Θ(nW) | Table 2D (optimisable si dépendances locales) |

---

## 5.3 Exercices Résolus

### Exercice 5.1 : Espace récursif vs itératif
**Énoncé :** Comparez l'espace auxiliaire de ces deux versions de factorielle :

```python
# Version A
def fact_rec(n):
    if n <= 1: return 1
    return n * fact_rec(n-1)

# Version B
def fact_iter(n):
    result = 1
    for i in range(2, n+1):
        result *= i
    return result
```

**Solution :**
- Version A : Profondeur n, chaque cadre stocke n et adresse retour → **Θ(n)**
- Version B : Variable `result` + boucle `i` → **Θ(1)**

### Exercice 5.2 : Tri fusion en place ?
**Énoncé :** Peut-on faire un tri fusion en Θ(1) espace auxiliaire ?

**Solution :** Tri fusion **standard** nécessite Θ(n) pour le merge.
Existe des variantes **in-place merge sort** (ex: Huang & Langston, 1988; Geffert et al.) mais très complexes, constantes élevées, pas utilisées en pratique.
Tri par tas (Heapsort) = Θ(n log n) temps, **Θ(1) espace** - alternative pratique.

### Exercice 5.3 : Sac à dos - Optimisation espace
**Énoncé :** Le sac à dos 0/1 standard utilise table 2D O(nW). Comment réduire à O(W) ?

**Solution :**
```python
# Version 2D
dp = [[0]*(W+1) for _ in range(n+1)]
for i in range(1, n+1):
    for w in range(W+1):
        if w_i <= w:
            dp[i][w] = max(dp[i-1][w], v_i + dp[i-1][w-w_i])
        else:
            dp[i][w] = dp[i-1][w]

# Version 1D (parcours poids DÉCROISSANT !)
dp = [0]*(W+1)
for i in range(n):
    for w in range(W, w_i-1, -1):  # Décroissant crucial !
        dp[w] = max(dp[w], v_i + dp[w-w_i])
```
**Pourquoi décroissant ?** Pour ne pas utiliser dp[w-w_i] déjà mis à jour pour l'objet i (ce qui autoriserait répétition).

---

## 5.4 Questions Théoriques avec Réponses Modèles

### Q5.1 : Quelle est la complexité spatiale de la recherche dichotomique récursive vs itérative ?
**Réponse :**
- Récursive : Θ(log n) (pile d'appel, profondeur log n)
- Itérative : Θ(1) (variables low, high, mid)

### Q5.2 : Expliquez pourquoi la tabulation bottom-up utilise généralement moins d'espace que la mémoïsation top-down pour le même problème de PD.
**Réponse :** Mémoïsation : table + pile d'appel (profondeur récursion). Tabulation : table seulement (itératif). De plus, tabulation permet souvent d'éliminer des dimensions de la table si les dépendances sont locales (ex: sac à dos 1D vs 2D).

### Q5.3 : Donnez un exemple où l'on accepte une complexité temporelle plus élevée pour réduire l'espace.
**Réponse :** Algorithmes de **flux (streaming)** : un seul passage sur les données, espace O(1) ou O(log n), mais temps parfois plus élevé ou résultats approximatifs (ex: comptage distincts avec HyperLogLog). Aussi : recomputation à la demande (lazy evaluation) au lieu de stocker.

### Q5.4 : La complexité spatiale de BFS est-elle toujours Θ(V) ?
**Réponse :** Oui dans le cas général (file + ensemble visité). Mais si le graphe est un arbre et qu'on n'a pas besoin de l'ensemble visité (pas de cycles), file seule = O(largeur max) ≤ O(V). Pour arbre binaire complet, largeur = Θ(V) au dernier niveau.

---

# CHAPITRE 6 : COMPLEXITÉ ET PREUVE DE CORRECTION <a name="chapitre-6"></a>

## 6.1 Objectifs Pédagogiques
- Comprendre les classes de complexité P, NP, NP-complet, NP-difficile
- Maîtriser les techniques de preuve de correction : induction, invariants de boucle, contradiction
- Savoir prouver la correction d'algorithmes itératifs et récursifs

## 6.2 Contenu Théorique Détaillé

### 6.2.1 Classes de complexité : P, NP, NP-complet

**Modèle de décision :** Problème de décision = réponse OUI/NON.

**P (Polynomial time) :** Ensemble des problèmes de décision résolubles en temps polynomial par une machine de Turing déterministe.
- Exemples : Tri, recherche dichotomique, plus court chemin (Dijkstra), flux max, test primalité (AKS)

**NP (Nondeterministic Polynomial time) :** Ensemble des problèmes de décision où une solution candidate peut être **vérifiée** en temps polynomial.
- Équivalent : Résoluble en temps polynomial par machine de Turing non-déterministe
- Exemples : SAT, 3-SAT, CLIQUE, COULEURAGE, SAC À DOS (décision), TSP (décision), HAMILTONIEN

**Relation :** P ⊆ NP (problème ouvert : P = NP ?)

**NP-complet (NPC) :**
Un problème L est NP-complet si :
1. L ∈ NP
2. ∀ L' ∈ NP, L' ≤ₚ L (réductible en temps polynomial)

**Théorème de Cook-Levin (1971) :** SAT est NP-complet (premier problème NPC).
**Méthode de preuve NPC :** Réduction depuis un problème NPC connu.

**Problèmes NPC classiques :**
- SAT, 3-SAT
- CLIQUE, COUVERTURE DE SOMMETS (VERTEX COVER)
- COULEURAGE 3-COLORABLE
- SAC À DOS (décision)
- TSP (décision)
- HAMILTONIEN
- PARTITION, SOUS-ENSEMBLE SUM

**NP-difficile (NP-hard) :** Au moins aussi difficile que les problèmes NP (pas nécessairement dans NP).
Ex: Version optimisation de TSP, SAC À DOS (optimisation).

### 6.2.2 Preuve par Induction

**Principe :** Pour prouver P(n) ∀ n ∈ ℕ :
1. **Base** : P(0) ou P(1) vrai
2. **Hérédité** : P(k) ⇒ P(k+1) ∀ k ≥ base

**Induction forte :** Hypothèse : P(0) ∧ P(1) ∧ ... ∧ P(k) ⇒ P(k+1)

**Application aux algorithmes récursifs :**
- P(n) = "L'algorithme termine et produit le bon résultat pour entrée de taille n"
- Base : cas de base (n=0, n=1)
- Hérédité : supposer correct pour tailles < n, prouver pour n

**Exemple - Correction Factorielle :**
```python
def fact(n):
    if n <= 1: return 1      # Base : fact(0)=1, fact(1)=1 ✓
    return n * fact(n-1)     # Hérédité : si fact(n-1)=(n-1)! alors fact(n)=n·(n-1)!=n! ✓
```

### 6.2.3 Invariants de Boucle (Loop Invariants)

**Méthode standard (Hoare) pour prouver correction d'une boucle :**
Soit `while condition: corps` avec invariant I.

1. **Initialisation** : I vrai avant la première itération
2. **Maintenance** : Si I vrai avant itération et condition vraie, alors I vrai après itération
3. **Terminaison** : La boucle termine (variant de boucle strictement décrémenté et borné)
4. **Post-condition** : I ∧ ¬condition ⇒ propriété désirée

**Exemple - Recherche linéaire :**
```python
def linear_search(arr, x):
    i = 0
    while i < len(arr) and arr[i] != x:
        i += 1
    return i < len(arr)
```
**Invariant I(i) :** "x n'apparaît pas dans arr[0..i-1]" (tous éléments avant i sont ≠ x)

- **Init** : i=0, arr[0..-1] vide → I vrai ✓
- **Maintien** : Si I(i) vrai et arr[i] ≠ x, alors I(i+1) vrai (x pas dans arr[0..i]) ✓
- **Terminaison** : i augmente, borné par len(arr) → termine
- **Post** : I(i) ∧ (i ≥ len(arr) ∨ arr[i]=x)
  - Si i < len(arr) : arr[i]=x et x pas avant → premier x trouvé ✓
  - Si i = len(arr) : x pas dans arr[0..len-1] → x absent ✓

### 6.2.4 Preuve par Contradiction

**Principe :** Supposer la négation de la thèse, déduire une contradiction.

**Exemple - Correction de Dijkstra :**
Thèse : Quand u est extrait de la file, d[u] = δ(s, u).
Supposer ∃ premier u extrait tel que d[u] > δ(s, u).
Soit y le premier sommet sur le chemin optimal s⇝u qui n'est pas encore extrait, x son prédécesseur (x extrait avant u).
Au moment de l'extraction de x, relaxation de (x,y) a lieu : d[y] ≤ d[x] + w(x,y) = δ(s,x) + w(x,y) = δ(s,y).
Puisque d[u] ≤ d[y] (u extrait avant y) et d[y] = δ(s,y) ≤ δ(s,u), on a d[u] ≤ δ(s,u).
Contradiction avec d[u] > δ(s,u). ✓

---

## 6.3 Exercices Résolus

### Exercice 6.1 : Preuve par induction - Tri par insertion
**Énoncé :** Prouvez par induction que le tri par insertion trie correctement.

**Solution :**
Algorithme :
```python
for i in range(1, n):
    key = arr[i]
    j = i - 1
    while j >= 0 and arr[j] > key:
        arr[j+1] = arr[j]
        j -= 1
    arr[j+1] = key
```

**Invariant de boucle externe I(i) :** "Sous-tableau arr[0..i-1] est trié et contient les mêmes éléments qu'initialement."

- **Base (i=1)** : arr[0..0] = 1 élément → trié ✓
- **Hérédité** : Supposons I(i) vrai. L'itération i insère arr[i] (valeur `key`) dans la bonne position dans arr[0..i-1] trié (boucle interne décale les éléments > key). Résultat : arr[0..i] trié, mêmes éléments → I(i+1) vrai ✓
- **Terminaison** : i va de 1 à n-1 → termine
- **Post-condition** : i = n, I(n) : arr[0..n-1] trié, permutation de l'original ✓

### Exercice 6.2 : Réduction NPC - 3-SAT vers CLIQUE
**Énoncé :** Montrez que 3-SAT ≤ₚ CLIQUE.

**Solution :**
Instance 3-SAT : Clauses C₁, C₂, ..., Cₖ, chaque clause = 3 littéraux.
Construction graphe G :
- Sommets : Un sommet par littéral dans chaque clause → 3k sommets
- Arêtes : Entre deux sommets de **clauses différentes** si les littéraux ne sont **pas contradictoires** (ex: x et ¬x contradictoires)

**Revendication :** 3-SAT satisfiable ⇔ G a une k-clique.

⇒ Si φ satisfiable, prendre un littéral vrai par clause. Ces k littéraux sont deux à deux non contradictoires → forment une clique.
⇐ Si k-clique, elle a exactement un sommet par clause (pas d'arêtes intra-clauses). Assigner vrai aux littéraux de la clique (cohérents car non contradictoires) → toutes clauses satisfaites. ✓

Construction polynomial en taille de φ. Donc 3-SAT ≤ₚ CLIQUE.

### Exercice 6.3 : Invariant de boucle - Partition QuickSort
**Énoncé :** Prouvez la correction de la procédure de partition de QuickSort (Lomuto) :

```python
def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i + 1
```

**Solution :**
**Invariant I(j) au début de l'itération j :**
1. arr[low..i] ≤ pivot
2. arr[i+1..j-1] > pivot
3. arr[high] = pivot

- **Init (j=low)** : i = low-1. arr[low..low-1] vide (≤ pivot) ✓. arr[low..low-1] vide (> pivot) ✓. arr[high]=pivot ✓.
- **Maintien** : Cas `arr[j] ≤ pivot` : i++, swap arr[i]↔arr[j]. L'élément ≤ pivot déplacé dans zone 1, zone 2 inchangée ✓. Cas `arr[j] > pivot` : i inchangé, j++ implicitement. L'élément reste dans zone 2 ✓.
- **Terminaison** : j = high. I(high) : arr[low..i] ≤ pivot, arr[i+1..high-1] > pivot, arr[high]=pivot.
- **Post swap final** : swap arr[i+1] et arr[high]. arr[low..i] ≤ pivot, arr[i+1]=pivot, arr[i+2..high] > pivot. Retourne i+1 = position finale pivot ✓

---

## 6.4 Questions Théoriques avec Réponses Modèles

### Q6.1 : Quelle est la différence entre NP-complet et NP-difficile ?
**Réponse :** **NP-complet** = dans NP ∩ NP-difficile (problème de décision, vérifiable en temps polynomial, aussi difficile que tout NP). **NP-difficile** = au moins aussi difficile que les problèmes NP, mais pas nécessairement dans NP (peut être problème d'optimisation, non vérifiable en temps polynomial, indécidable même).

### Q6.2 : Donnez les 4 étapes de la preuve de correction par invariant de boucle.
**Réponse :**
1. **Initialisation** : L'invariant est vrai avant la première itération
2. **Maintenance** : Si l'invariant est vrai avant une itération et que la condition de boucle est vraie, il reste vrai après l'itération
3. **Terminaison** : La boucle termine (variant de boucle)
4. **Post-condition** : L'invariant conjoint avec la négation de la condition de boucle implique la propriété désirée

### Q6.3 : Montrez que si P = NP, alors tout problème dans P (sauf ∅ et Σ*) est NP-complet.
**Réponse :** Soit L ∈ P, L ≠ ∅, L ≠ Σ*. Comme P = NP, L ∈ NP. Pour tout L' ∈ NP, L' ∈ P (puisque P=NP). On peut réduire L' vers L en temps polynomial : calculer la réponse pour L' (en P), puis produire une instance fixe dans L (si réponse OUI) ou hors L (si NON). Donc L' ≤ₚ L, donc L est NP-complet.

### Q6.4 : Pourquoi la preuve de correction de Dijkstra utilise-t-elle la propriété "premier sommet extrait avec d[u] > δ(s,u)" ?
**Réponse :** C'est une preuve par contradiction minimisant le contre-exemple. En prenant le **premier** tel sommet u, on garantit que son prédécesseur x sur le chemin optimal a été correctement traité (d[x] = δ(s,x)), ce qui permet d'appliquer la relaxation et d'obtenir la contradiction. Si on prenait un u quelconque, x pourrait aussi être incorrect.

---

# CHAPITRE 7 : OPTIMISATION D'ALGORITHMES <a name="chapitre-7"></a>

## 7.1 Objectifs Pédagogiques
- Identifier les goulots d'étranglement par analyse de complexité
- Appliquer les techniques d'optimisation classiques
- Comprendre les limites de l'optimisation (compromis, lisibilité, maintenance)

## 7.2 Contenu Théorique Détaillé

### 7.2.1 Identification des points faibles

**Profilage (Profiling) :**
- **Complexité théorique** : Analyse asymptotique (big O)
- **Mesure empirique** : Temps réel, comptage opérations, cache misses, branches mal prédites
- **Outils** : perf, gprof, Valgrind/Callgrind, cProfile, line_profiler

**Loi d'Amdahl :** Speedup max = 1 / ((1 - p) + p/s) où p = fraction optimisable, s = speedup de la partie optimisée.
*Exemple :* Optimiser 90% du code 10× plus vite → speedup global = 1/(0.1 + 0.9/10) = 5.26× seulement.

**Goulots d'étranglement typiques :**
- Boucles imbriquées inutiles → réduire complexité algorithmique
- Allocations mémoire fréquentes → réutiliser buffers, pools
- Accès mémoire non-linéaires → améliorer localité (cache)
- Récursivité excessive → transformation itérative
- Calculs redondants → mémoïsation, précalcul

### 7.2.2 Techniques d'optimisation

#### 1. Simplification de boucles
```python
# Avant : O(n²)
for i in range(n):
    for j in range(n):
        if i == j:  # Rarement vrai
            faire_quelque_chose()

# Après : O(n)
for i in range(n):
    faire_quelque_chose()
```

**Déplacement d'invariants de boucle (Loop-Invariant Code Motion) :**
```python
# Avant
for i in range(n):
    x = calcul_couteux(y)  # Ne dépend pas de i
    traiter(x, i)

# Après
x = calcul_couteux(y)
for i in range(n):
    traiter(x, i)
```

**Fusion de boucles (Loop Fusion) :**
```python
# Avant : 2 passages
for i in range(n): a[i] = f(i)
for i in range(n): b[i] = g(a[i])

# Après : 1 passage, meilleure localité cache
for i in range(n):
    a[i] = f(i)
    b[i] = g(a[i])
```

#### 2. Réduction de la récursivité
**Élimination de la récursion terminale (Tail Call Optimization) :**
```python
# Récursif terminal
def fact_tail(n, acc=1):
    if n <= 1: return acc
    return fact_tail(n-1, n*acc)

# Itératif équivalent
def fact_iter(n):
    acc = 1
    while n > 1:
        acc *= n
        n -= 1
    return acc
```

**Transformation récursion → itération (pile explicite) :**
```python
# DFS récursif
def dfs_rec(u):
    visited.add(u)
    for v in adj[u]:
        if v not in visited:
            dfs_rec(v)

# DFS itératif
def dfs_iter(start):
    stack = [start]
    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            for v in adj[u]:
                stack.append(v)
```

#### 3. Optimisation d'accès mémoire (Localité)
- **Localité temporelle** : Réutiliser données récentes
- **Localité spatiale** : Accéder données contiguës

```python
# Mauvais : parcours colonnes (stride n)
for j in range(n):
    for i in range(n):
        sum += mat[i][j]

# Bon : parcours lignes (contigu)
for i in range(n):
    for j in range(n):
        sum += mat[i][j]
```

**Blocking / Tiling (pour matrices) :**
```python
# Multiplication matrices par blocs pour tenir dans cache L1
for ii in range(0, n, B):
    for jj in range(0, n, B):
        for kk in range(0, n, B):
            for i in range(ii, min(ii+B, n)):
                for j in range(jj, min(jj+B, n)):
                    for k in range(kk, min(kk+B, n)):
                        C[i][j] += A[i][k] * B[k][j]
```

#### 4. Programmation dynamique vs Glouton vs Diviser pour régner
| Problème | Approche optimale | Complexité |
|----------|------------------|------------|
| Tri | Diviser pour régner (fusion) / Glouton (tas) | Θ(n log n) |
| Plus court chemin (poids ≥ 0) | Glouton (Dijkstra) | Θ((V+E) log V) |
| Plus court chemin (poids quelconques) | PD (Bellman-Ford) | Θ(VE) |
| Sac à dos 0/1 | PD | Θ(nW) |
| Arbre couvrant min | Glouton (Kruskal/Prim) | Θ(E log V) |
| TSP métrique | Approximation gloutonne (Christofides) | 1.5-opt |

#### 5. Structures de données spécialisées
| Besoin | Structure | Opérations clés |
|--------|-----------|-----------------|
| Min/Max fréquent, insertion | Tas (Heap) | O(log n) insert, O(1) peek, O(log n) extract |
| Recherche, insertion, suppression, ordre | Arbre équilibré (AVL, Rouge-Noir) | O(log n) tout |
| Union-Find (composantes connexes) | Disjoint Set Union + compression chemin | O(α(n)) ≈ O(1) |
| Fréquences, top-k | Tas + table de hachage / Count-Min Sketch | O(1) amorti |
| Recherche préfixes | Trie (Arbre de préfixes) | O(longueur) |
| Intervalles | Arbre d'intervalles / Segment Tree | O(log n) |

### 7.2.3 Limites de l'optimisation

**Règle des 90/10 :** 90% du temps d'exécution dans 10% du code.
**Optimisation prématurée :** "Root of all evil" (Knuth). D'abord code correct, clair, maintenable. Optimiser *après* profilage.
**Compromis :**
- Temps vs Espace
- Temps vs Lisibilité/Maintenabilité
- Optimalité vs Simplicité (approximation)
- Généricité vs Spécialisation

---

## 7.3 Exercices Résolus

### Exercice 7.1 : Optimisation de boucle - Calcul de polynôme
**Énoncé :** Optimisez l'évaluation de P(x) = a₀ + a₁x + a₂x² + ... + aₙxⁿ

**Solution :**
**Naïf (O(n²) multiplications) :**
```python
def poly_naif(a, x):
    result = 0
    for i in range(len(a)):
        term = a[i]
        for _ in range(i):  # x^i
            term *= x
        result += term
    return result
```

**Méthode de Horner (O(n)) :**
```python
def poly_horner(a, x):
    result = 0
    for coeff in reversed(a):
        result = result * x + coeff
    return result
```
*Factorisation : ((...((aₙ)x + aₙ₋₁)x + ...)x + a₀)*

### Exercice 7.2 : Optimisation mémoire - Suite de Fibonacci
**Énoncé :** Donnez 4 implementations de Fibonacci avec complexités temps/espace différentes.

**Solution :**
| Version | Temps | Espace | Notes |
|---------|-------|--------|-------|
| Récursif naïf | Θ(φⁿ) | Θ(n) pile | Exponentiel - inutilisable n>40 |
| Récursif + mémoïsation | Θ(n) | Θ(n) table + pile | Top-down PD |
| Itératif (2 vars) | Θ(n) | **Θ(1)** | Optimal espace |
| Matriciel / Doubling | Θ(log n) | Θ(1) | Exponentiation rapide |

**Méthode matricielle :**
```
[Fₙ₊₁  Fₙ  ] = [1 1]ⁿ
[Fₙ    Fₙ₋₁]   [1 0]
```
Exponentiation par carrés → O(log n) multiplications matricielles 2×2.

### Exercice 7.3 : Optimisation algorithme - Recherche du majority element
**Énoncé :** Trouver l'élément apparaissant > n/2 fois dans un tableau (s'il existe). Algorithme O(n) temps, O(1) espace.

**Solution : Algorithme de Boyer-Moore (Majority Vote)**
```python
def majority_element(arr):
    candidate = None
    count = 0
    for x in arr:
        if count == 0:
            candidate, count = x, 1
        elif x == candidate:
            count += 1
        else:
            count -= 1
    # Vérification (optionnelle si existence garantie)
    if arr.count(candidate) > len(arr) // 2:
        return candidate
    return None
```
**Preuve d'optimalité :** Chaque paire (candidate, autre) s'annule. Si majorité existe, elle survit. Temps Θ(n), Espace Θ(1).

---

## 7.4 Questions Théoriques avec Réponses Modèles

### Q7.1 : Expliquez la méthode de Horner pour l'évaluation de polynômes. Pourquoi est-elle optimale en nombre de multiplications ?
**Réponse :** P(x) = a₀ + x(a₁ + x(a₂ + ... + x(aₙ₋₁ + xaₙ)...)). n multiplications, n additions. Optimal car tout polynôme de degré n nécessite au moins n multiplications (sinon on obtiendrait un polynôme de degré < n).

### Q7.2 : Quand l'élimination de récursion terminale (TCO) est-elle applicable ? Donnez un exemple où elle ne l'est pas.
**Réponse :** TCO applicable si l'appel récursif est la **dernière opération** de la fonction (pas de calcul après le retour).
Exemple **sans TCO** :
```python
def fact(n):
    if n <= 1: return 1
    return n * fact(n-1)  # Multiplication APRÈS l'appel récursif
```
Ici il faut garder la pile pour multiplier au retour.

### Q7.3 : Quelle est l'idée du "Loop Unrolling" (déroulage de boucle) ? Quel en est l'inconvénient principal ?
**Réponse :** Répliquer le corps de la boucle k fois, itérer n/k fois. Réduit overhead de boucle (tests, incréments), permet vectorisation SIMD, pipeline CPU.
Inconvénient : **Gonflement du code** (code bloat) → peut dégrader performance si ne tient plus dans cache d'instructions (L1I).

### Q7.4 : Expliquez la loi d'Amdahl. Si on optimise 80% d'un programme pour le rendre 5 fois plus rapide, quel est le speedup global maximum ?
**Réponse :** Speedup = 1 / ((1-p) + p/s) = 1 / (0.2 + 0.8/5) = 1 / (0.2 + 0.16) = 1/0.36 ≈ **2.78×**. Même avec optimisation massive d'une partie, la partie non optimisée limite le gain global.

---

# ANNEXES

## Annexe A : Résumé des notations asymptotiques

| Notation | Définition | Signification |
|----------|------------|---------------|
| f = O(g) | ∃c,n₀>0 : ∀n≥n₀, f(n) ≤ c·g(n) | f majoré par g (pire cas) |
| f = Ω(g) | ∃c,n₀>0 : ∀n≥n₀, f(n) ≥ c·g(n) | f minoré par g (meilleur cas) |
| f = Θ(g) | ∃c₁,c₂,n₀>0 : ∀n≥n₀, c₁g(n) ≤ f(n) ≤ c₂g(n) | f encadré par g (cas serré) |
| f = o(g) | ∀c>0, ∃n₀ : ∀n≥n₀, f(n) < c·g(n) | f strictement plus petit que g |
| f = ω(g) | ∀c>0, ∃n₀ : ∀n≥n₀, f(n) > c·g(n) | f strictement plus grand que g |

## Annexe B : Théorème Maître (Master Theorem)

Pour T(n) = aT(n/b) + f(n) avec a ≥ 1, b > 1, f(n) > 0 :

Soit c = log_b(a).

1. **Cas 1** : Si f(n) = O(n^{c-ε}) pour ε>0 → T(n) = Θ(n^c)
2. **Cas 2** : Si f(n) = Θ(n^c log^k n) pour k ≥ 0 → T(n) = Θ(n^c log^{k+1} n)
3. **Cas 3** : Si f(n) = Ω(n^{c+ε}) pour ε>0 ET a·f(n/b) ≤ k·f(n) pour k<1 (régularité) → T(n) = Θ(f(n))

## Annexe C : Complexités des algorithmes de tri

| Algorithme | Meilleur | Moyen | Pire | Espace | Stable |
|------------|----------|-------|------|--------|--------|
| Tri bulle | Θ(n) | Θ(n²) | Θ(n²) | O(1) | Oui |
| Tri insertion | Θ(n) | Θ(n²) | Θ(n²) | O(1) | Oui |
| Tri sélection | Θ(n²) | Θ(n²) | Θ(n²) | O(1) | Non |
| Tri fusion | Θ(n log n) | Θ(n log n) | Θ(n log n) | O(n) | Oui |
| Tri rapide | Θ(n log n) | Θ(n log n) | Θ(n²) | O(log n) | Non |
| Tri par tas | Θ(n log n) | Θ(n log n) | Θ(n log n) | O(1) | Non |
| Tri comptage | Θ(n+k) | Θ(n+k) | Θ(n+k) | O(k) | Oui |
| Tri par base | Θ(d(n+k)) | Θ(d(n+k)) | Θ(d(n+k)) | O(n+k) | Oui |

## Annexe D : Références Bibliographiques Complètes

1. **Cormen, T.H., Leiserson, C.E., Rivest, R.L., Stein, C.** (2009). *Introduction to Algorithms*, 3rd ed. MIT Press. [Référence de base]
2. **Kleinberg, J., Tardos, É.** (2005). *Algorithm Design*. Pearson. [Approche par paradigmes]
3. **Sedgewick, R., Wayne, K.** (2011). *Algorithms*, 4th ed. Addison-Wesley. [Implémentations Java, visualisations]
4. **Aho, A.V., Hopcroft, J.E., Ullman, J.D.** (1983). *Data Structures and Algorithms*. Addison-Wesley. [Classique théorique]
5. **Knuth, D.E.** (1998). *The Art of Computer Programming*, Vol. 1-4. Addison-Wesley. [Encyclopédie]
6. **Dasgupta, S., Papadimitriou, C.H., Vazirani, U.V.** (2006). *Algorithms*. McGraw-Hill. [Approche mathématique]
7. **Even, S.** (2011). *Graph Algorithms*, 2nd ed. Cambridge University Press. [Spécialisé graphes]
8. **Vazirani, V.V.** (2001). *Approximation Algorithms*. Springer. [Algorithmes d'approximation]

---

# INDEX DES EXERCICES PAR CHAPITRE

| Chapitre | Exercices Résolus | Questions Théoriques |
|----------|-------------------|---------------------|
| 1 | 1.1, 1.2 | Q1.1 - Q1.4 |
| 2 | 2.1, 2.2, 2.3, 2.4 | Q2.1 - Q2.4 |
| 3 | 3.1, 3.2, 3.3 | Q3.1 - Q3.4 |
| 4 | 4.1, 4.2, 4.3, 4.4 | Q4.1 - Q4.4 |
| 5 | 5.1, 5.2, 5.3 | Q5.1 - Q5.4 |
| 6 | 6.1, 6.2, 6.3 | Q6.1 - Q6.4 |
| 7 | 7.1, 7.2, 7.3 | Q7.1 - Q7.4 |

**Total : 21 exercices résolus détaillés + 28 questions théoriques avec réponses modèles**

---

*Document préparé pour le cours "Conception et Analyse d'Algorithmes" - 21h*  
*Version 1.0 - Basé sur les références académiques standards (CLRS, Kleinberg & Tardos, Sedgewick & Wayne)*