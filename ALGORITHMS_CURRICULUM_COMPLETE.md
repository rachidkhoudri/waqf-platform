# DESIGN AND ANALYSIS OF ALGORITHMS
## Comprehensive Academic Curriculum for University-Level Students

**Course Level:** Graduate / Senior Undergraduate  
**Duration:** 21 Hours  
**Prerequisites:** Basic Algorithms, Advanced Data Structures, Programming Proficiency  
**Primary References:**
- Cormen, Leiserson, Rivest, Stein — *Introduction to Algorithms* (CLRS), 3rd ed., MIT Press
- Kleinberg, Tardos — *Algorithm Design*, Pearson
- Sedgewick, Wayne — *Algorithms*, 4th ed., Addison-Wesley
- Aho, Hopcroft, Ullman — *Data Structures and Algorithms*, Addison-Wesley

---

## TABLE OF CONTENTS

| Module | Topic | Hours |
|--------|-------|-------|
| 1 | Introduction to Algorithmic Complexity & Preliminary Notions | 3h |
| 2 | Analysis of Time Complexity | 3h |
| 3 | Data Structures and Complexity | 3h |
| 4 | Complexity Analysis Techniques: Divide & Conquer, Dynamic Programming, Greedy | 4h |
| 5 | Space Complexity | 2h |
| 6 | Complexity & Proof of Correctness | 3h |
| 7 | Algorithm Optimization | 3h |
| **Total** | | **21h** |

---

# MODULE 1: INTRODUCTION TO ALGORITHMIC COMPLEXITY & PRELIMINARY NOTIONS

## 1.1 Detailed Lecture Notes

### 1.1.1 Formal Definition of an Algorithm

**Definition (Knuth, 1973):** An algorithm is a finite sequence of unambiguous, mechanically executable instructions that, given an input instance from a problem domain, produces the corresponding output and terminates after a finite number of steps.

**Five Essential Properties (Knuth):**
1. **Finiteness:** The algorithm terminates after a finite number of steps
2. **Definiteness:** Each instruction is precisely and unambiguously specified
3. **Input:** Zero or more quantities are given initially
4. **Output:** One or more quantities are produced, related to inputs
5. **Effectiveness:** Each instruction is sufficiently basic to be executed by a human using pencil and paper

### 1.1.2 Algorithmic Problems and Resolution

**Algorithmic Problem:** A relation between a set of inputs (instances) and a set of valid outputs.

**Example — Sorting Problem:**
- Input: Sequence of n numbers ⟨a₁, a₂, ..., aₙ⟩
- Output: Permutation ⟨a'₁, a'₂, ..., a'ₙ⟩ such that a'₁ ≤ a'₂ ≤ ... ≤ a'ₙ

**Resolution:** The process of deriving a correct and efficient algorithm from a problem specification.

### 1.1.3 Motivation for Complexity Analysis

**Comparing Algorithms for the Same Problem:**

| Algorithm | 1,000 Elements | 1,000,000 Elements |
|-----------|---------------|-------------------|
| Insertion Sort O(n²) | ~0.001 s | ~1,000 s (16 min) |
| Merge Sort O(n log n) | ~0.0001 s | ~0.2 s |

**Purpose of Complexity Analysis:**
- Predict behavior on large inputs
- Compare algorithms independently of hardware
- Identify bottlenecks
- Guide efficient algorithm design

### 1.1.4 Fundamental Concepts and Types of Complexity

**Computational Model: RAM (Random Access Machine)**
- Memory: Sequence of addressable cells
- Basic operations: +, -, ×, /, comparisons, assignments, memory access → unit cost
- Instructions execute sequentially

**Time Complexity:** Number of elementary operations as a function of input size n
**Space Complexity:** Amount of memory used as a function of n

---

## 1.2 Solved Practical Exercises

### Exercise 1.1: Algorithm Identification

**Problem:** Determine which descriptions constitute formal algorithms.

a) "To bake a cake, mix ingredients, put in oven, wait until done."
b) "To find maximum in array: initialize max with first element, then for each subsequent element, if greater than max, update max."
c) "Solve x² + 1 = 0 in ℝ."

**Solution:**
- a) **No:** Ambiguous instructions ("mix", "wait until done"), no precise termination condition
- b) **Yes:** Finite, definite, defined I/O, effective
- c) **No:** No solution in ℝ; algorithm would not terminate or would fail

### Exercise 1.2: RAM Model Operation Costs

**Problem:** Give time cost in terms of n for each fragment:

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

**Solution:**
- **A:** n iterations × O(1) = **O(n)**
- **B:** n × n iterations × O(1) = **O(n²)**
- **C:** Repeated halving → ⌊log₂ n⌋ + 1 iterations = **O(log n)**

---

## 1.3 Theoretical Assessment Questions

### Q1.1
Formally define an algorithm and state Knuth's five characteristics.

### Q1.2
What is the difference between a problem and an instance of a problem?

### Q1.3
Why is asymptotic complexity more relevant than actual running time for comparing algorithms?

### Q1.4
In the RAM model, what is the cost of accessing array element A[i]?

---

## 1.4 Model Answers

### A1.1
An algorithm is a finite sequence of unambiguous, mechanically executable instructions... (see Section 1.1.1). Five characteristics: Finiteness, Definiteness, Input, Output, Effectiveness.

### A1.2
A **problem** is the general I/O relation (e.g., "sorting"). An **instance** is a concrete input (e.g., array [5, 2, 8, 1]).

### A1.3
Actual time depends on hardware, language, compiler, system load. Asymptotic complexity captures intrinsic behavior for large n, independent of these factors.

### A1.4
O(1) — unit cost, as memory is directly addressable.

---

# MODULE 2: ANALYSIS OF TIME COMPLEXITY

## 2.1 Detailed Lecture Notes

### 2.1.1 Asymptotic Notations (Landau Symbols)

Let f(n), g(n): ℕ → ℝ⁺.

**Big-O (Upper Bound):**
f(n) = O(g(n)) ⇔ ∃ c > 0, n₀ ≥ 0: ∀ n ≥ n₀, 0 ≤ f(n) ≤ c·g(n)

**Big-Omega (Lower Bound):**
f(n) = Ω(g(n)) ⇔ ∃ c > 0, n₀ ≥ 0: ∀ n ≥ n₀, 0 ≤ c·g(n) ≤ f(n)

**Big-Theta (Tight Bound):**
f(n) = Θ(g(n)) ⇔ ∃ c₁, c₂ > 0, n₀ ≥ 0: ∀ n ≥ n₀, 0 ≤ c₁·g(n) ≤ f(n) ≤ c₂·g(n)

**Interpretation:**
- f = O(g): "f grows no faster than g"
- f = Ω(g): "f grows at least as fast as g"
- f = Θ(g): "f grows at the same rate as g"

