---
title: "Efficiently Solving a Google Coding Interview Question Using Pure Mathematics"
date: '2019-01-15'
excerpt: "Pure mathematics can get a bad reputation at times for being too abstract, and losing relevance to the real world. I think this reputation is largely unjustified and so, in this post, I show how a knowledge of the pure mathematical topics of linear algebra and combinatorics led me to a blazingly fast, and devilishly simple solution to a Google coding interview question."
thumbnail: /gallery/thumbnails/google-interview-question.jpg
toc: true
categories:
- [Computer Science, Coding Problems]
tags:
- linear-algebra
- combinatorics
- problem-solving
---



{% codeblock lang:python %}
%precision 0
{% endcodeblock %}






    '%.0f'



## The Knight's Dialler

Recently, I have become more and more interested in the sort of coding problems that are typically used in job interviews for developer and software engineering roles. In particular, whilst browsing [Glassdoor](https://www.glassdoor.co.uk/), I came across an interview question previously used by Google called 'The Knight's Dialler'.

### The Problem Statement

The problem goes as follows: You place a knight chess piece on one of the 10 digits of a standard mobile phone keypad (shown below). You then move it arbitrarily in the typical 'L'-shaped patterns to any other number on the keypad. For example, if you were on the 1 key, you would be able to move to either the 6 or 8 key. All keys except the 5 leave you with a possible new key to jump to. Suppose that as you make the knight hop around, every new key it lands on is dialled (i.e. we do not dial the key it starts on), generating a sequence of integers. The question is: given a specific starting point on the keypad and a fixed number of moves, how many possible distinct numbers can be dialled? 
![The standard mobile phone keypad](/images/google-interview-question/keypad.jpg)
This is a great interview question! It is simple to explain; it is very open, allowing many different approaches to the problem; and – although the problem requires some thought to solve – the actual coded solutions are rather short.

### A Typical Solution

After looking at many of the submitted solutions to this problem on Glassdoor and various coding-puzzle forums, I noticed that a common approach to this involved some sort of recursion. The fact that most people jump to this method makes complete sense; the problem has a very recursive nature to it. If, for a given starting point, you know the number of possible sequences that you can dial in $n-1$ steps, then all you have to do is enumerate these with the possible choices for the $n$th step and you have your solution. 

The issue with this sort of method is that recursion can often lead to exponential-time algorithms. That is, algorithms whose runtime varies in-line with the exponential of one of the inputs (in this case, the number of allowed moves). This means that for large inputs, your algorithm will be unusable and so we should avoid this scenario if possible. 

Furthermore, unless you are careful with the details of your implementation, it is easy for the required amount of storage to grow with input size, another trait which is undesirable in algorithms. 

There are some approaches that avoid these issues. One of which is a dynamic programming approach, shown [here](https://leetcode.com/problems/knight-dialer/solution/). This runs in linear-time and uses constant memory, making it a strong solution. My only issue with this method is that its validity didn't immediately jump out to me. The internal logic is obscured by a series of nested loops and confusing temporary variables. 

These inefficient or confusing solutions are what made the interview question so interesting to me. Especially because, due to my mathematical background, I almost instantly saw how it could be solved using a solution that is both linear and constant in memory, as with the DP approach. What allowed me to quickly leap to this efficient solution was my knowledge of elementary linear algebra and combinatorics. In fact, this problem translates perfectly into these two fields, leading to a very refined and simplistic solution.

## A Mathematical Approach

I will explain the thought process behind my solution soon, but will begin by revealing the code (written in Python) so it can be used as a reference later.

### The Final Code, First



{% codeblock lang:python %}
import numpy as np

def count_numbers(start = 0, moves = 0):
  # adjacency matrix for the implied network
  adj_mtrx = np.matrix([
    [0,0,0,0,1,0,1,0,0,0],
    [0,0,0,0,0,0,1,0,1,0],
    [0,0,0,0,0,0,0,1,0,1],
    [0,0,0,0,1,0,0,0,1,0],
    [1,0,0,1,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,1,0,0],
    [0,0,1,0,0,0,1,0,0,0],
    [0,1,0,1,0,0,0,0,0,0],
    [0,0,1,0,1,0,0,0,0,0]
  ])
  
  # eigen-decomposition
  e, v = np.linalg.eig(adj_mtrx)
  
  # compute powers of diagonals
  e_power = np.diag(e ** moves)
  
  # compute number of full-length paths
  all_paths = np.matmul(np.matmul(v, e_power), np.transpose(v))
  
  # compute number of paths starting from the initial key
  num_paths = np.matmul(all_paths, [[1]] * 10)[start]
  
  # convert to scalar and return
  return(np.asscalar(num_paths))
{% endcodeblock %}



Short and sweet, but does it actually work? Let's test it on a few cases. First, we know that if we start the knight on the 5 key then we should never be able to move, so can't dial any digits. 



{% codeblock lang:python %}
count_numbers(start = 5, moves = 42)
{% endcodeblock %}






    0



Zero! Just as we expected. For one more test, we can look at the number of sequences that we can dial in a small number of moves.



{% codeblock lang:python %}
count_numbers(start = 1, moves = 3)
{% endcodeblock %}






    10



This gives 10 possible sequences. Getting out pen and paper will show us that this is in fact the correct amount. The possible sequences are:

- 1 -> 6 -> 1 -> 6
- 1 -> 6 -> 1 -> 8
- 1 -> 6 -> 7 -> 2
- 1 -> 6 -> 7 -> 6
- 1 -> 6 -> 0 -> 6
- 1 -> 6 -> 0 -> 2
- 1 -> 8 -> 1 -> 8
- 1 -> 8 -> 1 -> 6
- 1 -> 8 -> 2 -> 4
- 1 -> 8 -> 2 -> 8

Lastly, just to satiate curiosity, we can run the function for a large number of moves.



{% codeblock lang:python %}
print(count_numbers(start = 4, moves = 90))
{% endcodeblock %}



    2.6529416969833432e+32
    

As we can see, these numbers grow rapidly with the number of allowed moves. For example, the value computed above is larger than the estimated number of bacterial cells on Earth – so do forgive me if I don't check this one by hand.

To further validate my method, I compared my results to the solution given by the original Google interviewer who introduced the question and we obtained the exact same values.

### My Thought Process

So how does this method work? And, more importantly, how did I come up with this?

My initial insight towards the problem was that the movements of the knight can be abstracted away to the connections between the nodes of a network graph. Abstraction is a very common technique in mathematical problem-solving, in which you remove anything but the bare mathematical structures. The keys can be replaced by labelled nodes and the possible moves of the knight can be replaced by arcs. For example, since the knight can move from the 1 key to the the 6 key, we would have an arc between nodes 1 and 6. We would not have an arc between 1 and 2 however, since this is not a valid move for the knight. This gives us the following graph.
![A graph representation of the Knight's Dialler Problem](/images/google-interview-question/graph.jpg)
This graph completely captures all of the information about the problem. The only issue is, this picture is not currently in a computer readable form. There are many ways of storing graphs but the most common way in mathematics is to use an adjacency matrix. This is an $n\times n$ matrix (where $n$ is the number of vertices of the graph) where the cell in the $i$th row and $j$th column is 1 if nodes $i$ and $j$ are connected by an arc and 0 otherwise. Mathematicians favour this representation since it allows us to use all of the techniques we have developed in linear algebra – as we will see later in this post. The adjacency matrix for the above graph (which we will call $A$) will look like this.

$$A = 
\begin{pmatrix}
0 & 0 & 0 & 0 & 1 & 0 & 1 & 0 & 0 & 0 \\\\
0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 1 & 0 \\\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 1 \\\\
0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 \\\\
1 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 1 \\\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\\\
1 & 1 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\\\
0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\\\
0 & 1 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\\\
0 & 0 & 1 & 0 & 1 & 0 & 0 & 0 & 0 & 0 
\end{pmatrix}
$$

As you can see, we have a 1 at the intersection of the 0th row and 4th column since nodes 0 and 4 are connected. Also it is worth noting that since our graph is undirected – that is whenever you can go from one node to another, you can always come back in the opposite direction – our adjacency matrix is symmetric ($A^T=A$ in linear-algebraic terms).

If you look at the final code again, you'll find that the first line is simply just defining this matrix. 

Now that we have our graph in a form both friendly for computers and mathematicians alike, we can use a clever theorem from combinatorics to extract some useful information from our matrix. In particular, we use the result that the element in the $i$th row and $j$th column of the matrix $A^k$, for some natural number $k$, gives us the number of distinct paths from node $i$ to node $j$ of length $k$. 

That's a really interesting result, but what's its relevance to us? It may not seem clear at first, but in fact, knowing this gives the whole game away, providing us with an instant route to the problem's solution. This is because every possible sequence of dialled numbers corresponds exactly with one path through the network. And so, if we know how many paths there are from any starting point to any end point – which we obtain from our exponentiated adjacency matrix – we can simply sum up the values of interest to get our result.

Specifically, since we want to know the number of paths from a given starting point, we will want to sum over all of the columns of $A^k$ for a fixed row. If we recall how we compute matrix multiplications, it is not too hard to see that in order to get the sum across the $i$th row, we simply multiply $A^k$ by a column vector of length 10 containing only the value 1 and then extract the $i$th component of the resulting column vector. If you are sceptical of this, give it a go with a small arbitrary matrix to convince yourself. 

So that's it, we're done! This is a completely valid solution to the problem. It is incredibly simple; only requiring 3 lines of code - one of which is just defining the matrix. This solution is not perfect however. This approach is limited by the slow computation of $A^k$. Multiplying $10\times 10$ matrices is not a quick process and doing it $k-1$ times for large $k$ could take a long time. 

Using some knowledge of linear algebra, however, it is possible to speed up this method up with only a few more lines of code necessary.

### Turbo-charging Our Solution

The next idea that came to me was to use a technique known as eigen-decomposition to make computing the powers of $A$ more efficient. Recall that since our graph was undirected, our adjacency matrix $A$ will be symmetric. A well-known result in linear algebra lets us take advantage of this fact. It says that any symmetric matrix, such as $A$, can be decomposed in the following way.

$$A = P^TDP$$

where $D$ is a diagonal matrix – it is zero everywhere but the main diagonal – and $P$ is orthogonal – that is that $P^TP=PP^T=I$, where $I$ is the identity matrix. The proof of this is quite long-winded and mundane, using induction on the size of the matrix, but the result is incredibly powerful. One use of this is in computing powers of $A$. We simply have to observe that

$$
\begin{align*}
A^k &= \underbrace{A\cdot A\cdot\ldots\cdot A}_{k\text{-times}} \\\\
&= \underbrace{(P^TDP) \cdot (P^TDP)\cdot\ldots\cdot (P^TDP)}_{k\text{-times}} \\\\
&= P^T \cdot \underbrace{(DPP^T) \cdot (DPP^T)\cdot\ldots\cdot (DPP^T)}_{(k-1)\text{-times}}\cdot DP \\\\
&= P^T \cdot \underbrace{D \cdot D\cdot\ldots\cdot D}_{(k-1)\text{-times}}\cdot DP \\\\
&= P^TD^kP
\end{align*}$$

since all of the $P$'s and $P^T$'s on the inside of the product cancel out to give $I$ by orthogonality. We have now reduced the problem of exponentiating $A$ to exponentiating a diagonal matrix $D$. This may feel like we're going in circles, but that is not the case. Exponentiating a diagonal matrix – unlike a general matrix – is incredibly simple. All you have to do is exponent the individual elements, and since the majority of these are zero, this is very easy to do. After computing $D^k$ all that is left to do is compute $A^k=P^TD^kP$ – a computationally easy task – and carry on as described in the last section.

With this knowledge in hand, it shouldn't be too hard to piece together how the lines of the code above correspond to the steps of this method. Even with this new time-saving addition, our code still requires only 6 lines. I am yet to see any purely computer-science approach to this problem that is as short, simplistic, and elegant as this.

{% colorquote info %}
Because of the way eigen-decomposition behaves in `numpy`, the `v` that is returned to us is equivalent to $P^T$ above.
{% endcolorquote %}


### Time-complexity Analysis

Before we wrap up, we should take a quick theoretical look at how quickly our algorithm runs. We first look at the eigen-decomposition. In practice, calculating eigenvalues/vectors of an $n\times n$ matrix requires $O(n^3)$ time. There are algorithms such as Coppersmith and Winograd which compute these in $O(n^\omega)$ with $2< \omega < 3$, but due to the complexity of implementing code for these for little computational gain in most circumstances, they are rarely used. Since our matrix is of fixed size however, this part of the code is simply $O(1)$ time. The only other part of the code worth considering is the computation of $D^k$. This will involve exponentiating 10 numbers $k$ times each and so will run in $O(k)$ time. Hence our algorithm is linear, exactly the same as the dynamic programming approach but, I would argue, far more beautiful. 
