---
title: "Binomial Recursion"
date: '2018-10-17'
excerpt: "In this post, we take a simple coin-flipping puzzle and through scope-expansion and generalisation, turn it into a monster probability problem that we can be proud to have tackled. In it, we look at some clever techiques for calculating probabilities which are vital in any experienced statistian's toolbox."
thumbnail: /gallery/thumbnails/binomial-recursion.jpg
toc: true
categories:
- [Statistics, Probability]
tags:
- binomial-distribution
- coins
- no-coding
- tutorial
---

## An Infinite Coin Problem

Imagine you have a coin, biased in such a way that it lands heads with probability $p \in [0,1)$ (we will require $p \neq 1$ later in the post) and tails with probability $1-p$. You start by flipping this coin $n \in \mathbb{N}^+$ times. Then, count how many heads you obtained in this series of flips and call this $x\_1$. Begin flipping again, but this time doing a total of $x\_1$ tosses. You count the heads and call the resulting value $x\_2$. You can probably see where this is going.

In general, on the $i$th set of coin flips, you perform $x\_{i-1}$ tosses and record the numberof heads as $x\_i$. You repeat this until eventually you get no heads in a series of flips. If this occurred on the $i$th turn, we'd then have $0 = x_k = x\_{x+1} = \ldots$. Formalising this, if we let $X\_i$ be the random variable representing the number of heads obtained on the $i$th series of tosses, then these random variables are defined by

$$ X_1 \sim B(n,p) \qquad X_{i+1} \sim B(X_{i}, p) \ \forall i \in \mathbb{N} $$

There are many questions we could ask about these random variables, which in turn relate to questions about the original scenario. A sensible question might be regarding the distribution of each $X\_i$, which will correspond to asking what the likelihood is of getting a particular number of heads on a certain series of tosses. We may also wish to know how many heads we expect to see in total for a given $n$ and $p$. This is equivalent to asking what the value of $\mathbb{E}\left( \sum_{k=1}^\infty X\_k \right)$ is.

## Handling a specific case

{% colorquote info %}
To keep the focus on the important parts of this problem, I have omitted defining any pmfs outside of their support. Therefore, if any value of the pmf is undefined, it can be assumed to be zero.
{% endcolorquote %}


We will start simple by finding the distribution of the random variable $X\_2$ and from there we can go about generalising this for any $X\_i$. To begin, we note that since $X\_1$ is binomially distributed with parameters $n$ and $p$, it will have a probability mass function given by

$$ \mathbb{P}(X_1=k) = {n \choose k}  p^k (1-p)^{n-k} \qquad k \in [n] $$

We also know, given that $X\_1$ takes a particular value $k \in [n]$, that $X\_2$ will be distributed binomially with parameters $k$ and $p$ and so it will have the conditional probability mass function

$$ \mathbb{P}(X_2=l|X_1=k) = {k \choose l} p^l(1-p)^{k-l} \qquad l \in [k] $$

Combining these and using the definition of conditional probability we can construct the joint pdf 

$$
\begin{align}
\mathbb{P}(X_1 = k, X_2=l)  & = \mathbb{P}(X_1=k)\cdot\mathbb{P}(X_2=l|X_1=k) \\\\
& = {n \choose k}p^k(1-p)^{n-k} \cdot {k \choose l} p^l(1-p)^{k-l} \\\\
& = {n \choose k}  {k \choose l}  p^{k+l} (1-p)^{n-l} \qquad k,l \in [n],\  l\leq k
\end{align}
$$

This is a great position to be in as this function describes the entire combined behaviour of $X\_1$ and $X\_2$. To get the distribution of $X\_2$, all we have to do is fix $X\_2$ at a certain value and sum across all corresponding possible values for $X\_1$ in the support of the joint random variable. If we fix $X\_2$ to be $l \in [n]$ then we must have $l<X\_1$, and so we are required to sum across the values $l$ to $n$ as follows