**Properties:**
- Transitivity: f = O(g) ∧ g = O(h) ⇒ f = O(h)
- Reflexivity: f = O(f), f = Θ(f)
- Symmetry: f = Θ(g) ⇔ g = Θ(f)
- Transposition: f = O(g) ⇔ g = Ω(f)

### 2.1.2 Complexity Calculation Methodology

**Elementary Operations (Unit Cost in RAM):**
- Arithmetic: +, -, ×, /, %
- Comparisons: <, >, ≤, ≥, ==, !=
- Assignments: x = expr
- Memory access: array[i], object.field
- Function calls (excluding body)

**Loop Analysis:**

*Simple Loop:*
```python
for i in range(n):        # n iterations
    O(1) operation
# Complexity: n × O(1) = O(n)
```

*Nested Loops:*
```python
for i in range(n):        # n iterations
    for j in range(m):    # m iterations
        O(1)
# Complexity: O(n×m), if m=n then O(n²)
```

*Geometric Loop:*
```python
i = 1
while i < n:              # log₂ n iterations
    i = i * 2
# Complexity: O(log n)
```

**Recursive Function Analysis:**

*Factorial:*
T(n) = T(n-1) + O(1), T(1) = O(1) → **O(n)**

*Merge Sort:*
T(n) = 2T(n/2) + O(n) → **Θ(n log n)** (Master Theorem)

### 2.1.3 Best, Worst, and Average Case

| Algorithm | Best | Worst | Average |
|-----------|------|-------|---------|
| Linear Search | Θ(1) | Θ(n) | Θ(n) |
| Insertion Sort | Θ(n) | Θ(n²) | Θ(n²) |
| Merge Sort | Θ(n log n) | Θ(n log n) | Θ(n log n) |
| QuickSort | Θ(n log n) | Θ(n²) | Θ(n log n) |
| Binary Search | Θ(1) | Θ(log n) | Θ(log n) |

### 2.1.4 Common Complexity Classes

| Notation | Name | Examples |
|----------|------|----------|
| O(1) | Constant | Array access, stack push/pop |
| O(log n) | Logarithmic | Binary search, heap ops |
| O(√n) | Square Root | Naive primality test |
| O(n) | Linear | Array traversal, linear search |
| O(n log n) | Linearithmic | Merge sort, heap sort |
| O(n²) | Quadratic | Bubble sort, nested loops |
| O(n³) | Cubic | Naive matrix multiply |
| O(2ⁿ) | Exponential | TSP brute force, subsets |
| O(n!) | Factorial | Permutations, exact TSP |

**Hierarchy:** O(1) ⊂ O(log n) ⊂ O(√n) ⊂ O(n) ⊂ O(n log n) ⊂ O(n²) ⊂ O(n³) ⊂ O(2ⁿ) ⊂ O(n!)

---

## 2.2 Solved Practical Exercises

### Exercise 2.1: Asymptotic Ordering

**Problem:** Order by asymptotic growth: n², 2ⁿ, n log n, n³, log n, n, 1, n!, √n, n^log n

**Solution:**
1. 1 = Θ(1)
2. log n = Θ(log n)
3. √n = Θ(n⁰·⁵)
4. n = Θ(n)
5. n log n = Θ(n log n)
6. n² = Θ(n²)
7. n³ = Θ(n³)
8. n^log n = Θ(n^log n) [faster than any polynomial]
9. 2ⁿ = Θ(2ⁿ)
10. n! = Θ(n!) [Stirling: n! ~ √(2πn)(n/e)ⁿ]

### Exercise 2.2: Complex Loop Analysis

**Problem:** Find exact Θ complexity:

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

**Solution:**
- **A:** Σᵢ₌₀ⁿ⁻¹ (n - i) = n(n+1)/2 = **Θ(n²)**
- **B:** Outer: n iterations; Inner: log₂ n → **Θ(n log n)**
- **C:** Σᵢ₌₀ⁿ⁻¹ i² = (n-1)n(2n-1)/6 = **Θ(n³)**

### Exercise 2.3: Master Theorem Applications

**Problem:** Solve using Master Theorem T(n) = aT(n/b) + f(n):

a) T(n) = 4T(n/2) + n²
b) T(n) = 2T(n/2) + n³
c) T(n) = 3T(n/4) + n log n
d) T(n) = 7T(n/2) + n²

**Solution:**

Let c = log_b(a). Compare f(n) with n^c.

**a)** a=4, b=2 → log₂4 = 2. f(n) = n² = Θ(n² log⁰ n) → **Case 2, k=0** → **Θ(n² log n)**

**b)** a=2, b=2 → log₂2 = 1. f(n) = n³ = Ω(n¹⁺ε), ε=1. Regularity holds. → **Case 3** → **Θ(n³)**

**c)** a=3, b=4 → log₄3 ≈ 0.79. f(n) = n log n = Ω(n⁰·⁷⁹⁺ε) → **Case 3** → **Θ(n log n)**

**d)** a=7, b=2 → log₂7 ≈ 2.81. f(n) = n² = O(n²·⁸¹⁻ε) → **Case 1** → **Θ(n^log₂7) ≈ Θ(n²·⁸¹)**

### Exercise 2.4: Average Case — Linear Search

**Problem:** Array of n distinct elements, search for x known to be present. Average comparisons?

**Solution:**
P(x at position i) = 1/n. Comparisons = i.
Average = (1/n) Σᵢ₌₁ⁿ i = (n+1)/2 = **Θ(n)**

---

## 2.3 Theoretical Assessment Questions

### Q2.1
Prove that n² + 3n + 5 = Θ(n²).

### Q2.2
Is it true that f(n) = O(g(n)) implies g(n) = O(f(n))? Justify.

### Q2.3
Give the time complexity of:
```python
def algo(n):
    i = n
    while i > 0:
        j = i
        while j > 0:
            j = j - 1
        i = i // 2
```

### Q2.4
Why does insertion sort have Θ(n) best-case complexity?

---

## 2.4 Model Answers

### A2.1
Find c₁, c₂, n₀ > 0: c₁n² ≤ n² + 3n + 5 ≤ c₂n² for n ≥ n₀.
For n ≥ 5: n² ≤ n² + 3n + 5 ≤ n² + 3n² + 5n² = 9n².
Take c₁ = 1, c₂ = 9, n₀ = 5. ✓

### A2.2
**False.** Counterexample: f(n) = n, g(n) = n². n = O(n²) but n² ≠ O(n). O is not symmetric; Θ is.

### A2.3
Outer loop: log₂ n iterations (halving). At iteration k (i = n/2ᵏ), inner loop: n/2ᵏ iterations.
Total = Σₖ₌₀^{log n} n/2ᵏ = n × Σ(1/2ᵏ) < 2n = **Θ(n)**

### A2.4
Best case = already sorted. Inner loop (shifting) executes 0 times per iteration. Only n-1 comparisons from outer loop → Θ(n).

---

