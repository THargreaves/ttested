---
title: "Beauty From Chaos"
date: '2018-09-20'
excerpt: "Starting a new blog is hard. Period. In this post, I discuss the issues I faced in writing my first blog piece and how I overcame these by producing a simple, yet full workable, Shiny web app. It may be only be a small way to start, but I hope that it will be the first step in a highly fruitful journey."
thumbnail: /gallery/thumbnails/beauty-from-chaos.png
toc: true
categories:
- [Visualisation, Interactive]
tags:
- shiny
- r
---

## The Nightmare That Is a New Blog

Starting a blog should not be a difficult feat; and yet that is just what it has proven to be for me. There are far too many questions that I still don't have the answer to:

* What should I blog about?
* Who should I intend for the blog to be read by?
* How should I produce and publish it?
* When should I post my first piece of work?

On top of this I found myself on a never-ceasing chase for the perfect first post. Every time I felt like I was getting close to completion on a project I became faced with one of many dilemmas:

* There's some bug in my work that I don't know how to fix
* I don't know enough to properly solve the problem I'm working on
* The project seems too simple to share with the world

I have let these issues envelope me and this has resulted in an 'R' directory clogged with the corpses of uncompleted works. Almost all forgotten in the chase for a new exciting idea doomed for the same fate. This has gone on for some time. But now I have decided that it's time to put my foot down and take the plinge. Release anything. More exciting, difficult, and long-form work can always follow but the first step needed to be taken else that point would remain unreachable. I finally have the answers to the four questions that have been haunting me for the past few months: whatever, whoever, however, **now**.

The rest will follow soon as I learn more about what I want to achieve and how I can go about doing so. But for now, I hope you enjoy a small interactive visualisation I put together.

## One small step for man, one small step for mankind

I have always been interested in the patterns and order you can derive from random noise. This is what this first project was about. I decided to generate a matrix of random integers in some range, colour them in, and then connect matching adjacent points with a line of the same colour. This gave rise to some interesting designs, two examples of which are shown below.





![Two example designs, one with 3 colours and the other with 2](/images/beauty-from-chaos/beauty-from-chaos_5_0.svg)


This was simple enough to do so I decided to make the visualisation interactive using the [Shiny](https://shiny.rstudio.com/) package. The result of this can be found [here](https://timhargreaves.shinyapps.io/BeautyFromChaos/). Why not have a play with it and see what interesting designs it will generate for?
