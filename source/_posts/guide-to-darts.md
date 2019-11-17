---
title: "A Statistican's Guide to Playing Darts"
date: '2018-12-08'
excerpt: "Although the game of darts requires a tremendous amount of skill to be a good player, there is still a very large probabilistic element. In this post, we take undertake a stochastic analysis of the game in order to reach an optimum strategy for play depending on the typical accuarcy of your shots."
thumbnail: /gallery/thumbnails/guide-to-darts.png
toc: true
categories:
- [Statistics, Probability]
tags:
- animation
- sports
---




## Introduction

Darts is a game of incredible skill and precision. If however - like me - you lack the necessary coordination to shine at the sport, luck will have to suffice. Then, if things happen to go your way, all you are left to do is claim deliberateness. In fact, there is a truth to this for all players, newcomers and seasoned professionals alike. All abilities will have some natural variation between each throw giving rise to a probability distribution reflecting where the dart landed relative to where it was aimed. After all, no one is guaranteed to hit exactly where they wanted.

This raises the question, if you want to maximise your score in a given throw, where is it best to aim? We start with the extremes. If you were some sort of superhuman darts-ninja guaranteed to hit exactly where you aim, there is no doubt that you would simply aim for the treble 20 on every throw. Ultimately, it's the highest possible score you can get on the board and since you're certain to hit it if you try, it would be foolish to aim anywhere else. On the contrary, suppose you are a complete darts rookie, playing with your off-hand during a magnitude 7.6 earthquake. You'd be quite chuffed if you even managed to get it on the board, never mind what score you get. Since you are so unlikely to do even this, to maximise your score you need to have the highest chance of just getting on the board. This will be achieved by aiming at the centre. We now have our two extremes, the perfect player should always aim for treble 20 whereas a hopeless player should aim for the centre. But this still leaves us to ask what the best strategy is for any player in between these edge-cases.

## Modelling the Problem

### The Dartboard