# MODULE 3: DATA STRUCTURES AND COMPLEXITY

## 3.1 Detailed Lecture Notes

### 3.1.1 Arrays (Vectors)

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Access A[i] | Θ(1) | Direct addressing |
| Search (unsorted) | Θ(n) | Linear |
| Search (sorted, binary) | Θ(log n) | Requires preprocessing |
| Insert at end | Θ(1)* | *Amortized if dynamic |
| Insert at front/middle | Θ(n) | Element shifting |
| Delete | Θ(n) | Element shifting |

### 3.1.2 Linked Lists

| Operation | Singly | Doubly |
|-----------|--------|--------|
| Access i-th | Θ(i) | Θ(min(i, n-i)) |
| Search | Θ(n) | Θ(n) |
| Insert at front | Θ(1) | Θ(1) |
| Insert at end | Θ(n)* | Θ(1)* |
| Insert after known node | Θ(1) | Θ(1) |
| Delete known node | Θ(n)** | Θ(1) |

*With tail pointer. **Requires predecessor.

### 3.1.3 Trees

**Binary Search Tree (Unbalanced):**
| Op | Average | Worst |
|----|---------|-------|
| Search | Θ(log n) | Θ(n) |
| Insert | Θ(log n) | Θ(n) |
| Delete | Θ(log n) | Θ(n) |

**Balanced Trees (AVL, Red-Black, B-Trees):**
All operations: **Θ(log n)** guaranteed (height = O(log n))

**Heaps (Binary Heap):**
| Operation | Complexity |
|-----------|------------|
| Build (heapify) | Θ(n) |
| Insert | Θ(log n) |
| Extract min/max | Θ(log n) |
| Peek | Θ(1) |
| Increase key | Θ(log n) |

### 3.1.4 Graphs

**Representations:**
- Adjacency Matrix: Space Θ(V²), edge test Θ(1), neighbor scan Θ(V)
- Adjacency Lists: Space Θ(V+E), edge test Θ(deg), neighbor scan Θ(deg)

**Classic Algorithms (Adjacency Lists):**

| Algorithm | Complexity |
|-----------|------------|
| BFS/DFS | Θ(V + E) |
| Dijkstra (binary heap) | Θ((V+E) log V) |
| Dijkstra (Fibonacci heap) | Θ(V log V + E) |
| Bellman-Ford | Θ(VE) |
| Floyd-Warshall | Θ(V³) |
| Kruskal (sort + UF) | Θ(E log E) |
| Prim (binary heap) | Θ((V+E) log V) |
| SCC (Kosaraju/Tarjan) | Θ(V+E) |

### 3.1.5 Hash Tables

| Operation | Average | Worst |
|-----------|---------|-------|
| Search | Θ(1) | Θ(n) |
| Insert | Θ(1) | Θ(n) |
| Delete | Θ(1) | Θ(n) |

*Assuming good hash function (uniform hashing assumption).*

---

## 3.2 Solved Practical Exercises

### Exercise 3.1: Data Structure Selection

**Problem:** Maintain integer set with: insert, delete, find-min, find-arbitrary. Choose optimal structure for each emphasis.

**Solution:**
- **Min-Heap:** Insert O(log n), Min O(1), Extract-min O(log n), but search O(n)
- **Balanced BST (AVL/Red-Black):** All operations O(log n) — **best general purpose**
- **Hash Table + Heap:** Search O(1), Min O(1), but synchronization overhead
- **Conclusion:** Balanced BST for general use; Heap if min frequent and search rare.

### Exercise 3.2: BFS Complexity — Dense vs Sparse

**Problem:** Dense: E = Θ(V²). Sparse: E = Θ(V). Compare BFS with both representations.

**Solution:**
| | Sparse (E=Θ(V)) | Dense (E=Θ(V²)) |
|---|-----------------|-----------------|
| Adj Lists | Θ(V + V) = Θ(V) | Θ(V + V²) = Θ(V²) |
| Matrix | Θ(V²) | Θ(V²) |

**Conclusion:** Adjacency lists for sparse; matrix acceptable for dense.

### Exercise 3.3: Heapify Linear Time Proof

**Problem:** Prove bottom-up heapify takes Θ(n), not Θ(n log n).

**Solution:**
Node at height h does at most h swaps.
Nodes at height h ≤ ⌈n/2^{h+1}⌉.
Total ≤ Σₕ₌₀^{⌊log n⌋} h × ⌈n/2^{h+1}⌉ ≤ n Σₕ₌₀^∞ h/2^{h+1} = n × 1 = O(n).
(Series Σ h/2^h = 2)
Thus **Θ(n)**.

---

## 3.3 Theoretical Assessment Questions

### Q3.1
Why does doubly-linked list allow O(1) deletion of known node while singly-linked requires O(n)?

### Q3.2
What is the complexity of finding k-th smallest in unbalanced BST? In AVL?

### Q3.3
When would a hash table be inappropriate?

### Q3.4
Why is Dijkstra with Fibonacci heap theoretically faster but rarely used in practice?

---

## 3.4 Model Answers

### A3.1
Doubly-linked node has pointer to predecessor, enabling direct relink. Singly-linked requires traversal from head to find predecessor.

### A3.2
Unbalanced BST: O(n) worst case (degenerate to list). AVL: O(log n) guaranteed (height O(log n)).

### A3.3
When order operations needed (min, max, successor, sorted traversal) — hash tables don't maintain order. Also bad hash function or collision attacks (DoS).

### A3.4
Fibonacci: O(V log V + E) vs Binary: O((V+E) log V). But huge constants, complex implementation, memory overhead. Binary heap (or pairing heap) faster in practice.

---

# MODULE 4: COMPLEXITY ANALYSIS TECHNIQUES

## 4.1 Detailed Lecture Notes

### 4.1.1 Divide and Conquer

**Strategy:**
1. **Divide:** Decompose into smaller subproblems of same type
2. **Conquer:** Recursively solve (base case = small enough)
3. **Combine:** Merge subproblem solutions

**Recurrence:** T(n) = aT(n/b) + f(n)

| Algorithm | Recurrence | Complexity |
|-----------|------------|------------|
| Merge Sort | T(n) = 2T(n/2) + Θ(n) | Θ(n log n) |
| Binary Search | T(n) = T(n/2) + Θ(1) | Θ(log n) |
| Strassen | T(n) = 7T(n/2) + Θ(n²) | Θ(n^log₂7) ≈ Θ(n^2.81) |
| Max Element | T(n) = 2T(n/2) + Θ(1) | Θ(n) |

**Merge Sort Analysis:**
```python
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])      # T(n/2)
    right = merge_sort(arr[mid:])     # T(n/2)
    return merge(left, right)         # Θ(n)
```
Recursion tree: height log₂ n, each level costs Θ(n) → **Θ(n log n)**

### 4.1.2 Dynamic Programming

