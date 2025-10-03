---
title: "Racing Exponentials: Exact Rank Probabilities for Heterogeneous Exponential Random Variables"
date: '2025-07-13'
excerpt: "I present two exact approaches for efficiently computing the probability that an exponential random variable ranks kth among N independent exponentials with different rate parameters."
thumbnail: /gallery/thumbnails/racing-exponentials.jpg
toc: true
categories:
- [Probability]
tags:
- probability
- puzzle
---

In a recent event that made me feel like a true mathematician of old, I was excited to receive a piece of (admittedly e-)mail from a PhD friend of mine posing an intriguing probability problem that he needed solving.

The problem concerned $N$ independent (but not identically-distributed) random variables $X_1, \ldots, X_N$ and asks for the probability that $X_1$ ranks $k$th among them when sorted in ascending order. Specifically, he was interested in the case where each $X_i$ is exponentially distributed with unique rate parameters $\lambda_i$, i.e. $X_i \sim \text{Exp}(\lambda_i)$.

The obvious approach to this problem is Monte Carlo simulation, which he was well aware of. For moderate values of $N$ this is adequate, though computational costs rise rapidly when high precision is required or when $N$ is large. It therefore raises the question, whether there is a way to efficiently compute an exact value for this probability with a direct method.

I was initially skeptical about finding a tractable solution. To see why, consider the general form of this probability. For $X_1$ to rank $k$th, we need exactly $k-1$ of the other variables to be smaller than $X_1$, and the remaining $N-k$ variables to be larger. We can express this by conditioning on the value of $X_1$. If $X_1 = x$, then we need to choose which $k-1$ of the remaining $N-1$ variables fall below $x$, and the rest must exceed $x$. In the identically-distributed case, this is just a straightforward sum over $N$ terms with some binomial coefficients. However, in the heterogeneous case, we must consider all $\binom{N-1}{k-1}$ possible subsets of size $k-1$ from $\{2, \ldots, N\}$.
This gives:

$$P(X_1 \text{ ranks } k\text{th}) = \int_{-\infty}^{\infty} f_1(x) \sum_{\substack{S \subseteq \{2,\ldots,N\} \\ |S| = k-1}} \left[\prod_{j \in S} F_j(x) \prod_{j \notin S, j \neq 1} (1-F_j(x))\right] dx$$

Yikes! Here $f_1$ and $F_j$ denote the density and CDF of the respective random variables, and the sum runs over all $\binom{N-1}{k-1}$ subsets $S$ of size $k-1$ from $\{2, \ldots, N\}$. For each such subset, the integrand contains a product of $k-1$ CDFs (for variables in $S$) and $N-k$ survival functions (for variables not in $S$). This is a complex expression even before considering the sum over exponentially many subsets. For general distributions, it's probably fair to say that you're not going to find such an integrand in your table of integrals.

## A Closed-Form Solution for Exponentials

Despite my initial pessimism, I decided to work through the exponential case to see how far I could get, and luckily, things just so happen to simplify quite nicely.

For $X_i \sim \text{Exp}(\lambda_i)$, we have the density $f_i(x) = \lambda_i e^{-\lambda_i x}$ and CDF $F_i(x) = 1 - e^{-\lambda_i x}$ for $x \geq 0$. Substituting these into the probability expression above gives:

$$P(X_1 \text{ ranks } k\text{th}) = \sum_{\substack{S \subseteq \{2,\ldots,N\} \\ |S| = k-1}} \int_{0}^{\infty} \lambda_1 e^{-\lambda_1 x} \prod_{j \in S} (1-e^{-\lambda_j x}) \prod_{j \notin S, j \neq 1} e^{-\lambda_j x} \, dx$$

The crucial insight is that the product $\prod_{j \in S} (1-e^{-\lambda_j x})$ can be expanded using the inclusion-exclusion principle. For any finite set $S$, we have:

$$\prod_{j \in S} (1-e^{-\lambda_j x}) = \sum_{T \subseteq S} (-1)^{|T|} \prod_{j \in T} e^{-\lambda_j x}$$

Here the sum is over all subsets $T$ of $S$ (including the empty set), and the sign alternates based on the size of $T$. We can then easily simplify the product of exponentials as:

$$\prod_{j \in T} e^{-\lambda_j x} = e^{-\sum_{j \in T} \lambda_j x}$$