$$
\begin{align}
\mathbb{P}(X_2 = l)  & = \sum_{k=l}^n \mathbb{P}(X_1 = k, X_2=l) \\\\
& = \sum_{k=l}^n {n \choose k}  {k \choose l}  p^{k+l} (1-p)^{n-l} \qquad l \in [n]
\end{align}
$$

We can now go about simplifying this sum. First we extract any parts of the summand that do not depend on the index, $k$

$$
\begin{align}
\mathbb{P}(X_2 = l) & = p^l (1-p)^{n-l} \sum_{k=l}^n {n \choose k}  {k \choose l}  p^{k} \qquad l \in [n]
\end{align}
$$

Next we use the change of variable: $m=k-l$. This gives us a sum starting from zero. We follow this with some algebraic manipulation

$$
\begin{align}
\mathbb{P}(X_2 = l) & = p^l (1-p)^{n-l} \sum_{m=0}^{n-l} {n \choose m+l}  {m+l \choose l}  p^{m+l} \\\\
 & = (p^2)^l (1-p)^{n-l} \sum_{m=0}^{n-l} {n \choose m+l}  {m+l \choose l}  p^{m} \\\\
  & = (p^2)^l (1-p)^{n-l} \sum_{m=0}^{n-l} \frac{n!}{(m+l)!(n-m-l)!} \frac{(m+l)!}{m!l!} p^{m} \\\\
& = (p^2)^l (1-p)^{n-l} \sum_{m=0}^{n-l} \frac{n!}{(m+l)!(n-m-l)!} \frac{(m+l)!}{m!l!} p^{m} \\\\
& = (p^2)^l (1-p)^{n-l} \sum_{m=0}^{n-l} \frac{n!}{(n-m-l))!m!l!} p^{m} \\\\
& = \frac{n!}{l!(n-l)!} (p^2)^l (1-p)^{n-l} \sum_{m=0}^{n-l} \frac{(n-l)!}{m!(n-m-l)!} p^{m} \\\\
& = {n \choose l} (p^2)^l (1-p)^{n-l} \sum_{m=0}^{n-l} {n-l\choose m} p^{m} \cdot 1^{(n-l)-m} \qquad l \in [n]
\end{align}
$$

Lastly, observe that the summand is actually just the binomial expansion of $(1+p)^{n-l}$ and so we get 

$$
\begin{align}
\mathbb{P}(X_2 = l) & = {n \choose l} (p^2)^l (1-p)^{n-l} (1+p)^{n-l} \\\\
\mathbb{P}(X_2 = l) & = {n \choose l} (p^2)^l (1-p^2)^{n-l} \qquad l \in [n]
\end{align}
$$

by the difference of two squares. The eager-eyed reader may notice that this is in fact the probability mass function of a binomial random variable with parameters $n$ and $p^2$ and hence $X\_2 \sim B(n,p^2)$. This leads us to conjecture that

$$X_i \sim B(n,p^i) \quad \forall i \in \mathbb{N}$$

This turns out to be completely true. What follows is a formal proof of this using induction and then a combinatorial argument which aims to reason why this is true in a less formal way.

## A Formal Proof of the General Case

We will proceed inductively on $i$. We see that the statement holds for $i=1,2$ so we have our base case covered comfortably. For our inductive hypothesis we suppose that $X\_{i-1} \sim B(n,p^i)$ and proceed from here to try and show that $X\_{i} \sim B(n,p^{i+1})$. We do this using the same method as for $X\_2$; first we calculate the joint probability mass function of $X\_i$ and $X\_{i}$ and then sum over all valid values of $X\_{i-1}$ for fixed $X\_{i} = l$ to get the marginal distribution of $X\_{i}$ which will hopefully correspond to a binomial random variable with parameters $n$ and $p^{i}$. First note that for all $k,l \in [n],\  l\leq k$ we have