We will be looking at the [regulation dartboard](https://commons.wikimedia.org/wiki/File:Dartboard.svg), envisioned by Brian Gramlin in 1896. The numbers are ordered in such a way they they punish inaccuracy; if you aim for the highest score - 20 - and miss, you could easily end up with the lowest - 1. The standard radii for the rings according the British Darts Organisation are 6.4 mm, 16.0 mm, 99.0 mm, 107.0 mm, 162.0 mm and 170.0 mm with the radius of the whole board being 225 mm. These are the dimensions we'll use for our model.

### Throw Distribution

We will need to model the random nature of a dart throw by some sort of probability distribution. But what sort of distribution might we expect to see? A promising candidate would be modelling the horizontal and vertical displacement of the dart's actual target from the intended one by two independent and identically distributed normal random variables. The normal distribution is a bell shaped curve which is often used for modelling errors so is highly suitable for this purpose. If we set the parameter $\mu$ to zero then the joint density function of the two random variables will be highest at the point where the player aims and then tail off as you get further away, equally so in all directions. This is the exact behaviour we would expect to see in the real world; no matter what your ability is at darts you'll always be more likely to hit closer to where you were aiming than further. The standard deviation parameter, $\sigma$, will control how spread out the dart is likely to be from where it is intended. A good player would have a small standard deviation whereas a bad player would have a larger one resulting in a wider and flatter density curve. This is the same as saying that a good player is more likely to hit near to where they were aiming whilst a bad player has a higher likelihood to be further away.





![](/images/guide-to-darts/guide-to-darts_7_0.png)


This model is not a perfect reflection of reality. However, what we lose in accuracy we gain in simplicity which will come important later when we start using this model for computations. A handful of critiques and improvements are:

* There is no reason to believe that the standard deviation for the horizontal and vertical errors should be the same. It is reasonable to imagine that they would be similar but since you are having to counteract the affect of gravity when considering the vertical accuracy of your shot, this added layer of complexity may make the standard deviation slightly higher.
* The normal distribution is perfectly symmetrical but it is most likely not the case that this be true for the distribution of errors of a real player. The left or right-handedness of the player may give the distribution for the horizontal error a skew in a particular direction and the influence of gravity may do the same for the vertical component.
* Lastly, our assumption of the independence of the vertical and horizontal errors may not be justified. Perhaps if you mess up your horizontal aim, say due to shaky hand, you may be more likely to also mess up the vertical. 

Despite these possible discrepancies, we continue in the belief that our basic model is as accurate a reflection of real life as we need for any non-pathological cases.

## Forming a Strategy

### Calculating Scores

To begin, we will need a function which can convert a pair of Cartesian coordinates representing the location a dart lands to the respective score at that point. Due to the pattern-less nature of the numbers' order we will have to do this directly.


{% codeblock lang:R %}
calcScore <- function(x, y) {
  
  # concert to polar coordinates
  r <- sqrt(x^2 + y^2)
  if (r == 0) {
    theta <- 0
  } else {
    theta <-  atan2(y, x)
  }
  
  # transform so zero is on the boundary of 20 and 1 
  # and the angle increases as we go clockwise
  phi <- pi / 2 - theta - pi / 20
  
  # find what region the angle is in; 
  # e.g. region 1 is 0-18°, region 2 is 18°-36° etc.
  region <- findInterval(phi %% (2 * pi), 
                         seq(0, by = pi/10, length.out = 20))
  
  # find score for that region
  regionScore <- c(1, 18, 4, 13, 6, 10, 15, 2, 17, 3,
                    19, 7, 16, 8, 11, 14, 9, 12, 5, 20)[region]
  
  # find which ring the dart is in
  ring <- findInterval(r, c(0, 6.4, 16, 99, 107, 162, 170, Inf))
  
  # calculate final score
  score <- switch(ring,
                  50,
                  25,
                  regionScore,
                  3 * regionScore,
                  regionScore,
                  2 * regionScore,
                  0)
  
  return(score)
}
{% endcodeblock %}






The best way to visualise this data is using a heat-map.








![](/images/guide-to-darts/guide-to-darts_17_0.png)


### Calculating Expectations

We can use this score function alongside the density function for the 2D normal distribution to find the expected score attained by aiming at any location on the board for a given standard deviation. To find this expected value we simply centre our normal distribution at the point that is aimed at, then integrate the product of the density function and the score function over the entire board. We then sweep the distribution over the whole board to get the expected value at each point. 

In a perfect world we would compute this integral directly and to the highest precision our computer can store. In reality this process is extremely time consuming. In my preparation for this post, I developed such a method and even with the use of time-saving short-cuts and tight coding the program took over an hour to run for some larger standard deviations. Since the end goal is to compute this for many standard deviations, this is not a feasible approach. 

Instead, I got out my pen and paper and went about finding an approximation method which would give only a negligibly different result to the true value but would be much more computable. I decided in the end to split dartboard up into a 361x361 grid (essentially a 1mm x 1mm grid). There was nothing special mathematically about these exact dimensions - they just worked well with the code - and after some long-winded analysis and a touch of brute force computations, I concluded that for standard deviations of at most 110 this method would be accurate to the integer, which for this use is all we need. This is quite a weak bound so in reality the method will be a lot closer to the true solution but in the worst possible case we know that it is at least that good. In practice, if your standard deviation is any more than 100mm then there is no doubt that you should be aiming for the centre of the board.

We can package up this method in a neat little function so we can easily reuse it for any standard deviation.


{% codeblock lang:R %}
expectationMtrx <- function(sd) {
  # values used to approximate integral
  values <- -180:180
  
  # compute values of 2D normal density at approximating points
  density_mtrx <- outer(values, values, function(x, y){
    dnorm(x, 0, sd) * dnorm(y, 0, sd)
  })
  
  # compute scores at approximating points
  score_mtrx <- outer(values, values, calcScore)
  
  # pad with zeros on all sides
  zero_mtrx <- matrix(0, nrow = 361, ncol = 361)
  score_mtrx <- direct.sum(direct.sum(zero_mtrx, score_mtrx), 
                           zero_mtrx)
  
  # matrix to hold expected values
  expectationMatrix <- matrix(0, nrow = 361, ncol = 361)
  
  # sweep distribution matrix over the board
  for (i in 1:361) {
    for (j in 1:361) {
      # which subest of the score matrix to multiply with the density
      score_mtrx.subset <- score_mtrx[i + 361 + values, j + 361 + values]
      
      # contibution to expected value at approximating point
      contrib <- sum(score_mtrx.subset * density_mtrx)
      expectationMatrix[i, j] <- contrib
    }
  }
  
  return(expectationMatrix)
}
{% endcodeblock %}



## Visualising the Expectations

### Static visualisations

We can now call this function for any standard deviation up to 110 and get back a matrix giving the expected score we'd achieve for aiming at any location on the data board with that level of accuracy. Let's generate these matrices for a selection of standard deviations and visualise the results.








![](/images/guide-to-darts/guide-to-darts_24_0.png)


### Animated visualisations

These plots are interesting by themselves but don't tell the whole story. What we really need is an animation to show how the heat-map changes as the standard deviation increases, and more importantly, how this affects the optimum location to aim and the expected score corresponding to it. We produce such an animation using the `gganimate` package. 






![](/images/guide-to-darts/heatmap_animation.gif)
As we can see, the optimum location to aim for a low standard deviation is the treble 20, just as we expected. Once the standard deviation is above 16mm though, it becomes more effective to aim at the treble 19. As the standard deviation increases further, the optimum target sweeps inwards towards the bullseye. By a standard deviation of 100mm we are almost at the centre. If we continued increasing the standard deviation, we would find that the optimum target slowly approaches the exact centre of the board.

### Tracking the optimum

Let's now forget the expected scores themselves and consider just the location of the optimum target for each standard deviation. We can map its path to get the following plot.





![](/images/guide-to-darts/guide-to-darts_34_0.png)


This follows the behaviour that we described before, with the exact jump from treble 20 to treble 19 occurring at a standard deviation of 17mm. It can also be seen that the approach to the center slows as the standard deviation increases.

### Tracking the optimum score

It is now sensible to ask what the optimum obtainable expected score is for each standard deviation. We can look at this using the following visualisation





![](/images/guide-to-darts/guide-to-darts_38_0.svg)


It it evident from this plot, that the game of darts has a definite 'skill elbow'. For small standard deviations, the expected score is extremely high but as soon as you start increasing this, the score drops off massively until it begins to stabilise at around 20mm. Then as you increase standard deviation more the expected optimum score only slightly reduces and will eventually tail off to zero. 

This shows that darts is a game where the difference between a terrible player and a mediocre player is not that severe, but the difference between that same mediocre player and a good player manifests itself savagely, creating a completely one-sided game.

## Estimating Your Standard Deviation

This analysis is all well and good but without a way to calculate your own standard deviation it has no use in practice. I have therefore developed a test to estimate your standard deviation. This involves throwing 100 darts aimed exactly at the centre of the bullseye and recording how many of them lie within the outer bull ring (either the bullseye itself or the ring around it). It can be shown using an appropriate statistical transformation that the radius squared of two independent normal variables with mean zero and equal standard deviation $\sigma$ is distributed exponentially with rate parameter $\frac{1}{2\sigma^2}$. Using this, we can calculate for any standard deviation the probability that a throw aimed at the centre will land within the outer bull. We can then use this probability as a parameter for a binomial random variable representing the number of times we land inside the outer bull in 100 throws. By reversing this process, first estimating the binomial probability parameter from our sample and then using the cumulative density function of the exponential function, we can estimate the standard deviation for any given number of outer bull hits.

If all of that seemed very complicated, don't worry. Understanding the statistics behind where the standard deviations come from is not necessary for using the outcome of it in practice. The results of the above method can simply be read off from the following table.





<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script >$(document).ready( function () {$('#table0').DataTable();} );</script>
<table id="table0" class="display">

<thead>
	<tr><th scope=col>hits</th><th scope=col>sd</th><th scope=col>x</th><th scope=col>y</th><th scope=col>z</th></tr>
	<tr><th scope=col>&lt;int&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;int&gt;</th><th scope=col>&lt;int&gt;</th><th scope=col>&lt;dbl&gt;</th></tr>
</thead>
<tbody>
	<tr><td>100</td><td> 0.0</td><td>  0</td><td> 102</td><td>60.0</td></tr>
	<tr><td> 99</td><td> 5.3</td><td>  0</td><td> 102</td><td>58.0</td></tr>
	<tr><td> 98</td><td> 5.7</td><td>  0</td><td> 102</td><td>52.5</td></tr>
	<tr><td> 97</td><td> 6.0</td><td>  0</td><td> 102</td><td>47.2</td></tr>
	<tr><td> 96</td><td> 6.3</td><td>  0</td><td> 103</td><td>42.9</td></tr>
	<tr><td> 95</td><td> 6.5</td><td>  0</td><td> 103</td><td>39.5</td></tr>
	<tr><td> 94</td><td> 6.7</td><td>  0</td><td> 103</td><td>36.6</td></tr>
	<tr><td> 93</td><td> 6.9</td><td>  0</td><td> 103</td><td>33.9</td></tr>
	<tr><td> 92</td><td> 7.1</td><td> -1</td><td> 103</td><td>31.6</td></tr>
	<tr><td> 91</td><td> 7.3</td><td> -1</td><td> 103</td><td>29.5</td></tr>
	<tr><td> 90</td><td> 7.5</td><td> -1</td><td> 103</td><td>27.5</td></tr>
	<tr><td> 89</td><td> 7.6</td><td> -1</td><td> 104</td><td>25.8</td></tr>
	<tr><td> 88</td><td> 7.8</td><td> -1</td><td> 104</td><td>24.3</td></tr>
	<tr><td> 87</td><td> 7.9</td><td> -1</td><td> 105</td><td>22.9</td></tr>
	<tr><td> 86</td><td> 8.1</td><td> -2</td><td> 105</td><td>21.7</td></tr>
	<tr><td> 85</td><td> 8.2</td><td> -2</td><td> 106</td><td>20.6</td></tr>
	<tr><td> 84</td><td> 8.4</td><td>-35</td><td>-100</td><td>19.8</td></tr>
	<tr><td> 83</td><td> 8.5</td><td>-36</td><td>-100</td><td>19.0</td></tr>
	<tr><td> 82</td><td> 8.6</td><td>-36</td><td>-100</td><td>18.4</td></tr>
	<tr><td> 81</td><td> 8.8</td><td>-37</td><td>-101</td><td>17.8</td></tr>
	<tr><td> 80</td><td> 8.9</td><td>-37</td><td>-101</td><td>17.3</td></tr>
	<tr><td> 79</td><td> 9.1</td><td>-38</td><td>-101</td><td>16.9</td></tr>
	<tr><td> 78</td><td> 9.2</td><td>-38</td><td>-101</td><td>16.5</td></tr>
	<tr><td> 77</td><td> 9.3</td><td>-39</td><td>-100</td><td>16.1</td></tr>
	<tr><td> 76</td><td> 9.5</td><td>-39</td><td>-100</td><td>15.8</td></tr>
	<tr><td> 75</td><td> 9.6</td><td>-40</td><td> -99</td><td>15.6</td></tr>
	<tr><td> 74</td><td> 9.7</td><td>-41</td><td> -97</td><td>15.3</td></tr>
	<tr><td> 73</td><td> 9.9</td><td>-42</td><td> -96</td><td>15.1</td></tr>
	<tr><td> 72</td><td>10.0</td><td>-43</td><td> -94</td><td>14.9</td></tr>
	<tr><td> 71</td><td>10.2</td><td>-44</td><td> -92</td><td>14.7</td></tr>
	<tr><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td></tr>
	<tr><td>30</td><td> 18.9</td><td>-20</td><td>-8</td><td>11.8</td></tr>
	<tr><td>29</td><td> 19.3</td><td>-19</td><td>-8</td><td>11.8</td></tr>
	<tr><td>28</td><td> 19.7</td><td>-18</td><td>-7</td><td>11.7</td></tr>
	<tr><td>27</td><td> 20.2</td><td>-17</td><td>-7</td><td>11.7</td></tr>
	<tr><td>26</td><td> 20.6</td><td>-16</td><td>-6</td><td>11.6</td></tr>
	<tr><td>25</td><td> 21.1</td><td>-16</td><td>-6</td><td>11.5</td></tr>
	<tr><td>24</td><td> 21.6</td><td>-15</td><td>-6</td><td>11.5</td></tr>
	<tr><td>23</td><td> 22.1</td><td>-14</td><td>-5</td><td>11.4</td></tr>
	<tr><td>22</td><td> 22.7</td><td>-14</td><td>-5</td><td>11.3</td></tr>
	<tr><td>21</td><td> 23.3</td><td>-14</td><td>-5</td><td>11.3</td></tr>
	<tr><td>20</td><td> 24.0</td><td>-13</td><td>-5</td><td>11.2</td></tr>
	<tr><td>19</td><td> 24.6</td><td>-13</td><td>-5</td><td>11.1</td></tr>
	<tr><td>18</td><td> 25.4</td><td>-13</td><td>-4</td><td>11.0</td></tr>
	<tr><td>17</td><td> 26.2</td><td>-12</td><td>-4</td><td>11.0</td></tr>
	<tr><td>16</td><td> 27.1</td><td>-12</td><td>-4</td><td>10.9</td></tr>
	<tr><td>15</td><td> 28.1</td><td>-12</td><td>-4</td><td>10.8</td></tr>
	<tr><td>14</td><td> 29.1</td><td>-12</td><td>-4</td><td>10.7</td></tr>
	<tr><td>13</td><td> 30.3</td><td>-11</td><td>-4</td><td>10.6</td></tr>
	<tr><td>12</td><td> 31.6</td><td>-11</td><td>-4</td><td>10.6</td></tr>
	<tr><td>11</td><td> 33.1</td><td>-11</td><td>-4</td><td>10.5</td></tr>
	<tr><td>10</td><td> 34.9</td><td>-11</td><td>-3</td><td>10.4</td></tr>
	<tr><td> 9</td><td> 36.8</td><td>-11</td><td>-3</td><td>10.3</td></tr>
	<tr><td> 8</td><td> 39.2</td><td>-11</td><td>-3</td><td>10.2</td></tr>
	<tr><td> 7</td><td> 42.0</td><td>-11</td><td>-3</td><td>10.2</td></tr>
	<tr><td> 6</td><td> 45.5</td><td>-11</td><td>-3</td><td>10.1</td></tr>
	<tr><td> 5</td><td> 50.0</td><td>-11</td><td>-3</td><td>10.0</td></tr>
	<tr><td> 4</td><td> 56.0</td><td>-11</td><td>-3</td><td> 9.9</td></tr>
	<tr><td> 3</td><td> 64.8</td><td>-11</td><td>-3</td><td> 9.8</td></tr>
	<tr><td> 2</td><td> 79.6</td><td>-11</td><td>-3</td><td> 9.7</td></tr>
	<tr><td> 1</td><td>112.9</td><td>-11</td><td>-3</td><td> 9.6</td></tr>
</tbody>
</table>



If 100 throws seems like too many to bother with, you will get a similiar - though less precise - result by taking 25 or 50 throws and then multplying your number of hits by 4 or 2 respectively to simulate 100 throws.

Recalling the plot of optimum expected score vs. standard deviation, we saw that you need a standard deviation of less than around 20mm to pass the skill elbow and become a good darts player. From the table above, we see that for this to be the case, you would be expected to hit the outer bull at least 28 times out of the 100 hits. Do this hold for you?