This simplification is crucial and appears to be fairly unique to the exponential distribution.

Substituting this expansion back into our integral:

$$P(X_1 \text{ ranks } k\text{th}) = \sum_{\substack{S \subseteq \{2,\ldots,N\} \\ |S| = k-1}} \sum_{T \subseteq S} (-1)^{|T|} \int_{0}^{\infty} \lambda_1 e^{-\lambda_1 x} e^{-\sum_{j \in T} \lambda_j x} \prod_{j \notin S, j \neq 1} e^{-\lambda_j x} \, dx$$

Still a bit messy, but importantly, we've managed to move the integral inside the sums, making a closed-form solution at least tractable.

We can now combine all the exponential terms in the integrand. Collecting all terms involving $x$ in the exponent we have:

$$\int_{0}^{\infty} \lambda_1 \exp\left(-\left[\lambda_1 + \sum_{j \in T} \lambda_j + \sum_{j \notin S, j \neq 1} \lambda_j\right] x\right) dx$$

It will be convenient to define $\Lambda(S, T)$ to be the constant coefficient of $x$ in this exponential:

$$\Lambda(S, T) = \lambda_1 + \sum_{j \in T} \lambda_j + \sum_{j \notin S, j \neq 1} \lambda_j$$

With this notation, our integral has a nice closed-form as:

$$\int_{0}^{\infty} \lambda_1 e^{-\Lambda(S,T) x} dx = \frac{\lambda_1}{\Lambda(S,T)}$$

We can simplify the expression for $\Lambda(S,T)$ further. Note that we are summing $\lambda_1$, plus the rates for indices in $T \subseteq S$, plus the rates for all indices outside $S$ (excluding 1). This is equivalent to summing all rates except those in $S \setminus T$ (the elements of $S$ not in $T$). If we define $\Lambda = \sum_{j=1}^{N} \lambda_j$ to be the sum of all rates, then:

$$\Lambda(S, T) = \Lambda - \sum_{j \in S \setminus T} \lambda_j$$

Putting everything together, we obtain the closed-form (if not still quite computationally expensive) expression:

$$P(X_1 \text{ ranks } k\text{th}) = \lambda_1 \sum_{\substack{S \subseteq \{2,\ldots,N\} \\ |S| = k-1}} \sum_{T \subseteq S} \frac{(-1)^{|T|}}{\Lambda - \sum_{j \in S \setminus T} \lambda_j}$$

This is a double sum over finite sets that can be computed directly. The outer sum iterates over all subsets $S$ of size $k-1$ from $\{2, \ldots, N\}$, of which there are $\binom{N-1}{k-1}$. For each such subset $S$, the inner sum iterates over all subsets $T$ of $S$, of which there are $2^{|S|} = 2^{k-1}$. Each term in the inner sum involves computing a sum over at most $k-1$ elements (for $S \setminus T$), which takes $O(k)$ time. Therefore, the overall time complexity is:

$$O\left(\binom{N-1}{k-1} \cdot 2^{k-1} \cdot k\right)$$

The behavior of this complexity depends strongly on $k$. When $k=1$, the outer sum has only $\binom{N-1}{0} = 1$ term, and the inner sum for the empty set $S = \emptyset$ has only one term (the empty set $T = \emptyset$), giving $\Lambda(\emptyset, \emptyset) = \Lambda$. The formula thus reduces to the well-known result $P(X_1 \text{ is minimum}) = \lambda_1 / \Lambda$, with $O(1)$ complexity.

At the other extreme, when $k = N/2$, the binomial coefficient is largest. Using Stirling's approximation, we have:

$$\binom{N-1}{N/2-1} \approx \frac{2^{N-1}}{\sqrt{\pi (N-1)/2}} \approx \frac{2^{N-1}}{\sqrt{\pi N/2}}$$

Combining with the $2^{k-1} = 2^{N/2-1}$ factor from the inner sum gives:

$$\frac{2^{N-1}}{\sqrt{\pi N/2}} \cdot 2^{N/2-1} = \frac{2^{N-1+N/2-1}}{\sqrt{\pi N/2}} = \frac{2^{3N/2-2}}{\sqrt{\pi N/2}} = O\left(2^{3N/2} \cdot \frac{1}{\sqrt{N}}\right)$$

