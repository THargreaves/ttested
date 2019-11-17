---
title: "The Inaccuracy of Accuracy"
date: '2018-12-06'
excerpt: "In a data-driven world, your analyses will only ever be as good as the metric you use to evaluate them. In this post, I make the claim that the de facto metric used in data science is unfit for purpose and and can lead to the construction of unethical models. If this is the case, what should we use instead?"
thumbnail: /gallery/thumbnails/inaccuracy-of-accuracy.jpg
toc: true
categories:
- [Data Science, Best Practice]
tags:
- ethics
- no-coding
---
Imagine for a moment that, as part of your job, you are tasked with solving a statistical modelling problem. You've been instructed to develop a predictive tool - trained on a collection of historical data - that will take in new, unseen data and output a binary response variable ('yes'/'no', 1/0, etc.). You crack open your favourite IDE, swiftly throw down a few lines of code, hit 'run' and there you have it: 99% accuracy. 

Great job! Clearly that machine learning course you took has paid off. You pack up your work and prepare to head home early. After all, you earned it. Right?

***

Let's pause for a second and contemplate whether this is really a worthy accomplishment. The answer is: it depends. The importance of this '99%' figure will ultimately be determined by what you are trying to model and, more critically, what problem you are trying to solve. Let's look at this scenario again, but this time with reference to a specific real-world problem.

Suppose that you've been contracted by a biomedical company to build a model that will predict whether a patient has an illness based on a set of biological data collected from them. The illness in question is quite rare, affecting only around 1 in 500 people as illustrated below.






![](/images/inaccuracy-of-accuracy/inaccuracy-of-accuracy_3_0.svg)


Since the illness affects people with such infrequency, it's difficult to even spot the affected patients in the illustration of the sample (or near impossible for the [dichromats](https://www.color-blindness.com/deuteranopia-red-green-color-blindness/) - I can only apologise in advance). 

Let's go about fitting a model to this data. We use the following algorithm to determine whether or not a person has the illness.

1. Assume the illness does not exist

2. See step 1

We simply classify every patient as not having the illness. This is a preposterous idea and yet it will give us an accuracy of around 99.8%, far higher than the 99% accuracy we flaunted earlier. After all, we may never correctly diagnose a patient who *does* have the illness, but we will get every prediction correct whenever a patient *doesn't* have the illness, and this accounts for the vast majority of observations. 

This, however, is not the behaviour we wish to capture. Correctly identifying the few people who have the illness so that they can seek medical assistance quickly, is far more important than requiring a handful of people to be checked over by their doctor when it wasn't essential. In similar cases, such as fraud detection, we wish to obtain the same behaviour. It is vital that we detect the few true cases of fraud even if doing so results in a few incorrect guesses, which can be quickly disregarded after the necessary security checks have been completed.

The conclusion we reach - quite paradoxically - is that for a large range of problems, if we want to build an 'accurate' model in the colloquial sense, using the statistical measurement of accuracy is no use. Maximising accuracy just can't be guaranteed to reflect the problem we are trying to solve. But what can?

## A finer look at the problem

Let's take a look at our diagnosis problem once more, but through a new lens: the confusion matrix. We take a sample of 1000 people from the population and use our naive model to predict whether they have the illness (that is, we predict that everyone is unaffected). We then compare our predicted classifications with the true value to get the following confusion matrix.





              Reference
    Prediction  No Yes
           No  998   2
           Yes   0   0


This table shows that, of the 998 people who did in fact have the illness, we correctly predicted that all 998 of them were unaffected and of the 2 people who did, we incorrectly predicted that both of them did not have the illness. We calculate our accuracy by summing the number of correct predictions (the diagonal) and dividing by the total size of our sample (sum of all cells) giving the $\frac{998+0}{998+2+0+0} = 99.8\%$ we stated before. 

In order to describe the confusion matrix better we will need some terminology to describe each cell.

* The upper-left corner gives the number of true negatives (TN). This is the number of patients that we correctly identified to *not have* the illness.
* The upper-right corner gives the number of false negatives (FN). This is the number of patients who did have the illness but for who we didn't identify it.
* The lower-left corner gives the number of false positives (FP). This is the number of patients who didn't have the illness but our model predicted that they did.
* Lastly, the lower-right corner gives the number of true positives (TP). This is the number of people we correctly identified to *have* the illness.

Then, for a general binary classification problem with a positive (P) and negative (N) class (these were "yes" and "no" respectively for our diagnosis problem), the confusion matrix will look like this.





              Reference
    Prediction N  P 
             N TN FN
             P FP TP


Remembering how we calculated the accuracy using the matrix diagonal before, we get the following formula for the statistical accuracy of our model in terms of the false/true, positive/negative value counts.

$$\textrm{Accuracy} = \frac{\textrm{TN} + \textrm{TP}}{\textrm{TN} + \textrm{FN} + \textrm{FP} + \textrm{TP}}$$

## Precision and Recall

Thinking back again to the diagnosis problem, let us contemplate why our use of statistical accuracy as a measure of success failed. The main issue was that what we really valued in our model was the ability to correctly identify ill patients (the positive class) more so than the avoidance of labelling some perfectly healthy patients as likely to be ill. This would not be as much of an issue if the two classes (ill and not ill) were in similar proportions. In that case, failing to correctly identify ill patients would have a noticeable effect on our accuracy. When, however, the positive class is dwarfed by the negative class (or vice versa) the accuracy metric will no longer be of much use.

### Recall

We have already seen that the accuracy metric fails spectacularly for our diagnosis problem. But there is a metric that works much better. It goes by the name of 'recall' and its formula is as follows.

$$\textrm{Recall} = \frac{\textrm{TP}}{\textrm{TP} + \textrm{FN}}$$