**Two Essential Properties:**
1. **Optimal Substructure:** Optimal solution contains optimal subsolutions
2. **Overlapping Subproblems:** Same subproblems solved repeatedly (vs. D&C)

**Two Approaches:**
- **Memoization (Top-down):** Recursion + lookup table
- **Tabulation (Bottom-up):** Iterative table filling

**Example 1: 0/1 Knapsack**
n items, weight wᵢ, value vᵢ, capacity W. Maximize value.
```
OPT(i, w) = max value with first i items, capacity w
OPT(i, w) = 0                          if i=0 or w=0
OPT(i, w) = OPT(i-1, w)                if wᵢ > w
OPT(i, w) = max(OPT(i-1, w), 
                vᵢ + OPT(i-1, w-wᵢ))   otherwise
```
Complexity: **Θ(nW)** time, **Θ(nW)** space (or Θ(W) optimized)
*Note: Pseudo-polynomial (depends on W, not log W)*

**Example 2: Floyd-Warshall (All-Pairs Shortest Paths)**
```
dist[i][j]⁽ᵏ⁾ = min(dist[i][j]⁽ᵏ⁻¹⁾, dist[i][k]⁽ᵏ⁻¹⁾ + dist[k][j]⁽ᵏ⁻¹⁾)
```
k = allowed intermediate vertices {1..k}
Complexity: **Θ(V³)** time, **Θ(V²)** space

**Example 3: Longest Common Subsequence (LCS)**
```
LCS(X[1..i], Y[1..j]) = 
  0                              if i=0 or j=0
  1 + LCS(X[1..i-1], Y[1..j-1])  if X[i] = Y[j]
  max(LCS(X[1..i-1], Y[1..j]), 
      LCS(X[1..i], Y[1..j-1]))   otherwise
```
Complexity: **Θ(mn)** time and space

### 4.1.3 Greedy Algorithms

**Principle:** Build solution incrementally, making locally optimal choice at each step, hoping for global optimum.

**Two Properties for Optimality:**
1. **Greedy Choice Property:** Globally optimal solution can start with greedy choice
2. **Optimal Substructure:** Remaining subproblem after greedy choice has optimal solution

**Example 1: Dijkstra (Single-Source Shortest Paths, Non-negative Weights)**
- Greedy choice: Extract vertex with minimum distance
- Correctness: Induction + relaxation property
- Complexity: Array Θ(V²), Binary Heap Θ((V+E) log V), Fibonacci Θ(V log V + E)

**Example 2: Minimum Spanning Tree (Kruskal/Prim)**
- Kruskal: Sort edges, add if no cycle (Union-Find)
- Prim: Grow tree by minimum weight edge connecting tree to new vertex
- Proof: Cut property — minimum weight edge crossing any cut belongs to some MST

**Example 3: TSP Approximation (Metric TSP)**
- Double-tree / Christofides (3/2 ratio)
- General TSP: No polynomial approximation unless P=NP

**Example 4: Huffman Coding (Optimal Prefix Codes)**
- Greedy: Merge two lowest frequency symbols
- Optimality: Exchange argument — any optimal code can be transformed

---

## 4.2 Solved Practical Exercises

### Exercise 4.1: Divide & Conquer — Simultaneous Min/Max

**Problem:** Find min and max of n elements minimizing comparisons.

**Solution:**
```python
def min_max(arr):
    if len(arr) == 1: return (arr[0], arr[0])
    if len(arr) == 2: return (min(arr), max(arr))  # 1 comparison
    mid = len(arr) // 2
    min1, max1 = min_max(arr[:mid])
    min2, max2 = min_max(arr[mid:])
    return (min(min1, min2), max(max1, max2))  # 2 comparisons
```
Recurrence: T(n) = 2T(n/2) + 2, T(2) = 1
Solution: **3n/2 - 2 comparisons** (vs 2n-2 for separate search)

### Exercise 4.2: DP — Matrix Chain Multiplication

**Problem:** Chain A₁×A₂×...×Aₙ. Find parenthesization minimizing scalar multiplications.

**Solution:**
Dimensions: Aᵢ is pᵢ₋₁ × pᵢ
m[i][j] = min cost for Aᵢ...Aⱼ
```
m[i][i] = 0
m[i][j] = min_{i≤k<j} (m[i][k] + m[k+1][j] + pᵢ₋₁·pₖ·pⱼ)
```
Complexity: **Θ(n³)** time, Θ(n²) space.

### Exercise 4.3: Greedy — Coin Change

**Problem:** Coin system {1, 5, 10, 25}. Is greedy (largest coin first) optimal?

**Solution:** **Yes** for canonical system.
Proof: For any amount, # of 25¢ in optimal is maximal (else replace 5×5¢ with 25¢, etc.).
*Counterexample:* {1, 3, 4} for 6: greedy gives 4+1+1=3, optimal 3+3=2.

### Exercise 4.4: Dijkstra — Step-by-Step

**Problem:** Apply Dijkstra to: A→B(4), A→C(2), B→C(1), B→D(5), C→D(8), C→E(10), D→E(2), D→Z(6), E→Z(2). Source A.

**Solution:**
| Step | Extracted | Updated Distances |
|------|-----------|-------------------|
| Init | - | A=0, others=∞ |
| 1 | A(0) | B=4, C=2 |
| 2 | C(2) | B=min(4,2+1)=3, D=10, E=12 |
| 3 | B(3) | D=min(10,3+5)=8 |
| 4 | D(8) | E=min(12,8+2)=10, Z=14 |
| 5 | E(10) | Z=min(14,10+2)=12 |
| 6 | Z(12) | Done |

Path A→C→B→D→E→Z = 12

---

## 4.3 Theoretical Assessment Questions

### Q4.1
What is the fundamental difference between Divide & Conquer and Dynamic Programming?

### Q4.2
State the two properties for greedy optimality. Illustrate with Kruskal.

### Q4.3
Why is Knapsack DP pseudo-polynomial?

### Q4.4
Does Dijkstra work with negative edges? Why?

---

## 4.4 Model Answers

### A4.1
In **D&C**, subproblems are **disjoint** (e.g., merge sort). In **DP**, subproblems **overlap** — same subproblems solved repeatedly, hence memoization/tabulation.

### A4.2
1. **Greedy Choice:** ∃ optimal solution starting with greedy choice. Kruskal: minimum weight edge belongs to some MST (cut property).
2. **Optimal Substructure:** After greedy choice, remaining subproblem has optimal solution. Kruskal: after adding edge (u,v), contract u,v → MST of contracted graph + chosen edge.

### A4.3
Complexity Θ(nW) where W is numeric value, not log W. If W=10⁹, slow despite small n. Polynomial would be O(n^c log^d W).

