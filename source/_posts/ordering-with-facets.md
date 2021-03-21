---
title: "Ordering Factors within a Faceted Plot"
date: '2019-11-05'
excerpt: "ggplot2 is an amazing tool for building beautiful visualisations using a simple and coherent grammar—that is, when it wants to play nice. Sadly, this is not always the case and one can find themselves developing strange workarounds to overcome the limitations of the package. This post discusses one of these approaches, used to facilitate the correct ordering of factors within a faceted plot."
thumbnail: /gallery/thumbnails/ordering-with-facets.png
toc: true
categories:
- [Data Science, Visualisation]
tags:
- tidyverse
- r
- tutorial
---

Recently, I stumbled across an interesting dataset on [Kaggle](https://www.kaggle.com/). It contained information on every event, for every relevant year of the last 120 years of Olympic Games. The dataset can be found at [this](https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results) link, and although it does have some minor data integrity issues (at least at the time of writing this post) it has clear potential for telling some amazing stories.

My plan was to start simple, and create a faceted column chart showing how many medals the top 10 countries won over a selection of four games. At least, I _thought_ this would be simple. In fact, this plot ended up taking me down a data-viz rabbit hole, desperately trying to get by factors to order themselves how I wanted. Thankfully, I did eventually emerge, and so I am now here to share my journey so that the next unlucky victim of ggplot's tyranny can reach a solution without so much frustration.

### The Data

I will skip over the exact details regarding the full scope of the dataset and how I processed it for my use. The Kaggle page explains the contents of the dataset in clear terms and the source code for this project can be found on this blog's [GitHub repository](https://github.com/THargreaves/ttested). The important point is that after some messing about, I ended up with a dataset looking like this.





{% codeblock lang:R %}
medals_df
{% endcodeblock %}




<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script >$(document).ready( function () {$('#table0').DataTable();} );</script>
<table id="table0" class="display">

<thead>
	<tr><th scope=col>Team</th><th scope=col>Year</th><th scope=col>Bronze</th><th scope=col>Gold</th><th scope=col>Silver</th><th scope=col>Total</th></tr>
	<tr><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;int&gt;</th><th scope=col>&lt;int&gt;</th><th scope=col>&lt;int&gt;</th><th scope=col>&lt;int&gt;</th><th scope=col>&lt;int&gt;</th></tr>
</thead>
<tbody>
	<tr><td>Soviet Union </td><td>1956</td><td>32</td><td>37</td><td>29</td><td> 98</td></tr>
	<tr><td>United States</td><td>1956</td><td>17</td><td>31</td><td>25</td><td> 73</td></tr>
	<tr><td>Australia    </td><td>1956</td><td>13</td><td>13</td><td> 7</td><td> 33</td></tr>
	<tr><td>Germany      </td><td>1956</td><td> 7</td><td> 6</td><td>13</td><td> 26</td></tr>
	<tr><td>Hungary      </td><td>1956</td><td> 7</td><td> 9</td><td>10</td><td> 26</td></tr>
	<tr><td>Italy        </td><td>1956</td><td> 9</td><td> 8</td><td> 7</td><td> 24</td></tr>
	<tr><td>Great Britain</td><td>1956</td><td> 9</td><td> 6</td><td> 6</td><td> 21</td></tr>
	<tr><td>Japan        </td><td>1956</td><td> 3</td><td> 4</td><td>10</td><td> 17</td></tr>
	<tr><td>Sweden       </td><td>1956</td><td> 6</td><td> 6</td><td> 5</td><td> 17</td></tr>
	<tr><td>Finland      </td><td>1956</td><td>11</td><td> 3</td><td> 1</td><td> 15</td></tr>
	<tr><td>Soviet Union </td><td>1976</td><td>35</td><td>49</td><td>41</td><td>125</td></tr>
	<tr><td>United States</td><td>1976</td><td>25</td><td>34</td><td>35</td><td> 94</td></tr>
	<tr><td>East Germany </td><td>1976</td><td>25</td><td>40</td><td>25</td><td> 90</td></tr>
	<tr><td>West Germany </td><td>1976</td><td>17</td><td>10</td><td>12</td><td> 39</td></tr>
	<tr><td>Romania      </td><td>1976</td><td>14</td><td> 4</td><td> 9</td><td> 27</td></tr>
	<tr><td>Poland       </td><td>1976</td><td>13</td><td> 7</td><td> 6</td><td> 26</td></tr>
	<tr><td>Japan        </td><td>1976</td><td>10</td><td> 9</td><td> 6</td><td> 25</td></tr>
	<tr><td>Bulgaria     </td><td>1976</td><td> 7</td><td> 6</td><td> 9</td><td> 22</td></tr>
	<tr><td>Hungary      </td><td>1976</td><td>13</td><td> 4</td><td> 5</td><td> 22</td></tr>
	<tr><td>Cuba         </td><td>1976</td><td> 3</td><td> 6</td><td> 4</td><td> 13</td></tr>
	<tr><td>United States</td><td>1996</td><td>25</td><td>43</td><td>31</td><td> 99</td></tr>
	<tr><td>Germany      </td><td>1996</td><td>26</td><td>20</td><td>18</td><td> 64</td></tr>
	<tr><td>Russia       </td><td>1996</td><td>16</td><td>26</td><td>21</td><td> 63</td></tr>
	<tr><td>China        </td><td>1996</td><td>11</td><td>13</td><td>20</td><td> 44</td></tr>
	<tr><td>Australia    </td><td>1996</td><td>22</td><td> 9</td><td> 9</td><td> 40</td></tr>
	<tr><td>France       </td><td>1996</td><td>15</td><td>14</td><td> 7</td><td> 36</td></tr>
	<tr><td>Italy        </td><td>1996</td><td>12</td><td>13</td><td>10</td><td> 35</td></tr>
	<tr><td>Cuba         </td><td>1996</td><td> 8</td><td> 9</td><td> 8</td><td> 25</td></tr>
	<tr><td>Ukraine      </td><td>1996</td><td>12</td><td> 9</td><td> 2</td><td> 23</td></tr>
	<tr><td>South Korea  </td><td>1996</td><td> 3</td><td> 6</td><td>13</td><td> 22</td></tr>
	<tr><td>United States</td><td>2016</td><td>36</td><td>45</td><td>36</td><td>117</td></tr>
	<tr><td>China        </td><td>2016</td><td>25</td><td>25</td><td>18</td><td> 68</td></tr>
	<tr><td>Great Britain</td><td>2016</td><td>17</td><td>27</td><td>23</td><td> 67</td></tr>
	<tr><td>Russia       </td><td>2016</td><td>20</td><td>18</td><td>17</td><td> 55</td></tr>
	<tr><td>France       </td><td>2016</td><td>14</td><td>10</td><td>18</td><td> 42</td></tr>
	<tr><td>Germany      </td><td>2016</td><td>15</td><td>16</td><td>10</td><td> 41</td></tr>
	<tr><td>Japan        </td><td>2016</td><td>21</td><td>12</td><td> 8</td><td> 41</td></tr>
	<tr><td>Australia    </td><td>2016</td><td>10</td><td> 8</td><td>11</td><td> 29</td></tr>
	<tr><td>Italy        </td><td>2016</td><td> 8</td><td> 8</td><td>11</td><td> 27</td></tr>
	<tr><td>Canada       </td><td>2016</td><td>15</td><td> 4</td><td> 3</td><td> 22</td></tr>
</tbody>
</table>



To summarise, this is a dataset of 40 rows. Each row corresponds to the medals won by a particular country at a particular summer Olympic games. Each value of the year column is one 1956, 1976, 1996, and 2016, and only the ten countries with the most  medals for each year are included.

### Attempt 1 - Hope

What I then wanted to do, was to create a column chart showing the medals won by each country, faceted by the year of the games. My first solution was somewhat naive, going something like this.





{% codeblock lang:R %}
# tidy the dataset...
gather(medals_df, c(Bronze, Gold, Silver), key = 'Medal', value = 'Count') %>%
    mutate(Medal = factor(Medal, levels = c('Gold', 'Silver', 'Bronze'))) %>%
    # ...and plot
    ggplot(aes(x = Team, y = Count, fill = Medal)) +
        geom_col() +
        facet_wrap(~Year, nrow = 2, scales = 'free_y') +
        coord_flip() +
        # superfluous additions for aesthetics - see GitHub for contents 
        labels_and_colours
{% endcodeblock %}




![](/images/ordering-with-facets/ordering-with-facets_13_0.svg)


It's a valiant effort, but frankly, it's just ugly. By default, ggplot uses the factor's underlying ordering when deciding how to arrange a categorical axis. Since we did not specify an ordering, R defaults to using alphabetical order and so, as we can see, the y-axes is sorted alphabetically. Not only does this look bad but it makes the plot difficult to interpret. Which team had the 5th higher medal total in 1976? You'd have to take a second to figure it out; if the levels had been correctly ordered, this would be much simpler.

### Attempt 2 - Compromise

The solution seems obvious now (I thought): the problem is brought upon by not specifying an order for the `Team` factor before plotting. So if we were to do just that, our problem should disappear. We can use the `reorder` function from base R (alternatively `forcats::fct_reorder`) combined with a `mutate` to achieve this (or so I thought). The code and result look something like this.


{% codeblock lang:R %}
# first, reorder the factors by total...
mutate(medals_df, Team = reorder(Team, Total)) %>%
    # ...then tidy the dataset...
    gather(c(Bronze, Gold, Silver), key = 'Medal', value = 'Count') %>%
    mutate(Medal = factor(Medal, levels = c('Gold', 'Silver', 'Bronze'))) %>%
    # ...and plot
    ggplot(aes(x = Team, y = Count, fill = Medal)) +
        geom_col() +
        facet_wrap(~Year, nrow = 2, scales = 'free_y') +
        coord_flip() +
        # superfluous additions for aesthetics - see GitHub for contents 
        labels_and_colours
{% endcodeblock %}




![](/images/ordering-with-facets/ordering-with-facets_17_0.svg)


Close, but no cigar. Some ordering has taken place, but things still aren't quite right. The problem is that reordering has taken place at a global level, not per facet. This is not a bug, but the expected behaviour of `reorder`. When faced with duplicates in the factor it is given, it only orders the levels by using the median value for each unique level (`forcats::fct_reorder` uses the mean). Since our dataset contains teams that feature in the top 10 over multiple years (in fact, there are quite a few), this approach to ordering fails too.

We tried to play nicely and cooperate with ggplot, but that got us nowhere. It's now time to bring out the big guns.

### Attempt 3 - Aggression

At this point, I was starting to lose hope. Maybe this just wasn't something within the scope of ggplot's arsenal. I had one more idea though. It wasn't going to be pretty or even that sensible, but sure enough it worked. Here is the final code I came up with and the resulting plot. I will explain the mechanics of this code immediately after.


{% codeblock lang:R %}
medals_df %>%  
    # create a column called Order to store the factor ordering for each year
    arrange(Year, Total) %>%
    mutate(Order = row_number()) %>%
    # tidy the dataset as before
    gather(c(Bronze, Gold, Silver), key = 'Medal', value = 'Count') %>%
    mutate(Medal = factor(Medal, levels = c('Gold', 'Silver', 'Bronze'))) %>%
        # wrap in curly brackets so we can access the augmented dataset multiple times
        {
            # use Order for the x aesthetic instead of Team
            ggplot(., aes(x = Order, y = Count, fill = Medal)) +
                geom_col() +
                facet_wrap(~Year, nrow = 2, scales = 'free_y') +
                coord_flip() +
                # add custom breaks and labelling to the x-axis
                scale_x_continuous(
                  breaks = .$Order,
                  labels = .$Team,
                  expand = c(0,.4)  # just for looks
                ) +
                # superfluous additions for aesthetics - see GitHub for contents 
                labels_and_colours
        }
        
{% endcodeblock %}




![](/images/ordering-with-facets/ordering-with-facets_22_0.svg)


Perfect! Not only is this easier to interpret but it looks much better. So why does this work? Let's get into the details.

First, we create a new column, `Order`, which stores the order that each factor level should appear in _within_ each year. We do this by first arranging by year, then total, and using the `row_number()` helper to save that ordering. The observations for the year 1956 now have orderings spanning from 1 to 10, and if we carry on till 2016, these have orderings from 31 to 40.

When we get to plotting, rather than using `Team` as our x aesthetic, we use this new `Order`. Since we use a `free_y` scale when faceting this results in us still having ten y-axis ticks for each facet. At this point though, the ticks will be labelled 1-10, 11-20, etc. for each facet. To correct this, we need to manually set our x-axis breaks and labels.

We do this in `scale_x_continuous()`. We set the breaks to be equal to the `Order` column (note we use `.` here to access the dataframe we piped into the curly bracketed section) and then use `Team` as the labels. This means that the numeric labels are replaced with the team name that they original corresponded to. This is exactly what we were after.

### Wrapping Up

There you have it. It may not be the most elegant solution, but it certainly works. This approach can be adapted for any data that you wish to plot in this form. I hope that with this example to guide the way, a significant amount of frustration can be avoided.
