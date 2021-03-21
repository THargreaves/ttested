---
title: "Gloopy Violin Plots"
date: '2018-10-11'
excerpt: "The fourth dimension is often overlooked in data visualisation applications but, in doing so, are we potentially missing out on some more effective ways to present data? In this post, I argue that there are certain use cases where adding a temporal dimension to your visualation greatly improves the clarity of the result in expressing you message. Furthermore, I offer an example of such a visualisation, produced using the `gganimate` package."
thumbnail: /gallery/thumbnails/gloopy-violin-plots.png
toc: true
categories:
- [Data Science, Visualisation]
tags:
- r
- animation
- tidyverse
- tutorial
---
{% colorquote info %}
The following packages will be required for this post:
{% codeblock lang:R %}
library(gganimate) # animation
library(ggplot2) # visualisation
library(dplyr) # manipulating data
library(readr) # importing data
library(tidyr) # tidying data
{% endcodeblock %}


{% endcolorquote %}





## The Importance of the Fourth Dimension in Data Visualisation

The fourth dimension is often overlooked in data visualisation applications. There are some very understandable reasons for this. To begin, such plots are of no use in static mediums such as scientific journals, research papers or printed blog posts. Furthermore, they often require more effort to produce than single frame plots, perhaps requiring additional tools and packages or, in the worst, the manual stitching together of individual plots.

Despite its drawbacks, the use of time in the production of data visualisations can be very effective in expressing the meaning of a dataset in a natural and distinctly human way. Consider this example: if I were to give you pictures taken from a fixed camera at secondly intervals of a car driving down a road, you would most likely struggle to build a mental image of how far that car was travelling. This is strange because you have all the necessary data. All you are left to do is interpolate for the moments that you missed and then use your understanding of the world to have a guess at the speed of the car. This would be a surprisingly difficult task, yet if I gave you a video of the moving car, although you may not be completely accurate, you'd be able to make a much better judgement of the speed the car was travelling at.

## Enter: Gloopy Violin Plot

I intend to use this principle to produce a natural visualisation of the progress of same-sex marriage laws in the United States using [this](http://www.pewforum.org/2015/06/26/same-sex-marriage-state-by-state/) dataset by the [Pew Research Centre](http://www.pewresearch.org/). A reduced view of the dataset looks like this,





<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script >$(document).ready( function () {$('#table0').DataTable();} );</script>
<table id="table0" class="display">

<thead>
	<tr><th scope=col>State</th><th scope=col>1998</th><th scope=col>1999</th><th scope=col>2000</th></tr>
	<tr><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;chr&gt;</th></tr>
</thead>
<tbody>
	<tr><td>Alabama    </td><td>Statutory Ban     </td><td>Statutory Ban     </td><td>Statutory Ban     </td></tr>
	<tr><td>Alaska     </td><td>Constitutional Ban</td><td>Constitutional Ban</td><td>Constitutional Ban</td></tr>
	<tr><td>Arizona    </td><td>Statutory Ban     </td><td>Statutory Ban     </td><td>Statutory Ban     </td></tr>
	<tr><td>Arkansas   </td><td>Statutory Ban     </td><td>Statutory Ban     </td><td>Statutory Ban     </td></tr>
	<tr><td>California </td><td>Statutory Ban     </td><td>Statutory Ban     </td><td>Statutory Ban     </td></tr>
	<tr><td>Colorado   </td><td>No Law            </td><td>No Law            </td><td>Statutory Ban     </td></tr>
	<tr><td>Connecticut</td><td>Statutory Ban     </td><td>Statutory Ban     </td><td>Statutory Ban     </td></tr>
	<tr><td>Delaware   </td><td>Statutory Ban     </td><td>Statutory Ban     </td><td>Statutory Ban     </td></tr>
	<tr><td>Florida    </td><td>Statutory Ban     </td><td>Statutory Ban     </td><td>Statutory Ban     </td></tr>
	<tr><td>Georgia    </td><td>Statutory Ban     </td><td>Statutory Ban     </td><td>Statutory Ban     </td></tr>
</tbody>
</table>



The typical way of representing this data may be a collection of bar plots faceted by year or, if you allow yourself to treat the nominal variable representing the type of law as ordinal, a [ridgeline plot](http://blog.revolutionanalytics.com/2017/07/joyplots.html) (previously known as a joy-plot) would be a good choice. The problem with these two methods though is that it is very hard to conceptualise the speed of change when we are only given single snapshots in time rather than the whole picture just like with the car example above.

Instead I wanted to produce an animated violin plot to represent this data in a way that would be easier to interpret the message of. The core of this visualisation is produced as follows.
{% codeblock lang:R %}
# load data from a csv on GitHub
dl <- "https://raw.githubusercontent.com/zonination/samesmarriage/master/ssm.csv"
df <- read_csv(dl)
# store the four types of law from most opposed to least
laws <- c("Constitutional Ban", "Statutory Ban", "No Law", "Legal")

df %>%
  # tidy the data frame so it is in a form ggplot can work with
  gather(key = "year", value = "law", '1995':'2015') %>%
  # factor the law types using the order stored in the laws variable
  mutate(law = factor(law, levels = laws, ordered = TRUE)) %>%
  # encode the laws as numerical values so they can be used with a violin plot
  mutate(law.encode = as.numeric(law)) %>%
  # add dummy years to add pause before looping †
  rbind(filter(., year == "2015") %>%
          mutate(year = "2015 ")) %>%
  rbind(filter(., year == "2015") %>%
          mutate(year = "2015  ")) %>%
  # generate static plot
  ggplot(aes(x = 0, y = law.encode)) +
  geom_violin(bw = .3, trim = FALSE, scale = "area") +
  scale_x_discrete("Proportion of States") +
  scale_y_continuous("", breaks = 1:4, labels = laws) +
  coord_flip(xlim = c(-.5,.5), ylim = c(0,5)) +
  labs(title = "Same-Sex Marriage Laws in the USA", 
       # remove "dummy" from dummy year names
       subtitle = paste0("Year: ", "{closest_state}"),
       caption = "Source: Pew Research Centre") +
  theme_minimal() +
  theme(panel.grid.minor.x = element_blank()) +
  # animate using gganimate
  transition_states(year, transition_length = 1, state_length = 0) +
  ease_aes('sine-in-out') -> p

# animate with custom parameters
animate(p, nframes = 300, fps = 15, width = 720, height = 540)
{% endcodeblock %}

![](/images/gloop-violin-plots/gloopy-violin-plot.gif)
{% colorquote info %}
† Sadly, at of the time of writing this post, `gganimate` does not have a simple way to add a pause between loops. This is the best solution I could find to overcome this limitation. UPDATE: `gganimate` now has the ability to add pauses at both the beginning and end of the loop. See the [documentation](https://rdrr.io/github/dgrtwo/gganimate/man/animate.html) for the `animate()` function to learn more.
{% endcolorquote %}


This graphic shows us how much fluctuation there was on same-sex marriage law in the USA throughout the early 2000's and almost makes clear the sudden impact on national legislation when the Supreme Court legalized same-sex marriage on June 26, 2015.