### A4.4
**No.** Invariant (extracted distance = true distance) assumes adding edge cannot reduce distance of extracted vertex. With negative weights, path through unextracted vertex could be shorter.
Counterexample: A→B(1), B→C(-2), A→C(1). Dijkstra extracts C(1) then B(1) → C distance=1, but A→B→C = -1.

---

# MODULE 5: SPACE COMPLEXITY

## 5.1 Detailed Lecture Notes

### 5.1.1 Definition and Measurement

**Space Complexity S(n):** Memory (machine words) used for input size n.

**Components:**
- **Input Space:** Size of input data (often excluded from *auxiliary* space)
- **Auxiliary Space:** Extra space for local variables, call stack, temporary structures
- **Output Space:** Size of output

**Convention:** Space complexity = auxiliary space (excluding input/output)

### 5.1.2 Space Analysis

**Iterative Algorithms:**
```python
def algo_iter(n):
    a = 0                    # O(1)
    tab = [0] * n            # O(n)
    mat = [[0]*n for _ in range(n)]  # O(n²)
    return sum(tab)
# Auxiliary space: O(n²)
```

**Recursive Algorithms:**
Space = **Max recursion depth × Space per frame**

```python
def fact(n):
    if n <= 1: return 1
    return n * fact(n-1)
# Depth = n, each frame O(1) → Space = Θ(n)

def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])      # Copy: O(n/2)
    right = merge_sort(arr[mid:])     # Copy: O(n/2)
    return merge(left, right)         # O(n) temporary
# Depth = log n, but copies each level → O(n log n) naive
# Optimized (indices): O(n) temp array + O(log n) stack = O(n)
```

### 5.1.3 Time-Space Tradeoffs

| Technique | Time Gain | Space Cost | Example |
|-----------|-----------|------------|---------|
| **Memoization** | Avoids recomputation | Table O(n) or O(n²) | Fibonacci, LCS |
| **Tabulation** | Iterative, no stack | Table O(n) or O(n²) | Knapsack, Floyd-Warshall |
| **Precomputation** | O(1) queries | Lookup table | Perfect hash, precomputed factorials |
| **Compression** | Less I/O | CPU decompression | BWT, LZ77 |
| **Streaming** | Constant space | Single pass | Reservoir sampling |

**Fibonacci Comparison:**
| Method | Time | Space |
|--------|------|-------|
| Naive Recursive | Θ(φⁿ) | Θ(n) stack |
| Memoized | Θ(n) | Θ(n) table + stack |
| Iterative (2 vars) | Θ(n) | **Θ(1)** |
| Binet Formula | Θ(log n)* | Θ(1) |
| Matrix Exponentiation | Θ(log n) | Θ(1) |

*Floating precision limited.*

### 5.1.4 Space Complexity of Classic Algorithms

| Algorithm | Auxiliary Space | Notes |
|-----------|-----------------|-------|
| Merge Sort | Θ(n) | Temporary array for merge |
| QuickSort | Θ(log n) avg, Θ(n) worst | Recursion stack (tail-call optimizable) |
| HeapSort | Θ(1) | In-place |
| BFS | Θ(V) | Queue + visited array |
| DFS | Θ(V) | Stack (explicit or recursive) |
| Dijkstra (heap) | Θ(V) | Heap + distances + prev |
| Floyd-Warshall | Θ(V²) | Distance matrix |
| DP 1D | Θ(n) or Θ(W) | 1D table |
| DP 2D | Θ(n²) or Θ(nW) | 2D table (optimizable if local deps) |

---

## 5.2 Solved Practical Exercises

### Exercise 5.1: Recursive vs Iterative Space

**Problem:** Compare auxiliary space of:

```python
# A
def fact_rec(n):
    if n <= 1: return 1
    return n * fact_rec(n-1)

# B
def fact_iter(n):
    result = 1
    for i in range(2, n+1):
        result *= i
    return result
```

**Solution:**
- A: Depth n, each frame stores n and return address → **Θ(n)**
- B: Variables `result`, `i` → **Θ(1)**

### Exercise 5.2: In-Place Merge Sort?

**Problem:** Can merge sort be Θ(1) auxiliary space?

**Solution:** Standard merge sort needs Θ(n) for merge.
In-place variants exist (Huang & Langston, 1988; Geffert) but extremely complex, high constants, not practical.
Heapsort = Θ(n log n) time, **Θ(1) space** — practical alternative.

### Exercise 5.3: Knapsack Space Optimization

**Problem:** Standard 0/1 Knapsack uses 2D O(nW). Reduce to O(W).

**Solution:**
```python
# 2D Version
dp = [[0]*(W+1) for _ in range(n+1)]
for i in range(1, n+1):
    for w in range(W+1):
        if w_i <= w:
            dp[i][w] = max(dp[i-1][w], v_i + dp[i-1][w-w_i])
        else:
            dp[i][w] = dp[i-1][w]

# 1D Version (DECREASING weight loop!)
dp = [0]*(W+1)
for i in range(n):
    for w in range(W, w_i-1, -1):  # Decreasing crucial!
        dp[w] = max(dp[w], v_i + dp[w-w_i])
```
**Why decreasing?** Prevents using dp[w-w_i] already updated for item i (would allow repetition).

---

## 5.3 Theoretical Assessment Questions

### Q5.1
Space complexity of recursive vs iterative binary search?

### Q5.2
Why does bottom-up tabulation generally use less space than top-down memoization?

### Q5.3
Give an example where higher time complexity is accepted to reduce space.

### Q5.4
Is BFS space always Θ(V)?

---

## 5.4 Model Answers

### A5.1
- Recursive: Θ(log n) (call stack, depth log n)
- Iterative: Θ(1) (low, high, mid variables)

### A5.2
Memoization: table + call stack (recursion depth). Tabulation: table only (iterative). Tabulation also enables dimension elimination if dependencies local (e.g., knapsack 1D vs 2D).

### A5.3
**Streaming algorithms:** Single pass, O(1) or O(log n) space, but sometimes higher time or approximate results (e.g., HyperLogLog for distinct counting). Also: recomputation on demand instead of storing.

### A5.4
Yes generally (queue + visited set). But for trees without cycles (no visited set needed), queue only = O(max width) ≤ O(V). For complete binary tree, width = Θ(V) at last level.

---

# MODULE 6: COMPLEXITY AND PROOF OF CORRECTNESS

## 6.1 Detailed Lecture Notes

### 6.1.1 Complexity Classes: P, NP, NP-Complete

**Decision Problem:** Yes/No answer.

**P (Polynomial Time):** Decision problems solvable in polynomial time by deterministic TM.
Examples: Sorting, binary search, shortest path (Dijkstra), max flow, primality (AKS).

**NP (Nondeterministic Polynomial):** Decision problems where a certificate can be **verified** in polynomial time.
Equivalent: Solvable in polynomial time by nondeterministic TM.
Examples: SAT, 3-SAT, CLIQUE, 3-COLORING, KNAPSACK (decision), TSP (decision), HAMILTONIAN.