$$
\begin{align}
\mathbb{P} \left(X_{i-1} = k, X_i = l \right) & =\mathbb{P} \left( X_{i-1} = k \right) \cdot \mathbb{P} \left( X_i = l| X_{i-1} = k \right)  \\\\
& = {k \choose l} p^l (1-p)^{k-l} \cdot {n \choose k} \left( p^{i-1} \right)^k \left( 1 - p^{i-1} \right)^{n - k}
\end{align}
$$

Which implies that

$$
\begin{align}
\mathbb{P} \left( X_n = i \right) & = \sum_{k=l}^n {k \choose l} {n \choose k} p^l (1-p)^{k-l}  \left( p^{i-1} \right)^k \left( 1 - p^{i-1} \right)^{n - k} \\\\
 & = p^l  \sum_{k=l}^n {k \choose l} {n \choose k} (1-p)^{k-l}  \left( p^{i-1} \right)^k \left( 1 - p^{i-1} \right)^{n - k} \\\\
\end{align}
$$

We then use the substitution $m=k-l$ to get
  
$$
\begin{align}
\mathbb{P} \left( X_n = i \right) & = p^l  \sum_{m=0}^{n-l} {m + l \choose l} {n \choose m + l} \left(1-p \right)^{m}  \left( p^{i-1} \right)^{m+l} \left( 1 - p^{i-1} \right)^{(n - l) - m} \\\\
 & = \left( p^i \right)^l  \sum_{m=0}^{n-l} {m + l \choose l} {n \choose m + l} \left(1-p \right)^{m}  \left( p^{i-1} \right)^{m} \left( 1 - p^{i-1} \right)^{(n - l) - m} \\\\
& = \left( p^i \right)^l  \sum_{m=0}^{n-l} \frac{(m+l)!  n!}{l!  m!  (m+l)!  ((n-l)-m)!} \left(1-p \right)^{m}  \left( p^{i-1} \right)^{m}  \left( 1 - p^{i-1} \right)^{(n - l) - m} \\\\
& = \left( p^i \right)^l  \sum_{m=0}^{n-l} \frac{n!}{l!  m!  ((n-l)-m)!} \left(1-p \right)^{m}  \left( p^{i-1} \right)^{m} \left( 1 - p^{i-1} \right)^{(n - l) - m} \\\\
& = \left( p^i \right)^l \frac{n!}{l!  (n-l)!}  \sum_{m=0}^{n-l} \frac{(n-l)!}{m!  ((n-l)-m)!} \left(1-p \right)^{m}  \left( p^{i-1} \right)^{m} \left( 1 - p^{i-1} \right)^{(n - l) - m} \\\\
& = \left( p^i \right)^l {n \choose l}  \sum_{m=0}^{n-l} {n-l \choose m} \left(1-p \right)^{m}  \left( p^{i-1} \right)^{m} \left( 1 - p^{i-1} \right)^{(n - l) - m} \\\\
& = \left( p^i \right)^l {n \choose l}  \sum_{m=0}^{n-l} {n-l \choose m} \left(p^{i-1}-p^i \right)^{m}  \left( 1 - p^{i-1} \right)^{(n - l) - m} \\\\
& = \left( p^i \right)^l {n \choose l} \left( p^{i-1} - p^i + 1 - p^{i-1} \right)^{n-l} \\\\
& = {n \choose l} \left( p^i \right)^l \left(1 - p^i \right)^{n-l} \\\\
\end{align}
$$

Since this last line is the probability mass function for a binomially distributed random variable with parameters $n$ and $p^i$, our induction is complete and so we can rest assured that our conjecture does hold for all $i \in \mathbb{N}$.

The jump from the third-to-last to penultimate step is probably the toughest and involves spotting that the summand is the binomial expansion of $((p^{i-1}-p^i)+(1-p^{i-1}))^{n-l}$. This may be somewhat difficult to notice in the forward direction but checking it in the reverse is a trivial matter of substituting the two expressions forming the binomial into the expansion formula. In fact, the whole proof may feel like it has an air of aimless wandering with the right results just popping out with little explanation to the logic behind the proof's direction. I would not argue at all with the analysis! The best way to understand the structure of this proof is to compare it to the specific case of finding the distribution of $X\_2$. The proofs are very similar but it is much clearer to follow the thought process behind the simpler case. 

