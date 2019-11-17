---
title: "Maths Matters: Bouncy Numbers"
date: '2019-10-19'
excerpt: "When we get swept up by the data science craze, it is often all too easy to forget the importance of pure mathematics and statistics, in place of flashy new algorithms and machine learning models. As a reminder of the power of pure mathematics, this post discusses how I used a moderate knowledge of combinatorics to solve a challenging ProjectEuler+ problem with only 4 essential lines of code."
thumbnail: /gallery/thumbnails/bouncy-numbers.jpg
toc: true
categories:
- [Computer Science, Coding Problems]
tags:
- combinatorics
- problem-solving
---

{% colorquote warning %}
This blog post will contain a solution to problem #113 (non-bouncy numbers) of ProjectEuler+ which will in turn provide a substantial hint for problem #112 (bouncy numbers). 
{% endcolorquote %}

 
Almost a year ago now I wrote a blog post titled [Efficiently Solving a Google Coding Interview Question Using Pure Mathematics](/google-interview-question/). In it, I discuss how I had used techniques from pure mathematical fields such as combinatorics and linear algebra, to find a solution to a typical Google interview problem that was simple, efficient, and impressively short. 

Today's post could easily be described as the spiritual successor to the former. We will tackle a new problem, this time from [ProjectEuler+](https://www.hackerrank.com/contests/projecteuler/challenges) ([HackerRank](https://www.hackerrank.com)'s take on the original [ProjectEuler](https://projecteuler.net/)). The exact techniques we use will certainly differ but the overall style and structure will be the same. More importantly, so will the take-away message: maths matters!

## Bouncy Numbers

The problem that we will be looking at involves a definition of what makes a number bouncy, or more importantly _not_ bouncy. We will be concerned with counting how many non-bouncy numbers there are less than a given power of ten.

The best place to start is by defining what exactly a bouncy number is.

### The Problem Statement

The specific problem that we will be looking at is #113 - non-bouncy numbers. The original problem statement can be found [here](https://www.hackerrank.com/contests/projecteuler/challenges/euler113/problem) but I will summarise below.

We say that a number is increasing if no digit is exceeded by the digit to its left. For example, 123 and 445 are both increasing numbers but 687 isn't. We have a similar definition for decreasing numbers in which no digit is exceed by the digit to its right.

We call any positive integer that is neither increasing nor decreasing a bouncy number. The crux of the question is simply-stated: how many positive integers below $10^k$ are _not_ bouncy?

{% colorquote info %}
These answers grow large with $k$ and so the original problem adds that the answer should be printed modulo $(10^9 + 7)$ but we will ignore this for simplicity.
{% endcolorquote %}

 
### A Typical Solution

This problem stood out to me as it seemed to have a surprisingly low success rate of around 50% for what to me seemed like a straight-forward problem. The reason for this disparity is that my initial approach to the problem took a vastly different line of attack to most, judging by the problem discussion board.

It appears that most competitors tried to tackle the problem using either brute force (good luck) or dynamic programming. The issue is, that due to the large number of test cases and range of $k$ (up to $10^5$) any brute force approach, and all but the most efficient dynamic programming solutions, will ending up using more than the allowable code execution time.

My solution differs in that there is no recursion, no iteration, and no enumeration; in fact there's not really any code at all. Why? Because my experience with combinatorics led me to know a closed form for the solution.

## A Mathematical Approach

Before we get into the nitty-gritty mathematics, lets take a look at the code for my solution (written in Python). The input format for the problem is first an integer $t$ giving the number of test cases, followed by $t$ lines each containing a different value of $k$. The output format is then $t$ lines, each containing the number of non-bouncy numbers less than $10^k$.

### The Final Code, First

{% codeblock lang:python %}
from functools import reduce 

# define combinatorial choose function
def nCr(n,k):
    numer = reduce(lambda x, y: x * y, list(range(n, n - k, -1)))
    denom = reduce(lambda x, y: x * y, list(range(1, k + 1)))
    return numer // denom

for _ in range(int(input())):
    k = int(input())
    num_increasing = nCr(k + 9, 9) - 1
    num_decreasing = nCr(k + 10, 10) - (k + 1)
    num_both = 9 * k
    num_not_bouncy = num_inc + num_dec - num_bth
    print(num_not_bouncy)
{% endcodeblock %}


This code passes all visible and hidden test cases for the problem in barely any time.

The first section of the code—importing `functools.reduce` and defining `nCr(n,k)`—isn't actually part of the general problem-solving logic. They simply make up for the lack of base mathematical functionality in Python by manually adding definitions. In all, only the four lines starting `num_{something} = ` are essential for solving the problem, the rest is just boilerplate code.

These four lines carry a lot of power. Before we piece them together though, we will have to have a quick review of elementary combinatorics.

### My Thought Process

#### Elementary Combinatorics

{% colorquote info %}
If you feel like you have a good grasp of basic combinatorics including the definition of $n \choose k$ and knowledge of the principle of bijections, this section will not teach you anything new so I advise that you skip over it.
{% endcolorquote %}

 
Combinatorics is a vast field of mathematics but we will only need to take a short glance at a specific area. In particular, we will be looking at the function denoted by

$$n\choose k$$

which we pronounce as _n choose k_. 

This function gives the number of ways of selecting $k$ objects out of $n$ distinguishable choices. For example if we to form a team of 5 out of a class of 30 pupils, we would be able to do this in ${30 \choose 5}$ unique ways.

That's nice and all, but just defining a notation for a concept doesn't get us very far. The important point is that we have a formula for $n\choose k$ which lets us calculate it simply and efficiently for any reasonable $n$ and $k$. The formula is as follows:

$${n\choose k} = \frac{n!}{k!(n-k)!} = \frac{n \cdot (n-1) \cdot \ldots \cdot (n - k + 2) \cdot (n - k + 1)}{k \cdot (k-1) \cdot \ldots \cdot 2 \cdot 1}$$

This is exactly what that first block of code in our solution is for. It sets up the function to compute $n \choose k$ for any positive integers $0 \leq k \leq n$. This doesn't contribute to the overall logic of the solution but is necessary component to the required computations.

<hr>

Before we get on to exactly into how my solution works, we will need to take a quick detour to learn about the principle of bijections. This is best illustrated with a motivating example.

Suppose that you have a handful of apples and oranges and you want to know whether you have the same quantity of each fruit. The obvious way to check this is to count how many of each fruit you have and then compare these two numbers to check for equality. 

Let's consider this problem again but now with two large crates, each full of apples and oranges respectively. Counting is now a risky endeavour; how can we be sure that we don't lose count or accidentally miss a piece of fruit? A more robust solution would be to pair the apples and oranges up until we either run out of both fruits at the same time - in which case the original quantities of each fruit were the same - or there is one type of fruit left over - and so the original numbers were not equal.

This notation is abstracted in the field of combinatorics (and maths at large) to what is known as the principle of bijections. This states that whenever we can form a one-to-one correspondence (also known as a bijection, hence the name) between two sets, they are of the same size. This principle will come in handy in just a few moments.

#### Application to the Problem

With preliminaries out of the way, we can proceed to solve to the problem. We split our approach into four parts:

1) Calculate the number of increasing numbers less than $10^k$

