---
title: "Bank Holiday Bodge: Daily XKCD Mailer"
date: '2020-01-01'
excerpt: "2020 is here and one of my goals for the coming year is to finally get caught up on the XKCD comic series. Starting from the beginning is a dull way of doing things so instead I've taken advantage of Google Cloud Platform's Cloud Scheduler to setup a python script to email me a random selection of new comics each day. In this post I will share how you can do the same."
thumbnail: /gallery/thumbnails/xkcd-mailer.png
toc: false
categories:
- [Computer Science, Cloud Computing]
tags:
- python
- gcp
- bank-holiday-bodge
- tutorial
---
{% colorquote success %}
For those only interested in the code and setup guide for the mailer, see the corresponding [GitHub repository](https://github.com/THargreaves/xkcd-mailer).
{% endcolorquote %}


"Hey, that reminds of that [XKCD comic](https://xkcd.com/) about *XYZ*! Have you seen that one?"

As a generally techy person who spends most of his working and social time with equally techy individuals, I probably hear the above utterance more often than "How are you today?" or "Good Morning" (though perhaps that speaks more towards the introversion of some of my colleagues). Although there are rare occasions when I can answer it with "yes, that one was great!", I sadly find myself having no clue what they are talking about more often than not. 

The reason for this is that I discovered the XKCD series relatively late in the comic's lifespan. By that time, [Randall](https://en.wikipedia.org/wiki/Randall_Munroe) had already released close to 2000 comics, and the thought of catching up seemed daunting. On the other hand, the more mature data scientists, software engineers, and web developers that I know were well into their careers by the time XKCD was first gaining traction, and so were able to keep track of its progression.

This desire to be in on the jokes (without having to first sneak a quick Google of the comic on my phone) led me to decide that 2020 would be the year that I finally got caught up on the entire catalogue. The issue was, I didn't want to view the series in chronological order. It took some time for Randall to develop his style and so what I really wanted was a random selection of his comics from the entire time-span of the series' existence. I could have simply manually chosen a random selection of comics each day but then I would have to be aware of not repeating choices and making sure I saw the first parts of multi-part comics before the rest. This seemed like far too much fuss.

Instead, I decided that Python could lend me a hand. I created a script to scrape the [all comics pages](https://www.explainxkcd.com/wiki/index.php/List_of_all_comics_(1-500)) of [explainxkcd.com](https://www.explainxkcd.com/wiki/index.php/Main_Page) and then send me a handful of comics. Furthermore, the script ensures that it never repeats a comic, only sends the first unread comic of a multi-part series, and safely terminates when the user is up-to-date. I then set this script up on [Google Cloud Platform](https://cloud.google.com/) (GCP) so that it would execute every weekday at 9am to send an email to my work address with my daily selection of comics.

This project has larger splintered off from my blog to form its own [GitHub repository](https://github.com/THargreaves/xkcd-mailer). This is where you can find instructions on how to setup the script on GCP. I will use the rest of this post to simply justify some of my choices in developing the script and choosing GCP as its host.

![Example of an email sent by the mailer](/images/xkcd-mailer/mail-content.png)

The structure of my code is quite standard though I have tried to make it as flexible as possible. That way, with a bit of knowledge of CSS and RegEx, the script can be easily to scrape another series (say [PHD comics](http://phdcomics.com/)). 

There were many ways that I could have executed this script on a daily basis. My first attempt was with [PythonAnywhere](https://www.pythonanywhere.com/) but had to abandon this idea when I discovered their [strict webscraping policy](https://help.pythonanywhere.com/pages/403ForbiddenError/). This left me to choose between [Amazon Web Services](https://aws.amazon.com/) (AWS) and GCP. I decided to go with the latter as I have more experience with it and, more importantly, you are not required to supply billing information to use their free tier as is the case with AWS. This means that there was no risk of an accidental, surprise billing.

I hope that any other XKCD fans find this script useful. Anyway, happy new year, and all the best for 2020!