**Relationship:** P ⊆ NP (open: P = NP?)

**NP-Complete (NPC):**
L is NP-complete iff:
1. L ∈ NP
2. ∀ L' ∈ NP, L' ≤ₚ L (polynomial-time reducible)

**Cook-Levin Theorem (1971):** SAT is NP-complete.
**Proof Method:** Reduction from known NPC problem.

**Classic NPC Problems:**
SAT, 3-SAT, CLIQUE, VERTEX COVER, 3-COLORING, KNAPSACK (decision), TSP (decision), HAMILTONIAN, PARTITION, SUBSET SUM.

**NP-Hard:** At least as hard as NP problems (not necessarily in NP).
Example: Optimization versions of TSP, Knapsack.

### 6.1.2 Proof by Induction

**Principle:** Prove P(n) ∀ n ∈ ℕ:
1. **Base:** P(0) or P(1) true
2. **Inductive Step:** P(k) ⇒ P(k+1) ∀ k ≥ base

**Strong Induction:** P(0) ∧ ... ∧ P(k) ⇒ P(k+1)

**Application to Recursive Algorithms:**
P(n) = "Algorithm terminates and produces correct result for size n"
- Base: Base cases (n=0, n=1)
- Inductive: Assume correct for sizes < n, prove for n

**Example — Factorial Correctness:**
```python
def fact(n):
    if n <= 1: return 1      # Base: fact(0)=1, fact(1)=1 ✓
    return n * fact(n-1)     # Inductive: if fact(n-1)=(n-1)! then fact(n)=n·(n-1)!=n! ✓
```

### 6.1.3 Loop Invariants

**Hoare Logic for Loop Correctness:**
For `while condition: body` with invariant I:

1. **Initialization:** I true before first iteration
2. **Maintenance:** If I true before iteration and condition true, then I true after
3. **Termination:** Loop terminates (variant strictly decreases and bounded)
4. **Post-condition:** I ∧ ¬condition ⇒ desired property

**Example — Linear Search:**
```python
def linear_search(arr, x):
    i = 0
    while i < len(arr) and arr[i] != x:
        i += 1
    return i < len(arr)
```
**Invariant I(i):** "x does not appear in arr[0..i-1]"

- **Init:** i=0, arr[0..-1] empty → I true ✓
- **Maintenance:** If I(i) true and arr[i] ≠ x, then I(i+1) true ✓
- **Termination:** i increases, bounded by len(arr) → terminates
- **Post:** I(i) ∧ (i ≥ len(arr) ∨ arr[i]=x)
  - If i < len(arr): arr[i]=x and x not before → first x found ✓
  - If i = len(arr): x not in arr[0..len-1] → x absent ✓

### 6.1.4 Proof by Contradiction

**Principle:** Assume negation of thesis, derive contradiction.

**Example — Dijkstra Correctness:**
Thesis: When u extracted, d[u] = δ(s, u).
Assume ∃ first u extracted with d[u] > δ(s, u).
Let y be first vertex on optimal path s⇝u not yet extracted, x its predecessor (extracted before u).
At x extraction, relaxation of (x,y): d[y] ≤ d[x] + w(x,y) = δ(s,x) + w(x,y) = δ(s,y).
Since d[u] ≤ d[y] (u extracted before y) and d[y] = δ(s,y) ≤ δ(s,u), we get d[u] ≤ δ(s,u).
Contradiction with d[u] > δ(s,u). ✓

---

## 6.2 Solved Practical Exercises

### Exercise 6.1: Induction Proof — Insertion Sort

**Problem:** Prove insertion sort correctness by induction.

**Solution:**
```python
for i in range(1, n):
    key = arr[i]
    j = i - 1
    while j >= 0 and arr[j] > key:
        arr[j+1] = arr[j]
        j -= 1
    arr[j+1] = key
```

**Loop Invariant I(i):** "Subarray arr[0..i-1] is sorted and contains same elements as originally."

- **Base (i=1):** arr[0..0] = 1 element → sorted ✓
- **Inductive:** Assume I(i) true. Iteration i inserts arr[i] (`key`) into correct position in sorted arr[0..i-1] (inner loop shifts elements > key). Result: arr[0..i] sorted, same elements → I(i+1) true ✓
- **Termination:** i from 1 to n-1 → terminates
- **Post:** i = n, I(n): arr[0..n-1] sorted, permutation of original ✓

### Exercise 6.2: NPC Reduction — 3-SAT to CLIQUE

**Problem:** Show 3-SAT ≤ₚ CLIQUE.

**Solution:**
3-SAT instance: Clauses C₁...Cₖ, each 3 literals.
Construct graph G:
- Vertices: One per literal per clause → 3k vertices
- Edges: Between vertices of **different** clauses if literals **not contradictory** (x and ¬x are contradictory)

**Claim:** 3-SAT satisfiable ⇔ G has k-clique.

⇒ If φ satisfiable, pick one true literal per clause. These k literals pairwise non-contradictory → form clique.
⇐ If k-clique, has exactly one vertex per clause (no intra-clause edges). Assign true to clique literals (consistent) → all clauses satisfied. ✓

Construction polynomial in |φ|. Hence 3-SAT ≤ₚ CLIQUE.

### Exercise 6.3: Loop Invariant — QuickSort Partition (Lomuto)

**Problem:** Prove correctness of Lomuto partition.

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

**Solution:**
**Invariant I(j) at start of iteration j:**
1. arr[low..i] ≤ pivot
2. arr[i+1..j-1] > pivot
3. arr[high] = pivot

- **Init (j=low):** i = low-1. arr[low..low-1] empty (≤ pivot) ✓. arr[low..low-1] empty (> pivot) ✓. arr[high]=pivot ✓.
- **Maintenance:** Case `arr[j] ≤ pivot`: i++, swap arr[i]↔arr[j]. Element ≤ pivot moved to zone 1, zone 2 unchanged ✓. Case `arr[j] > pivot`: i unchanged, j++ implicitly. Element stays in zone 2 ✓.
- **Termination:** j = high. I(high): arr[low..i] ≤ pivot, arr[i+1..high-1] > pivot, arr[high]=pivot.
- **Final Swap:** swap arr[i+1] and arr[high]. arr[low..i] ≤ pivot, arr[i+1]=pivot, arr[i+2..high] > pivot. Return i+1 = final pivot position ✓

---

## 6.3 Theoretical Assessment Questions

### Q6.1
Difference between NP-complete and NP-hard?

### Q6.2
State the 4 steps of loop invariant correctness proof.

### Q6.3
Show that if P = NP, then every problem in P (except ∅ and Σ*) is NP-complete.

### Q6.4
Why does Dijkstra's proof use "first vertex extracted with d[u] > δ(s,u)"?

---

## 6.4 Model Answers