Including the $O(k) = O(N)$ factor for computing subset sums, the overall complexity for $k = N/2$ is $O(2^{3N/2} \cdot \sqrt{N})$.

The following Julia implementation computes this probability directly:

```julia
using Combinatorics

function prob_x1_kth_direct(λs::Vector{Float64}, k::Int)
    N = length(λs)
    Λ = sum(λs)
    prob = 0.0

    for S in combinations(2:N, k-1)
        for T in powerset(S)
            sign = (-1)^length(T)
            denominator = Λ - sum(λs[j] for j in setdiff(S, T); init=0.0)
            prob += sign / denominator
        end
    end

    return λs[1] * prob
end
```

## A Dynamic Programming Approach

While the direct summation method is elegant, it is essentially a brute-force enumeration of all possible subsets of variables that could rank below $X_1$. After some playing about, I found out that we can do better than this by taking a dynamic programming approach that exploits the memoryless property of the exponential distribution.

First, we note that the probability that any $X_i$ is the minimum among all $N$ variables is:

$$P(X_i = \min(X_1, \ldots, X_N)) = \frac{\lambda_i}{\sum_{j=1}^{N} \lambda_j}$$

This result can be understood through the Poisson process interpretation: independent exponential random variables $X_1, \ldots, X_N$ with rates $\lambda_1, \ldots, \lambda_N$ represent the first arrival times of $N$ independent Poisson processes. The superposition of these processes is itself a Poisson process with rate $\Lambda = \sum_{j=1}^{N} \lambda_j$. By the thinning property, each arrival of the superposed process is assigned to process $i$ with probability $\lambda_i / \Lambda$. Therefore, the probability that the first arrival comes from process $i$ is simply $\lambda_i / \Lambda$.

Crucially, once we observe which variable is the minimum, the memoryless property tells us that the remaining variables are still independent exponentials with their original rates. To see this, suppose $X_j$ is the minimum and takes value $t$. Then for any other variable $X_i$ with $i \neq j$, we know $X_i > t$. By the memoryless property of the exponential distribution:

$$P(X_i > t + s \mid X_i > t) = P(X_i > s)$$

In other words, conditioning $X_i$ on being larger than $t$ simply shifts the distribution by $t$, but the residual $X_i - t$ is still exponentially distributed with rate $\lambda_i$. This means that after removing the minimum, the remaining variables form exactly the same type of problem, just with one fewer variable.

This observation suggests a recursive approach. Let $P(R, k)$ denote the probability that $X_1$ ranks $k$th among the subset of variables indexed by $R \subseteq \{1, \ldots, N\}$, where we require $1 \in R$. We will also use the notation $\Lambda_R = \sum_{j \in R} \lambda_j$ for the sum of rates in subset $R$.

The base case is straightforward: if we want $X_1$ to be the minimum (rank 1st), this occurs with probability:

$$P(R, 1) = \frac{\lambda_1}{\Lambda_R}$$

For $k \geq 2$, we condition on which variable is the minimum among those in $R$. There are two cases. First, if $X_1$ is the minimum, then $X_1$ ranks 1st, which doesn't contribute to $P(R, k)$ for $k \geq 2$. Second, if some other variable $X_j$ with $j \in R \setminus \{1\}$ is the minimum, then by the memoryless property, we remove $X_j$ and $X_1$ must rank $(k-1)$th among the remaining variables. This gives the recurrence:

$$P(R, k) = \sum_{j \in R \setminus \{1\}} \frac{\lambda_j}{\Lambda_R} \cdot P(R \setminus \{j\}, k-1)$$

The probability we seek is $P(\{1, \ldots, N\}, k)$.

To compute this efficiently, we use memoization. The state space consists of all possible subsets $R \subseteq \{1, \ldots, N\}$ containing index 1, paired with all possible rank values from 1 to $|R|$. There are at most $2^{N-1}$ such subsets (since 1 must be included), and for each subset of size $m$ we consider up to $m$ different rank values. This gives roughly $O(2^N \cdot N)$ states in total. For each state, computing the sum in the recurrence requires iterating over at most $N$ values of $j$ and performing $O(1)$ work per value (assuming memoized values are cached). Thus the overall time complexity is:

$$O(2^N \cdot N^2)$$