In words, we calculate this value by taking the number of cases in which we correctly identified the illness and divide that by the total number of people that did in fact have the illness. In our example above, since $\textrm{TP} = 0$, we get a precision of $0$. Whereas we gained an extremely high value of accuracy, the precision of our model is as low as it physically can be. It is clear that this metric can't be duped by the rarity of the positive class.

### Precision

This handles the case where we wish to focus on the correct identification of the positive class; but what about the negative class? An example of such a scenario is the judicial system. The assumption of innocence shows that we care much more about ensuring an innocent person is not sent to prison, than making sure that all guilty persons are locked away. This suffers from the reverse of the issue that the diagnosis problem had. Here the positive class is likely to outsize the negative since it would be rare to bring someone to court without at least a reasonable amount of evidence against them. Because of this, if we were to evaluate our judicial system using statistical accuracy as our metric, we would get a good performance from the practice of immediately jailing anyone who enters the courtroom. Another example would be spam email detection; letting some spam get through is tolerable but hiding important emails in the junk folder is not. Thankfully, there is an alternative metric which counteracts this behaviour. It is called 'precision' (also known as sensitivity).

$$\textrm{Precision} = \frac{\textrm{TP}}{\textrm{TP} + \textrm{FP}}$$

This is very similar to recall, but rather than dividing the number of true positive cases by the total number of *actual* positives, we instead divide by the total number of positives we *predicted*. In other words, it is asking what proportion of the observations we predicted to be positive were actually positive. 

There are many other statistical measurements used to evaluate binary classification models such as specificity, fall-out, and false discovery rate. These are described in intricate detail on the Wikipedia page for [sensitivity and specificity](https://en.wikipedia.org/wiki/Sensitivity_and_specificity).

### The precision-recall spectrum

Although these metrics may seem like miraculous solutions to all accuracy-related issues they do have their own drawbacks. These both tackle particular types of problems well - precision is very good at ensuring you don't inaccurately identify too many negative class members, and recall makes sure that you correctly identify a good proportion of the positive class members. However, the success of one can lead to the failure of the other - precision does not care whether you are correctly identifying the positive class members, and recall isn't bothered whether you erroneously identify a large amount of negative class members. They do their own jobs well, but do not focus on anything else.

They exist on a spectrum; succeeding in one opens you up to the possibility of failure in the other. If you know that the type of problem you are trying to tackle will be solved better by using a specific one of these then go ahead. But, if you want something in the middle of this spectrum - combining their behaviour - there is another option.

## The $\textrm{F}\_1$ Score

When you want to reflect the combination of the behaviour of two metrics, a common strategy is to take their mean. Which mean? That very much depends on the context. In this context the best course of action is to use the harmonic mean. In doing this we define the $\textrm{F}\_1$ score of a model.

$$\textrm{F}_1 = \frac{2}{\frac{1}{\textrm{Precision}}+\frac{1}{\textrm{Recall}}}\left(=\frac{2 \times\textrm{Precision}\times\textrm{Recall}}{\textrm{Precision}+\textrm{Recall}}\right)$$

This method gives a very good balance between precision and recall. Whenever either of precision or recall get two small, the denominator will grow massively, forcing the $\textrm{F}\_1$ score to shrink to near zero. More importantly, unlike with the arithmetic and geometric mean, having a small value of one of precision and recall is very hard (and in some cases impossible) to fix just by adjusting the other value. You are forced to fix the issue at hand to improve your score. Furthermore, since precision and recall are restricted to the range $[0,1]$ so will their harmonic mean, $\textrm{F}\_1$. This metric will account for a perfect balance of precision and recall, no matter the split of the positive and negative class quantities, and still return a value that we can process in a similar way to accuracy. This is exactly the behaviour we want in our metric.

Notice that when one of precision or recall is zero, then the $\textrm{F}\_1$ score is undefined. Therefore we need at least one correctly identified positive case in order to have a valid $\textrm{F}\_1$ score. This seems resonable; if your model doesn't get a single positive prediction right, it is barely even a model. There is also a convention (which you are free to use as long as you don't mind angering the pure mathematicians) that whenever the $\textrm{F}\_1$ score is undefined, we say that its value is zero. This uses the false assumption that division of a positve number by zero yields $+\infty$ but is preferred since it allows our metric to function for all confusion matrices with accurate limiting behaviour.

{% colorquote info %}
For those interested, by replacing the references to precision and recall in the formula for the $\textrm{F}\_1$ score with their definitions, it can be shown that it takes a value equal to the accuracy of a model whenever the true positive and true negative values are the same
{% endcolorquote %}


## Why this matters

As discussed in great depth by Virginia Eubank's book [Automating Equality](https://virginia-eubanks.com/books/), we are beginning to live in a world where automated systems - rather than humans - control a large proportion of the way we live; be it socially, economically, or politically. In a perfect world, we would have all of these algorithms thoroughly audited, but that is currently far from the case. Until we get to that stage (of which Cathy O'Neil, the author of [Weapons of Math Destruction](https://weaponsofmathdestructionbook.com/), is building excellent foundations for through her new [algorithmic auditing and risk consulting company](http://www.oneilrisk.com/)) the next best thing we can do is start using a metric that does a decent job of reflecting our goals as data scientists.

The use of statistical accuracy is pervasive throughout the data science community. Every Kaggle competition, machine learning showcase, and PR campaign, relies on it almost in entirety. For many of the budding data scientists who may not come from a rich statistical background, this can be a great danger. It builds bad habits and avoids the discussion of important topics surrounding data ethics. The field is still young and hopefully we will have a chance to right this wrong at least to some extent, before it becomes too ingrained in the standard process.

Is it finally time to concede, and admit the inherent inaccuracy of 'accuracy'?