### A6.1
**NP-complete** = in NP ∩ NP-hard (decision problem, verifiable in poly time, as hard as any NP). **NP-hard** = at least as hard as NP problems, but not necessarily in NP (can be optimization, not verifiable in poly time, even undecidable).

### A6.2
1. **Initialization:** Invariant true before first iteration
2. **Maintenance:** If invariant true before iteration and condition true, remains true after
3. **Termination:** Loop terminates (loop variant)
4. **Post-condition:** Invariant ∧ ¬condition ⇒ desired property

### A6.3
Let L ∈ P, L ≠ ∅, L ≠ Σ*. Since P = NP, L ∈ NP. For any L' ∈ NP, L' ∈ P. Reduce L' to L in poly time: compute L' answer (in P), output fixed instance in L (if YES) or outside L (if NO). Thus L' ≤ₚ L, so L is NP-complete.

### A6.4
Proof by contradiction minimizing counterexample. Taking **first** such u guarantees its predecessor x on optimal path was correctly processed (d[x] = δ(s,x)), enabling relaxation to yield contradiction. Arbitrary u might have incorrect predecessor.

---

# MODULE 7: ALGORITHM OPTIMIZATION

## 7.1 Detailed Lecture Notes

### 7.1.1 Identifying Bottlenecks

**Profiling:**
- **Theoretical:** Asymptotic analysis (Big O)
- **Empirical:** Actual time, operation counts, cache misses, branch mispredictions
- **Tools:** perf, gprof, Valgrind/Callgrind, cProfile, line_profiler

**Amdahl's Law:** Max speedup = 1 / ((1 - p) + p/s) where p = optimizable fraction, s = speedup of that part.
*Example:* Optimize 90% of code 10× → global speedup = 1/(0.1 + 0.9/10) = 5.26×.

**Typical Bottlenecks:**
- Unnecessary nested loops → reduce algorithmic complexity
- Frequent memory allocations → reuse buffers, pools
- Non-linear memory access → improve locality (cache)
- Excessive recursion → iterative transformation
- Redundant computations → memoization, precomputation

### 7.1.2 Optimization Techniques

#### 1. Loop Optimizations
```python
# Before: O(n²)
for i in range(n):
    for j in range(n):
        if i == j:  # Rare
            do_something()

# After: O(n)
for i in range(n):
    do_something()
```

**Loop-Invariant Code Motion:**
```python
# Before
for i in range(n):
    x = expensive_computation(y)  # Independent of i
    process(x, i)

# After
x = expensive_computation(y)
for i in range(n):
    process(x, i)
```

**Loop Fusion:**
```python
# Before: 2 passes
for i in range(n): a[i] = f(i)
for i in range(n): b[i] = g(a[i])

# After: 1 pass, better cache locality
for i in range(n):
    a[i] = f(i)
    b[i] = g(a[i])
```

#### 2. Recursion Reduction
**Tail Call Elimination:**
```python
# Tail recursive
def fact_tail(n, acc=1):
    if n <= 1: return acc
    return fact_tail(n-1, n*acc)

# Iterative equivalent
def fact_iter(n):
    acc = 1
    while n > 1:
        acc *= n
        n -= 1
    return acc
```

**Recursion → Iteration (Explicit Stack):**
```python
# Recursive DFS
def dfs_rec(u):
    visited.add(u)
    for v in adj[u]:
        if v not in visited:
            dfs_rec(v)

# Iterative DFS
def dfs_iter(start):
    stack = [start]
    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            for v in adj[u]:
                stack.append(v)
```

#### 3. Memory Access Optimization (Locality)
- **Temporal locality:** Reuse recently accessed data
- **Spatial locality:** Access contiguous memory

```python
# Poor: column-major (stride n)
for j in range(n):
    for i in range(n):
        sum += mat[i][j]

# Good: row-major (contiguous)
for i in range(n):
    for j in range(n):
        sum += mat[i][j]
```

**Blocking/Tiling (Matrix Multiply):**
```python
for ii in range(0, n, B):
    for jj in range(0, n, B):
        for kk in range(0, n, B):
            for i in range(ii, min(ii+B, n)):
                for j in range(jj, min(jj+B, n)):
                    for k in range(kk, min(kk+B, n)):
                        C[i][j] += A[i][k] * B[k][j]
```

#### 4. Algorithmic Paradigm Selection
| Problem | Optimal Approach | Complexity |
|---------|------------------|------------|
| Sorting | D&C (merge) / Greedy (heap) | Θ(n log n) |
| Shortest Path (≥0) | Greedy (Dijkstra) | Θ((V+E) log V) |
| Shortest Path (any) | DP (Bellman-Ford) | Θ(VE) |
| Knapsack 0/1 | DP | Θ(nW) |
| MST | Greedy (Kruskal/Prim) | Θ(E log V) |
| Metric TSP | Greedy Approx (Christofides) | 1.5-approx |

#### 5. Specialized Data Structures
| Need | Structure | Key Operations |
|------|-----------|----------------|
| Frequent min/max, insert | Heap | O(log n) insert, O(1) peek, O(log n) extract |
| Search, insert, delete, order | Balanced BST | O(log n) all |
| Union-Find (components) | DSU + path compression | O(α(n)) ≈ O(1) |
| Frequencies, top-k | Heap + hash / Count-Min | O(1) amortized |
| Prefix search | Trie | O(length) |
| Intervals | Interval Tree / Segment Tree | O(log n) |

### 7.1.3 Limits of Optimization

**90/10 Rule:** 90% execution time in 10% of code.
**Premature Optimization:** "Root of all evil" (Knuth). Correct, clear, maintainable code first. Optimize *after* profiling.
**Tradeoffs:**
- Time vs Space
- Time vs Readability/Maintainability
- Optimality vs Simplicity (approximation)
- Generality vs Specialization

---

## 7.2 Solved Practical Exercises

### Exercise 7.1: Loop Optimization — Polynomial Evaluation

**Problem:** Optimize P(x) = a₀ + a₁x + a₂x² + ... + aₙxⁿ

**Solution:**
**Naive (O(n²) multiplications):**
```python
def poly_naif(a, x):
    result = 0
    for i in range(len(a)):
        term = a[i]
        for _ in range(i):
            term *= x
        result += term
    return result
```

**Horner's Method (O(n)):**
```python
def poly_horner(a, x):
    result = 0
    for coeff in reversed(a):
        result = result * x + coeff
    return result
```
*Factorization: ((...((aₙ)x + aₙ₋₁)x + ...)x + a₀)*

### Exercise 7.2: Space Optimization — Fibonacci

**Problem:** Four implementations with different time/space complexities.

**Solution:**
| Version | Time | Space | Notes |
|---------|------|-------|-------|
| Naive Recursive | Θ(φⁿ) | Θ(n) stack | Unusable n>40 |
| Memoized Recursive | Θ(n) | Θ(n) table + stack | Top-down DP |
| Iterative (2 vars) | Θ(n) | **Θ(1)** | Space optimal |
| Matrix / Doubling | Θ(log n) | Θ(1) | Fast exponentiation |