A naive implementation would use a dictionary to store memoized values, with subsets represented as sorted vectors or tuples. However, note that since the subsets of $\{1, \ldots, N\}$ correspond bijectively to integers in $\{0, \ldots, 2^N-1\}$ via their binary representation (where bit $i$ indicates whether element $i$ is in the subset), we can use a simple array of length $2^N$ for memoization instead. This eliminates the overhead of hashing and dictionary lookups, and significantly reduces memory allocation costs.

This approach to dynamic programming simultaneously computes the probabilities for all ranks $k$ from 1 to $N$ in a single pass, and in doing so, has complexity that is independent of $k$. This is unlike the direct method which targets a specific rank, with complexity varying dramatically with $k$ (from $O(1)$ for $k=1$ to $O(2^{3N/2}\sqrt{N})$ for $k=N/2$). It follows that for single small values of $k$ (or large values close to $N$), the direct method is likely to be faster, while for moderate values of $k$ near $N/2$ or multiple ranks required, the DP approach will be more efficient (although you will be limited by memory constraints for large $N$).

In the final section of this post, I discuss some exploratory work in modifying the DP approach for the single target rank case, and using pruning to reduce the state space.

We implement this DP approach using the efficient bit-masking technique below:

```julia
function prob_x1_kth_position(lambdas::Vector{Float64}, k::Int)
    n = length(lambdas)
    # memo[bitmask, target_k] = probability
    memo = fill(-1.0, 2^n, n)  # -1.0 indicates not yet computed

    # Full set bitmask: all bits set
    full_mask = (1 << n) - 1
    result = dp(full_mask, k, lambdas, memo, n)
    return result, memo
end

function dp(mask::Int, target_k::Int,
    lambdas::Vector{Float64},
    memo::Matrix{Float64},
    n::Int)
    # Count number of elements in the set
    set_size = count_ones(mask)

    # Base cases
    if set_size == 1 && target_k == 1
        return 1.0
    end
    if target_k <= 0 || target_k > set_size
        return 0.0
    end

    # Check memoization
    if memo[mask+1, target_k] >= 0.0  # +1 for 1-based indexing
        return memo[mask+1, target_k]
    end

    result = 0.0
    lambda_sum = 0.0

    # Calculate lambda_sum for elements in the mask
    for i in 1:n
        if (mask & (1 << (i - 1))) != 0
            lambda_sum += lambdas[i]
        end
    end

    # Case 1: X₁ (index 1) is the minimum
    if (mask & 1) != 0 && target_k == 1  # Check if bit 0 is set (element 1)
        result += lambdas[1] / lambda_sum
    end

    # Case 2: Some other variable Xⱼ is the minimum
    for j in 1:n
        if (mask & (1 << (j - 1))) != 0 && j != 1  # j is in the set and j != 1
            new_mask = mask & ~(1 << (j - 1))  # Remove element j
            result += (lambdas[j] / lambda_sum) * dp(new_mask, target_k - 1, lambdas, memo, n)
        end
    end

    # Store result in memo
    memo[mask+1, target_k] = result
    return result
end
```

## Extensions

To wrap up, I'll briefly describe two extensions to the above methods that I've spent a bit of time exploring, but haven't fully worked through yet. Proceed with caution, but the general ideas should be solid.

### Repeated Rate Parameters

When multiple variables share the same rate parameter, the problem structure simplifies due to exchangeability. Suppose the $N$ variables are partitioned into $G$ groups, where group $g$ contains $n_g$ variables all with rate $\lambda_g$. Without loss of generality, assume $X_1$ belongs to group 1. Within each group, the variables are exchangeable, so we need only track how many variables from each group remain, rather than tracking individual variables.

We define a state vector $\mathbf{r} = (r_1, \ldots, r_G)$ where $r_1$ counts the number of other variables in group 1 (excluding $X_1$ itself), and $r_g$ for $g \geq 2$ counts the number of remaining variables in group $g$. The target variable $X_1$ is tracked separately. The total instantaneous rate when all variables in state $\mathbf{r}$ are present (including $X_1$) is:

$$S(\mathbf{r}) = \lambda_1(r_1 + 1) + \sum_{g=2}^{G} \lambda_g r_g$$

The $+1$ term accounts for $X_1$ itself. Let $F(\mathbf{r}, k)$ denote the probability that $X_1$ ranks $k$th given the current state $\mathbf{r}$. The base case is:

