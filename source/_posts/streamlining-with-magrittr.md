---
title: "Streamlining Your Data Science Workflow With Magrittr"
date: '2018-10-21'
excerpt: "The Tidyverse is here to stay so why not make the most out of it? The `magrittr` package extends the basic piping vocabulary of the core Tidyverse to facilitate the production of more intuitive, readable, and simplistic code. This post aims to be an all encompassing guide to the package and the benefits it provides."
thumbnail: /gallery/thumbnails/streamlining-with-magrittr.jpg
toc: true
categories:
- [Data Science, Best Practice]
tags:
- tutorial
- r
- tidyverse
- magrittr
---

Packages required for this post:


{% codeblock lang:R %}
suppressPackageStartupMessages(library(dplyr)) # manipulating data
library(ggplot2) # data visualisation
library(magrittr) # piping (to be elaborated on throughout the post)
{% endcodeblock %}



    Warning message:
    "package 'ggplot2' was built under R version 3.6.1"

# Getting to know magrittr

*Magrittr* (pronounced with a sophisticated French accent, as per the introductory vignette) is an incredibly powerful R package that forms the foundation of the [tidyverse](https://www.tidyverse.org/). In my personal opinion, it is one of the most underrated packages in the R ecosystem. Without its existence, my productivity in R would be severely hampered.

The most fundamental tool this package offers is called the  "pipe" operator, `%>%`. The purpose of this operator is to take the value on the left hand side (LHS) and pass it into whatever function call is on the right hand side (RHS) as the first argument. In other words, if you write something along the lines of `x %>% f()`, this will be evaluated as `f(x)`. More generally if your function already has some filled parameters as in `x %>% f(y, z)`, this is evaluated as `f(x, y, z)`. This lets you produce chunks of code called "pipelines" which use multiple pipe operators to create a continual flow of functions, the output of one being passed on to the next such as in this example.


{% codeblock lang:R %}
# data manipulation without magrittr
cars_subset <- filter(mtcars, mpg > 15)
cars_grouped <- group_by(cars_subset, cyl)
cars_aggregate <- summarise(cars_grouped, mean = mean(disp))
cars_sort <- arrange(cars_aggregate, desc(mean))
cars_sort
{% endcodeblock %}




<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script >$(document).ready( function () {$('#table0').DataTable();} );</script>
<table id="table0" class="display">

<thead>
	<tr><th scope=col>cyl</th><th scope=col>mean</th></tr>
	<tr><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th></tr>
</thead>
<tbody>
	<tr><td>8</td><td>320.0500</td></tr>
	<tr><td>6</td><td>183.3143</td></tr>
	<tr><td>4</td><td>105.1364</td></tr>
</tbody>
</table>




{% codeblock lang:R %}
# data manipulation with magrittr
mtcars %>% 
  filter(mpg > 15) %>%
  group_by(cyl) %>%
  summarise(mean = mean(disp)) %>%
  arrange(desc(mean))
{% endcodeblock %}




<script >$(document).ready( function () {$('#table1').DataTable();} );</script>
<table id="table1" class="display">

<thead>
	<tr><th scope=col>cyl</th><th scope=col>mean</th></tr>
	<tr><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th></tr>
</thead>
<tbody>
	<tr><td>8</td><td>320.0500</td></tr>
	<tr><td>6</td><td>183.3143</td></tr>
	<tr><td>4</td><td>105.1364</td></tr>
</tbody>
</table>



As you can see, we get the exact same result in either. However, there is no question that the second method, using *magrittr*, is easier to follow and is far simply to write due to its reduced code duplication. Using *magrittr* lets you avoid the use of any temporary variables such as `cars_grouped` and `cars_sort` and lets you produce one long pipeline with each function leading naturally into the next. Furthermore, using the pipe operator makes your code far more interpretable to anyone less tech-savvy. The pipeline is written in the same way that you would describe the data manipulation process: take the data, filter it for certain MPG, group by number of cylinders, find the mean of each group, arrange the rows using this mean in descending order and print the output. If you've never seen *magrittr* before, I hope that this example confirms its place in your data science tool-kit.

Anyone familiar with the use of tidyverse packages, though, will most likely recognise this operator. This is because it is included in the packages `dplyr` and `tidyr` - tidyverse packages for data manipulation and tidying respectively- and most likely others too. Paradoxically, this inclusion is in fact unfavourable for *magrittr*'s full adoption as it leads many people to believe that this is as far as piping in R reaches, but that is far from the truth. Using the *magrittr* package directly (as opposed to through another tidyverse package), gives you access to several other pipe operator variants which offer you even more power over your workflow. Furthermore there are plenty of tricks involving *magrittr* that many people are unaware of. In this blog post, I wish to give a thorough introduction to the main features of the package through the use of practical examples. I hope that I can convince you that *magrittr* is truly one of the most important packages in the R ecosystem for the productive developer.

# Further pipe operators

{% colorquote info %}
All printing has been disabled in this post to avoid adding unnecessary baggage. All of the examples are self-contained however so if you which to see their output, you can simply copy the chunks to your own R session and run them, provided you have dplyr and magrittr installed and loaded.
{% endcolorquote %}


Alongside the standard piping operator `%>%`, *magrittr* offers three related operators which offer similar functionality but with slightly different execution. These may not be used as frequently as %>% but they are still extremely important to have familiarity with for the special cases in which they can be effectively utilised.

### The compound assingment operater

The first additional operator we look as is called the compound pipe operator. This is implemented using `%<>%`. The effect of this is very similar to `%>%`, except rather than simply piping the LHS into the first argument of the RHS and evaluating it, the result of this process is then assigned to the LHS as its new value. This is essentially shorthand for `x <- x %>% f()`, which is instead being replaced with `x %<>% f()`. This can be combined with multiple instances of the regular pipe to create pipelines designed to manipulate an existing object. Here is an example use of the compound assignment operator using the iris data set.
{% codeblock lang:R %}
iris_sample <- iris[sample(nrow(iris), 30), ]
iris_sample %<>% filter(Species != "setosa") %>%
  select(Sepal.Length, Sepal.Width) %>%
  arrange(Sepal.Length, Sepal.Width)
{% endcodeblock %}


### The tee operator

The tee operator, `%T>%`, is also rather similar in function to the standard pipe, except rather than returning the result of evaluating the RHS, it instead returns the LHS. For example if you were to run `x %T>% f`, R would run `f(x)` but will return `x` instead of `f(x)`. This is useful for when the function you are piping into is used for its side-effects (e.g. plotting, printing) rather than the value it returns. This then lets you carry on your pipeline rather than having to halt abruptly when a function doesn't return a useful value. An example use of this is generating a plot mid-pipeline as shown here.
{% codeblock lang:R %}
sample(1:100, size = 50) %>%
  cbind(sample(1:100, size = 50)) %T>%
  plot() %>% # plot is used for its side-effect
  colMeans() %>% # the result of cbind is passed into here
  diff()
{% endcodeblock %}


#### A word of warning

Despite the many amazing things *magrittr* can do to help you supercharge your R productivity, it does have its idiosyncrasies. The most prevalent of which is that it doesn't play well with *ggplot2*. This is due to the operator precedence (think BIDMAS/PEMDAS but for all operators R uses such as `&`, `!`, `$`, etc.) that R employs, which evaluates the *magrittr* pipe operators before the *ggplot2* plus operator (which is actually just a specific method of the S3 class for binary addition). This means that if we write some code like the following, with the goal of taking some data, plotting it, and then carrying on with data manipulation we receive an error.
{% codeblock lang:R %}
iris %T>%
  ggplot(aes(x = Sepal.Length, y = Sepal.Width)) +
    geom_point() %>%
  filter(Petal.Length < 2) %>%
  head()
{% endcodeblock %}





    Warning message in eval(expr, envir, enclos):
    "Error in UseMethod("filter_") : 
    no applicable method for 'filter_' applied to an object of class 
    "c('LayerInstance', 'Layer', 'ggproto', 'gg')""

This is because the R interpreter will evaluate
{% codeblock lang:R %}
geom_point() %>%
  filter(Petal.Length < 2) %>%
  head()
{% endcodeblock %}


first. Which gives an error since `filter` has no idea what to do when it is passed a ggplot object as its first argument rather than a data frame. To avoid this issue we have to explicitly tell the interpreter to evaluate the plus operator before the pipe operators using bracketing. Note, that since auto-printing is disabled inside brackets, we have to explicitly tell R to print the ggplot object using `print`.
{% codeblock lang:R %}
iris %T>%
  {print(ggplot(., aes(x = Sepal.Length, y = Sepal.Width)) +
    geom_point())} %>%
  filter(Petal.Length < 2) %>%
  head()
{% endcodeblock %}


This somewhat diminishes the clarity *magrittr* is designed to introduce to your code but I would argue that is still more elegant than creating a temporary variable or having code duplication, one pipeline leading to the plot, the other to the further data manipulation functions. Furthermore, if you are familiar with this behaviour and its typical solution, it isn't as off-putting as on first glance. To learn more about operator precedence in R, use `?Syntax` in the console.

### The exposition operator

Finally, the last *magrittr* pipe we have to discuss is the exposition operator. Of the three additional pipe operators, this is the one most unlike `%>%`. As the name perhaps suggests, it it used to expose the names contained within the LHS object to the RHS. This lets you use the names directly in the RHS without having to prefix them with the likes of `object$`. For example, if you wanted to evaluate in the form `f(x$a, x$b, x$c)`, you could use the exposition operator to write this as `x %$% f(a, b, c)`. This is really useful when the function on your RHS does not have a `data` argument in the way that `lm` or `aggregate` do. Here is an example of its use.
{% codeblock lang:R %}
Orange %>%
  filter(Tree == 1) %$%
  cor(age, circumference)
{% endcodeblock %}


# Tips and tricks to supercharge your magrittr usage

### Piping as a later argument

So far, we have only considered pipes in which the LHS is used as the first argument of the RHS function. The flexibility of *magrittr* means that this isn't the only way we can do things. What the pipe operators will in fact do is use the LHS as the first *unspecified* parameter. This means that if you want to use the LHS input as the 3rd argument of a function, all you have to do is give values for the first two parameters using named values. For example if we wanted choose a random number from a uniform distribution on $[0,1]$ and use this as the variance for a sample of normal variables, we would do this as follows.
{% codeblock lang:R %}
runif(n = 1) %>%
  rnorm(n = 20, mean = 0)
{% endcodeblock %}


### Using placeholders

*Magrittr*'s plasticity doesn't even end there! The package also lets you make use of what are called "place-holders". These are implemented using the period symbol and will be replaced with the LHS input when they are evaluated. For example the code `x %>% f(5, nrow(.), .^2)` will be evaluated as `f(5, nrow(x), x^2)`. This lets you completely remove any duplication of `x` in the RHS function call. This method can be extended to very complex scenarios by using curly braces to enclose a series of statements such as in this example.
{% codeblock lang:R %}
sample(1:10, size = 5) %>%
{ 
  if (sum(.) > 25)
    max(.)
  else min(.)
}
{% endcodeblock %}


Using place-holders also allows you to use *magrittr* with not only functions, but expressions to. You simply write out the expression as normal, replacing any instance of RHS with a period and then enclose it in curly braces. For example we can use this to normalise a random sample of integers.
{% codeblock lang:R %}
sample(1:100, size = 10, replace = FALSE) %>%
  {(. - min(.)) / (max(.) - min(.))}
{% endcodeblock %}


### Pipes and binary operators

The last feature of *magrittr* that I wish to discuss is how it can be used with binary operators. In fact, there is a way to force *magrittr* to work with such operators using standard R code. This uses the trick that operators can be called in a similar style to functions by enclosing them in single quotes and giving them two arguments to be used as the right and left hand side of the operator. For example we can write `4 + 5` as `` `r '\x60+\x60(4, 5)'` `` or `x[4]` as `` `r '\x60[\x60(x, 4)'` ``. You can then pipe into these functions using *magrittr*.

This is a far from an ideal solution so its lucky that the package offers a set of helper functions called "aliases" designed to make this process easier. Examples of such functions include `extract()`, `add()` and `divide_by` though there are plenty more. You can find a whole list of them by using `?extract` after *magrittr* is loaded. Here is an example use.
{% codeblock lang:R %}
matrix(runif(100, max = 10), nrow = 10) %>%
  mod(10) %>% # alias for `%%`
  multiply_by_matrix(t(.)) %>% # alias for `%*%`
  equals(t(.)) %>% # alias for `==`
  all()
# should return TRUE as any matrix multiplied by its transpose is symmetric
{% endcodeblock %}