2) Calculate the number of decreasing numbers less than $10^k$

3) Calculate the number of numbers less than $10^k$ that are both increasing and decreasing

4) Compute the number of bouncy numbers less than $10^k$ using the above three values

It turns out that each of these can each be completed in just a single line of code involving the `nCr(n, k)` function we defined earlier. We will break down each step one at a time.

#### Step 1

We start by counting the number of increasing numbers less than $10^k$. As a reminder, we include both strictly increasing (e.g. $123$) and weakly increasing (e.g. $455$) in our general definition of increasing numbers.

Counting these directly is rather difficult but we can introduce a clever one-to-one correspondence to make this task much easier. We will define the mapping as follows:

* Given an increasing positive integer less than $10^k$, write it in the form $d_1d_2\ldots d\_k$ where $d_1 \ldots d\_k$ are digits between 0 and 9 to be concatenated
* Since the given number was increasing we have $0 \leq d_1 \leq d_2 \leq \ldots \leq d\_k \leq 9$
* We map this integer to a sequence of stars (\*) and bars (|) such that each star corresponds to the digits $d_1\ldots d\_k$
* Further we set the number of bars between the $i$th and $(i+1)$th star to be equal $d_{i+1} - d\_{i}$
* Lastly we place a number of bars equal to $d\_1$ at the start of the sequence and $9 - d\_k$ at the end

They may seem like a highly opaque definition but hopefully the inclusion of an example will add clarity. 

First we look at the number $457$ when $k=5$. Since we are considering five digits, we write this as 00457. We start with our 5 stars:

$$\*\*\*\*\*$$

Our first digit is $0$ so we don't place any bars at the start. Likewise our second digit is $0$ and so as there was no increase, we do not insert a bar. Between the second and third digit however we have an increase of $4$ so we insert that many bars there to get:

$$\*\*||||\*\*\*$$

Carrying on, we have a jump of $1$ between the third and fourth digit and $2$ between the fourth and last so we add the corresponding number of bars to the diagram:

$$\*\*||||\*|\*||\*$$

Finally, we add two bars to the end of the sequence since $7$ is two short of $9$. This leaves us with:

$$\*\*||||\*|\*||\*||$$

Notice that we can convert these sequence representations back by reversing our rules. For example the sequence,

$$||\*\*|\*\*|\*|||||$$

corresponds to the increasing number $22334$.

Notice that in general we will have $k$ stars and 9 bars. The reason for the latter is perhaps less apparent. It follows from the way we defined the number of bars between each of the digits and at the end. The number at the start was $d\_1$. Then we had $d_2-d\_1$ between the first pair, and $d_3-d\_2$ between the next. We continue this until there are $d_k - d\_{k-1}$ between the last pair. Lastly, we add $9-d\_k$ bars to the end. So in total we have