$$F(\mathbf{r}, 1) = \frac{\lambda_1}{S(\mathbf{r})}$$

For $k \geq 2$, we condition on which variable is the next to arrive (i.e., the minimum). If one of the $r_1$ other variables from group 1 arrives next, this occurs with probability $\lambda_1 r_1 / S(\mathbf{r})$, and we transition to state $\mathbf{r} - \mathbf{e}_1$ (where $\mathbf{e}_1$ is the unit vector in the first coordinate). Similarly, if a variable from group $g \geq 2$ arrives next, this occurs with probability $\lambda_g r_g / S(\mathbf{r})$. The recurrence is:

$$F(\mathbf{r}, k) = \sum_{g=1}^{G} \frac{\lambda_g r_g'}{S(\mathbf{r})} F(\mathbf{r} - \mathbf{e}_g, k-1)$$

where $r_1' = r_1$ (the other members of group 1) and $r_g' = r_g$ for $g \geq 2$.

The advantage of this formulation is that the state space has size $\prod_{g=1}^{G} (n_g + 1)$, which is polynomial in $N$ when $G$ is fixed. For example, with two groups of sizes $n_1$ and $n_2$, the state space has size $O(n_1 n_2) = O(N^2)$, vastly smaller than the $O(2^N)$ states in the general case. This makes problems with repeated rates dramatically more tractable.

### Single Rank Memory Optimization

The DP implementation presented in Section 3 uses a two-dimensional memoization table storing $(R, k)$ pairs, requiring $O(2^N \cdot N)$ space. This is appropriate when computing probabilities for multiple rank values, but when we only need a single specific rank $k$, we can reduce the memory footprint to $O(2^N)$ by using a one-dimensional table indexed only by $R$.

The observation is that for a fixed target rank $k_{\text{target}}$, the rank query associated with each subset during the recursion is uniquely determined by the subset size. If we start with $N$ variables and want $X_1$ to rank $k_{\text{target}}$-th, then when we have a subset $R$ of size $m$ remaining, we must be querying whether $X_1$ ranks $(k_{\text{target}} - (N - m))$-th among those $m$ variables. In other words, the rank decreases by exactly one each time we remove a variable from the recursion, so given the initial target rank and the current subset, the rank being computed is implicit.

This means we can use a single array `memo[mask]` rather than a matrix `memo[mask, k]`, reducing memory requirements by a factor of $N$. The downside is that this optimization only benefits single-rank queries—if we want probabilities for multiple values of $k$, we would need to recompute the table for each one.

### Pruned Dynamic Programming

When we are only interested in the probability for a single specific value of $k$, particularly when $k$ is small (or close to $N$), the standard DP approach does substantial unnecessary work. The issue is that the memoization table stores results for all possible rank values across all subsets, even though many of these will never be queried when computing $P(\{1,\ldots,N\}, k)$ for a specific $k$.

We can improve efficiency by pruning branches of the recursion that cannot possibly contribute to the target rank. The key observation is that if we have already removed too many variables (recursed too deeply), it becomes impossible to reach the target rank. Let $d = N - |R|$ denote the current depth (number of variables already removed). For $X_1$ to end up in position $k$ overall, we need $d + k$ to equal $k$ when $X_1$ is selected. If the current state has $d + k > k_{\text{target}} + 1$, then even if $X_1$ were selected immediately as the next minimum, it would be in position $d + 1 > k_{\text{target}}$, so this branch can be pruned.

Additionally, we can modify the memoization structure to avoid storing results for all rank values. Rather than maintaining a full table of $(R, k)$ pairs, we only compute and memoize states that lie on paths from the initial state $(\{1, \ldots, N\}, k_{\text{target}})$ to valid base cases. This can be implemented by checking, before recursing, whether the recursive call could possibly contribute to reaching the target rank.

In practice, this bounded DP approach substantially reduces both time and space requirements, particularly when $k$ is small (or close to $N$, by symmetry). The asymptotic worst-case complexity remains $O(2^N)$ when $k = N/2$, but the constant factors improve considerably. For small values of $k$, the pruned search tree can be exponentially smaller, often making the bounded DP competitive with or even faster than the direct summation method, while still maintaining the DP's flexibility for handling multiple queries.