## A Combinatorial Justification

For those readers who prefer an intuitive explanation of why a result is true more than a formal proof, I also offer a more combinatorial justification of proposition. To keep things simple, I will only focus on the first two random variables $X\_1$ and $X\_2$, though this result can easily be generalised inductively. 

The key insight to this explanation is noticing that the order of events involved in the problem can be changed without actually affecting the distributions of $X\_1$ and $X\_2$. A binomial random variable with parameters $n$ and $p$ is simply the sum of $n$ independent and identically distributed Bernoulli random variables with parameter $p$. We can treat Bernoulli random variables as drawing a ticket from a box in which all tickets either have the number 0 or 1 written on them, the proportion of which having 1 being $p$.

In the original statement of the problem if we have $X_1 = x\_1$ take on a specific value, this amounts to use drawing $n$ tickets from such a box mentioned above and counting that $x\_1$ have a 1 written on them. Then, if we have $X_2 = x\_2$ take on a specific value too, this equates to us performing a secondary follow-up experiment in which we draw $x\_1$ tickets from the box again and seeing that $x\_2$ of them have a 1 written on them.

We now frame this problem in a different way. We draw the $n$ tickets for $X\_1$ as before but now, rather than waiting till the end to see how many 1's we have, as soon as we draw a 1, we follow this up by drawing another ticket but for $X\_2$ instead. We can think of this procedure as actually just drawing one ticket from the box but with three possibilities for what can be written on it:

* $X\_1=0$. This value models drawing a zero for $X\_1$ and hence not drawing for $X\_2$.
* $X_1=1, X\_2 = 0$. This value models drawing a one for $X\_1$ but then getting a zero for $X\_2$.
* $X_1=1, X\_2 = 1$. This value models drawing a one for both $X\_1$ and $X\_2$.

We observe that these events occur with probability $(1-p)$, $p(1-p)$ and $p^2$ respectively. Since to have $X_2=x\_2$ all we care about is having $x\_2$ tickets out of the $n$ total be of the last type which occurs with probability $p^2$ each time, independent of any other ticket combination, we must have $X\_2 \sim B(n, p^2)$ as we expected.

## Finding The Expectation

Now that we know the distributions of each $X\_i$, computing the expectation of their sum isn't too tricky. We do have to be careful of convergence issues but since we restricted $p$ to be less than 1, we don't run into any issues. If $p$ is 1, it's clear that the coin-tossing goes on forever and so obviously don't have an expectation for the total number of heads. We will calculate this value my first using the linearity of expectation, then recalling that the expected value of a $B(n,p)$ random variable is $np$ and then using the formula for the closed for of an infinite geometric series, which will converge since $p<1$.

$$
\begin{align}
\mathbb{E}\left( \sum_{k=1}^\infty X_k \right) & = \sum_{k=1}^\infty \mathbb{E}(X_k) \\\\
& = \sum_{k=1}^\infty np^k \\\\
& = np \sum_{k=1}^\infty p^{k-1} \\\\
& = np \sum_{j=0}^\infty p^{j} \quad [j=k-l]\\\\
& = \frac{np}{1-p} \qquad p \in [0,1)
\end{align}
$$

Interestingly, this is exactly the number of tosses you perform on the first set of flips multiplied by the odds of getting a head.

## Final Comments

It is worth mentioning that, in fact, this proposition can be generalised further. We do this by letting $X_1 \sim B(n, p\_1)$ and defining $X_i \sim B(X_{i-1}, p\_i) \  \forall i \in \mathbb{N}$. Then it is true, similar to above that  
$$X_i \sim B \left( n, \prod_{k=1}^{i} p_k \right) \  \forall i \in \mathbb{N} $$
The proof is almost identical to the one given above just with some more notational complexity. The combinatorial justification can also easily be adapted to accommodate this change. I leave it to the eager reader to confirm the validity of this statement for themselves.