**Matrix Method:**
```
[Fₙ₊₁  Fₙ  ] = [1 1]ⁿ
[Fₙ    Fₙ₋₁]   [1 0]
```
Exponentiation by squaring → O(log n) 2×2 matrix multiplications.

### Exercise 7.3: Algorithmic Optimization — Majority Element

**Problem:** Find element appearing > n/2 times (if exists). O(n) time, O(1) space.

**Solution: Boyer-Moore Majority Vote**
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
    # Optional verification
    if arr.count(candidate) > len(arr) // 2:
        return candidate
    return None
```
**Proof:** Each (candidate, other) pair cancels. If majority exists, it survives. Time Θ(n), Space Θ(1).

---

## 7.3 Theoretical Assessment Questions

### Q7.1
Explain Horner's method for polynomial evaluation. Why is it optimal in multiplications?

### Q7.2
When is Tail Call Optimization (TCO) applicable? Give an example where it is not.

### Q7.3
What is "Loop Unrolling"? Main disadvantage?

### Q7.4
Explain Amdahl's Law. If 80% of program is optimized 5×, what is max global speedup?

---

## 7.4 Model Answers

### A7.1
P(x) = a₀ + x(a₁ + x(a₂ + ... + x(aₙ₋₁ + xaₙ)...)). n multiplications, n additions. Optimal because any degree-n polynomial requires ≥ n multiplications (otherwise would yield degree < n polynomial).

### A7.2
TCO applies if recursive call is **last operation** (no computation after return).
**No TCO example:**
```python
def fact(n):
    if n <= 1: return 1
    return n * fact(n-1)  # Multiplication AFTER recursive call
```
Stack frame retained for post-return multiplication.

### A7.3
Replicate loop body k times, iterate n/k times. Reduces loop overhead, enables SIMD vectorization.
Disadvantage: **Code bloat** → may degrade performance if exceeds instruction cache (L1I).

### A7.4
Speedup = 1 / ((1-p) + p/s).
For p=0.8, s=5: 1 / (0.2 + 0.8/5) = 1 / (0.2 + 0.16) = 1/0.36 ≈ **2.78×**.
Even massive optimization of part is limited by unoptimized portion.

---

# APPENDICES

## Appendix A: Asymptotic Notation Summary

| Notation | Definition | Meaning |
|----------|------------|---------|
| f = O(g) | ∃c,n₀>0: ∀n≥n₀, f(n) ≤ c·g(n) | f upper-bounded by g (worst case) |
| f = Ω(g) | ∃c,n₀>0: ∀n≥n₀, f(n) ≥ c·g(n) | f lower-bounded by g (best case) |
| f = Θ(g) | ∃c₁,c₂,n₀>0: ∀n≥n₀, c₁g(n) ≤ f(n) ≤ c₂g(n) | f tightly bounded by g |
| f = o(g) | ∀c>0, ∃n₀: ∀n≥n₀, f(n) < c·g(n) | f strictly smaller than g |
| f = ω(g) | ∀c>0, ∃n₀: ∀n≥n₀, f(n) > c·g(n) | f strictly larger than g |

## Appendix B: Master Theorem

For T(n) = aT(n/b) + f(n), a ≥ 1, b > 1, f(n) > 0:

Let c = log_b(a).

1. **Case 1:** f(n) = O(n^{c-ε}), ε>0 → T(n) = Θ(n^c)
2. **Case 2:** f(n) = Θ(n^c log^k n), k ≥ 0 → T(n) = Θ(n^c log^{k+1} n)
3. **Case 3:** f(n) = Ω(n^{c+ε}), ε>0 AND a·f(n/b) ≤ k·f(n), k<1 (regularity) → T(n) = Θ(f(n))

## Appendix C: Sorting Algorithm Complexities

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble Sort | Θ(n) | Θ(n²) | Θ(n²) | O(1) | Yes |
| Insertion Sort | Θ(n) | Θ(n²) | Θ(n²) | O(1) | Yes |
| Selection Sort | Θ(n²) | Θ(n²) | Θ(n²) | O(1) | No |
| Merge Sort | Θ(n log n) | Θ(n log n) | Θ(n log n) | O(n) | Yes |
| QuickSort | Θ(n log n) | Θ(n log n) | Θ(n²) | O(log n) | No |
| Heap Sort | Θ(n log n) | Θ(n log n) | Θ(n log n) | O(1) | No |
| Counting Sort | Θ(n+k) | Θ(n+k) | Θ(n+k) | O(k) | Yes |
| Radix Sort | Θ(d(n+k)) | Θ(d(n+k)) | Θ(d(n+k)) | O(n+k) | Yes |

## Appendix D: Key Equations Reference

**Backpropagation:**
∂J/∂W⁽ˡ⁾ = δ⁽ˡ⁾ (a⁽ˡ⁻¹⁾)ᵀ
δ⁽ˡ⁾ = (W⁽ˡ⁺¹⁾)ᵀ δ⁽ˡ⁺¹⁾ ⊙ σ'(z⁽ˡ⁾)

**Gradient Checking:**
∂J/∂θᵢ ≈ [J(θ + εeᵢ) - J(θ - εeᵢ)] / (2ε)

**Weight Initialization:**
- Xavier/Glorot: Var(W) = 2/(n_in + n_out)
- He: Var(W) = 2/n_in (better for ReLU)

**Loss Functions:**
- MSE: ½n Σ (y - ŷ)²
- Cross-Entropy: -1/n Σ [y log ŷ + (1-y) log(1-ŷ)]
- Huber: ½(y-ŷ)² if |y-ŷ|≤δ else δ|y-ŷ| - ½δ²

---

# COMPREHENSIVE EXERCISE INDEX

| Module | Solved Exercises | Theoretical Questions |
|--------|------------------|----------------------|
| 1 | 1.1, 1.2 | Q1.1 - Q1.4 |
| 2 | 2.1, 2.2, 2.3, 2.4 | Q2.1 - Q2.4 |
| 3 | 3.1, 3.2, 3.3 | Q3.1 - Q3.4 |
| 4 | 4.1, 4.2, 4.3, 4.4 | Q4.1 - Q4.4 |
| 5 | 5.1, 5.2, 5.3 | Q5.1 - Q5.4 |
| 6 | 6.1, 6.2, 6.3 | Q6.1 - Q6.4 |
| 7 | 7.1, 7.2, 7.3 | Q7.1 - Q7.4 |

**Total:** 21 solved exercises + 28 theoretical questions with model answers

---

*Curriculum developed for "Design and Analysis of Algorithms" — 21 Hours*  
*Based on standard academic references (CLRS, Kleinberg & Tardos, Sedgewick & Wayne)*  
*Version 1.0 — Professional Academic Standard*