$$d_1 + (d_2 - d_1) + (d_3 - d_2) + \ldots (d_k - d_{k-1}) + (9-d_k) = 9$$

bars.

Since mappings are unique in both the forwards and backwards direction (try working backwards from the stars and bars above to the original number), we have a one-to-one correspondence. It follows from the principle of bijections that the number of increasing numbers less than $10^k$ is exactly equal to the number of ways of creating a sequence of $k$ stars and $9$ bars.

The end is now in sight. The last step is to notice that the number of ways of arranging $k$ stars and $9$ bars is the same as the number of ways of picking $9$ objects from a choice of $k+9$. Why is this? Well suppose that we have $k+9$ spaces which can each be filled with either a star or a bar:

$$\underbrace{\\\_\\\,\\\_\\\,\\\_\ldots\\\_\\\,\\\_\\\,\\\_}_{k+9}$$

We then pick $9$ of these to fill with the 9 bars we have available. Then the remaining $k$ spaces are forced to be stars. Since the choice of spaces to fill with bars uniquely determines the sequence of stars and bars, and vice-versa, these represent the same process.

Finally, remember from our definition of $n \choose k$ is the number of ways of choosing k elements from a selection of n objects. Well that is exactly what we have done here, but choosing $9$ objects from $k+9$ instead. 

There are therefore

$${k+9} \choose 9$$

ways to create such sequences of stars and bars, and so using the principle of bijections, this is exactly how many increasing numbers less than $10^k$ we have.

A small tweak remaining is just to subtract $1$ from the result since the problem specifically concerns _positive_ integers. With this addition made we are left with the first 'proper' line of code in my solution:

{% codeblock lang:python %}
num_increasing = nCr(k + 9, 9) - 1
{% endcodeblock %}


#### Step 2

This next step is very similar to the last but with a minor change. This is since, with decreasing numbers, we are allowed to have zeros both at the start and end of the number (the leading zeros being used to pad the number to have $k$ digits).

We use the same numbers of stars as before but add an extra bar. We also decide on the number of bars between each star in a slightly altered way. This is harder to describe algebraically so instead we use the rule that for each additional bar, our next star progresses one place in the following sequence

$${0,9,8,\ldots,1,0}$$

This is highly analogous to the previous method so I won't go into additional examples though I encourage the reader to try one out for themselves.

The important point is that we are now arranging $k$ stars and $10$ bars. In a similar way to before we find that this can be done in

$${k+10} \choose 10$$

ways.

We must make a similar correction to before. This time, however, we subtract $k+1$ rather $1$. This is because we have $k+1$ unique representations of zero, show below.

$$\underbrace{\*\*\*\ldots\*\*\*}_{k}||||||||||$$

$$\underbrace{\*\*\*\ldots\*\*\*}_{k-1}||||||||||\*$$

$$\vdots$$

$$\*||||||||||\underbrace{\*\*\*\ldots\*\*\*}_{k-1}$$

$$||||||||||\underbrace{\*\*\*\ldots\*\*\*}_{k}$$

This leaves us with the second essential line of code:

{% codeblock lang:python %}
num_increasing = nCr(k + 10, 10) - (k + 1)
{% endcodeblock %}


#### Step 3

Thankfully this step is much simpler than the last two. We introduce this to prevent double-counting numbers that are both increasing and decreasing. The only numbers satisfying both these properties are those made of a single digit.

It is not hard to show that there are $9 \cdot k$ ways to do this. Indeed, there are $9$ digits that can choose from and then we can repeat it one of $1, 2, \ldots, k$ times (i.e. $k$ different ways). 

This leads us to the third line of the main body of the code:

{% codeblock lang:python %}
num_both = 9 * k
{% endcodeblock %}


#### Step 4

To round everything up will simply note that the number of non-bouncy integers less than $10^k$, which by definition is the number of integers less than $10^k$ that are neither increasing nor decreasing, is equal the number of integers less than $10^k$ that are increasing plus the number that are decreasing subtract the number that are both increasing and decreasing.

This gives rise to the final important line of code:

{% codeblock lang:python %}
num_not_bouncy = num_inc + num_dec - num_bth
{% endcodeblock %}


With this, we can draw a close to this post. Before we do though, I would like to emphasise the importance of pure mathematics in this solution. Without a reasonable knowledge of combinatorics, coming up with this solution would have been highly unlikely and so one may have been forced to resort to more complicated or inefficient methods. 

Some would argue that this approach seems far more confusing than a dynamic programming approach and I understand that train of thought. At first glance, this solution seems incredibly involved and time-consuming to produce. I argue though, that with practice of pure mathematics—and, in particular, combinatorics—this sort of problem-solving becomes second nature, allowing you to tackle challenges of this sort after only a few seconds of contemplation.
