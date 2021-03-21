---
title: "Bank Holiday Bodge: The Sentiment of Shakespeare"
date: '2020-04-13'
excerpt: "As much as we'd like to in order to appear cultured, it is likely that many of us just haven't found the time or motivation to get through the iconic Shakespeare plays we are all familiar with. I don't have a full solution for that, but at the very least, this post presents a way of understanding the general narrative arc of the plays from a quick glance."
thumbnail: /gallery/thumbnails/sentiment-of-shakespeare.jpg
toc: true
categories:
- [Data Science, Visualisation]
tags:
- r
- bank-holiday-bodge
---

## Introduction

Before I started my commitment to producing a quick blog post every bank holiday, I don't think I really considered how frequently they come in pairs. Well, I certainly know now, and for that reason, this post will be short and sweet.


<hr>


With the limited free time I have available, I try my best to have at least some understanding of culture. In particular, I have spent the last year trying to work through 'the classics'. That is, the classic films, books, and even research papers. This has been a colossal challenge as, well, there's just so much to get through.

This got me thinking, my time would be better spent in simply understanding the gist of these cherished pieces. In fact, there are many services devoted to this notion. Take as an example, [Blinkist](https://www.blinkist.com/en), a company promising to spare your valuable time by presenting popular books in condensed 15-minute discoveries. Maybe though, you don't even have time for this. Could there be a way to understand the general arc of a story with just one glance?

The answer to this is almost certainly no, but that didn't stop me from having a shot at it anyway. I decided that the most important summarising feature of a book is the overall arc of sentiment—that is, how positive or negative the text is at any point. This, along with some general context of what the book is about, could give you an idea of how turbulent the story is, what the overall mood is, and how we would be left feeling at the end. Admittedly, this is still far from the level of insight you would glean by thoroughly digesting the same book, but in terms of value added per time spent it is a strong candidate.

I decided to test this approach using a selection of Shakespeare's plays. These have the handy feature of being composed of scenes and acts, offering an intuitive way of dividing the visualisation. That is not to say that this approach couldn't be easily generalised to one long text such as the script of a film—the only change tweak would be to the final type of visualisation. So without further ado ([about nothing](https://en.wikipedia.org/wiki/Much_Ado_About_Nothing)—eh?) let's quickly discuss how I implemented such a system and discuss a selection of the resulting visualisations.

## Sourcing Sentiment

{% colorquote info %}
I do not plan to dissect my source code in detail, but rather link anyone interested to the [GitHub repository](https://github.com/thargreaves/ttested) for this site where they will be able to find.
{% endcolorquote %}


I started by scraping the text of several of Shakespeare's plays from [this site](http://shakespeare.mit.edu/), which contains a large collection of his works. There are other sources that I could have used such as [Project Gutenberg](https://www.gutenberg.org/) which would have also allowed for more general texts, but the site I decided to use made it easy to detect the boundaries of scenes/acts so I kept with that for simplicity.

With these texts obtained, I performed some basic cleaning and then used the `tidytext` package to analyse the overall sentiment (positive or negative) of each scene. I'm not going to go into details regarding exactly how these sentiments are calculated but rather direct curious readers to [this talk](https://youtu.be/l40-JFn6F9M?t=1872) I gave for Warwick Data Science Society which offers an introduction to sentiment analysis and how it can be used to predict presidential approval ratings in the US.

Using these sentiments, it was then straightforward to create a visualisation for the data. I decided to use a waterfall plot as this presents both the overall arc of sentiment as well as scene-to-scene changes.




## Visualisation

A full version of this visualisation can be found [here](https://www.ttested.com/files/shakespeare_sentiments.png). For now, we will just take a look at one example to see how their sentiments match up with the narrative arc.





![](/images/sentiment-of-shakespeare/sentiment-of-shakespeare_18_0.svg)


If you are familiar with Romeo and Juliet, I hope you will agree that this plot quite accurately portrays the overall narrative arc of the play. We start with warring factions, which is then disrupted with hopes of love. This sentiment then grows to reach a climax at the end of the second act with marriage of the pair imminent. Sadly, from then on, it's only downhill, concluding with a mournful mutual-suicide in the last scene of the play.

Without knowledge of the play, picking out those details is admittedly impossible. Despite this, picking out the general turbulence of the story's sentiment, the climax of happiness in the middle and the eventual sad ending is complete feasible in one glance. Either way, we are left with a pretty visualisation.

I hope you enjoyed this post. I would encourage anyone to take the source code for this project (linked above) and apply it to other Shakespeare plays or entirely new sources. Who knows what interesting patterns you may find.
