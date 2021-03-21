---
title: "Integrating Hexo and Jupyter to Build a Data Science Blog"
date: '2019-08-20'
excerpt: "When creating a data science blog, there are many different approaches that can be taken. The main two decisions revolve around how you wish to write your content and which static site generator you wish to use to build your site. For the last year I have been using RStudio, Blogdown, and Hugo to achieve this but - after much deliberation - I have decided that change is needed. This blog post follows my transition to building a data science blog powered by Jupyter and Hexo, the obstacles I came up against, and the solutions I came to employ."
thumbnail: /gallery/thumbnails/integrating-hexo-and-jupyter.png
toc: true
categories:
- [Meta]
tags:
- python
- web-development
- tutorial
---
We all know the saying, "New Year, New (The)me". Inspired by that thought - or perhaps just by the idea of using that as an opener - I decided that I would begin the 2019/20 academic year by re-theming this blog. This was meant to be a short and sweet project; move some files, install some packages, and off we go. That couldn't have been further from the truth. In transitioning, I have come across many challenges regarding the immaturity of the integration between static site generators and Jupyter. I have spent considerable time over the summer remedying such issues, and I hope that by documenting my struggles and eventual solutions in this post, I can make a similar move much simpler for anyone doing so in the future.

## Hugo and Blogdown

When I first created this blog almost a year ago, I decided to use Hugo as the static site generator behind the site. Reaching this decision was simple. At that time, I was only using R for any data science work and RStudio offered an easy-to-use set of add-ins built upon the `blogdown` package. This made the production of a data science blog a piece of cake. You could build your site directly in RStudio using interactive R notebooks. These would then be processed automatically by the package and converted into a form ready for Hugo to work with. 

This worked well for me for several months but I soon started to grow fed up with system for the following reasons.

### Language Agnosticism

I am a strong believer in using the right tool for the right job. And through this philosophy, I soon realised that solely using R wasn't going to cut it for complicated projects. I wanted to be learning about and discussing the use of other languages for data science. Currently this has only amounted to a splattering of posts using Python and Bash, but I have plans to be including many more languages in my projects in the future. I therefore want to make sure that I am using a system that is language agnostic and easily expandable.

RStudio and Blogdown is not such a system. Although it is technically possible to use Python, SQL, and Bash code in R notebooks, the experience is buggy and generally unpleasant. There is a clear preference towards blogging in R. Although this is the main language I use at the moment, who knows what the data science landscape will look like in five years? And so, I decided that it was time to move away from such a tight-knit ecosystem.

On top of this, when it comes to sharing my code on GitHub, supplying people with an R notebook is not generally helpful. If this notebook contains R code then that makes sense, but if it is written for a different language then it is unlikely that the intended user of the notebook will even have RStudio installed and so won't be able to open it.

### Static Site Generation

Hugo is a good tool for static site generation, but it is not for me. I don't like the available themes, the limited extendability, the manual configuration of the site. It just doesn't sit well with me, even though I can understand why many people would like it.

The Blogdown package defaults to using Hugo as its static site generator and although it is _possible_ to set up the package to use a different generator, the documentation on this is limited and many features - such as syntax highlighting stop working.

I want a website that is modern and feature-rich. This means tools such as site search, hierarchical categorisation, and customisable word-count/reading-time by default. Hugo almost certainly has the potential to add these features but this would require some serious graft and I do not have the time or skills for that.

## Hexo and Jupyter

It was clear that I was finding Blogdown and Hugo frustrating but I hadn't considered any alternatives. I then stumbled across [this](https://www.dataquest.io/blog/how-to-setup-a-data-science-blog/) blog post on [dataquest.io](https://www.dataquest.io/). This still wasn't exactly what I wanted - Pelican themes are painfully minimal in both features and design - but it started the ball rolling. I then came across [this](https://github.com/ppoffice/hexo-theme-icarus) GitHub repository for a Hexo theme called Icarus. Now that was exactly what I wanted. The theme is gorgeous, the documentation for Hexo looked clear and intuitive, and using the ideas from the DataQuest blog post, I cloud easily integrate it with Jupyter notebooks (or so I thought).

I installed Hexo, downloaded the theme, filled out the config files, and opened a single post from my old Blogdown site to use as a test. I copied the Markdown and code chunks from the original file into a Jupyter notebook (using the R kernel), converted it to markdown with `jupyter nbconvert --to markdown path/to/file`, and voilà...it didn't work.

Well, it did work, just not as I expected. There were several issues that needed to be fixed. Hours became days, days became weeks, and soon I was wondering whether it would be easier to just use a Dropbox folder full of TXT files for my website. I did, however, manage to fix the major issues. So let's begin walking through them, and seeing how I came to a solution.

### Syntax Highlighting

We'll start simple. When I first generated by Hexo site I noticed that none of the code blocks had syntax highlighting. This was strange since the Icarus theme definitely included highlight.js and yet all codeblocks featured only large blocks of matte grey text. Looking through the [Icarus documentation](https://blog.zhangruipeng.me/hexo-theme-icarus/categories/) I soon realised what was wrong.

There was a clear disparity between the way that the Jupyter notebook converter and Hexo defined codeblocks. This syntax for the former uses triple backticks to open close a codeblock. Whereas the latter uses a more verbose tag notation shown [here](https://hexo.io/docs/tag-plugins.html#Code-Block). I would like to include examples of these in this post but I can't find a way to stop the Hexo render no matter how I try to escape them so you will just have to use your imagination.

This is very easy to fix using a simple pattern-replace regular expression. For the same reason as above, I cannot include the code directly in this post but, as you will see later, I have created a Python script which you can download to fix all of these issues automatically.

### Image Directories

Arguably, this problem has an even simpler solution than the first. The root of this issue is that the notebook converter places all outputted figures into a folder called `{name-of-post}_files` and then points all image links in the markdown file to that folder. This needs to be changed to the actual directory that you will be storing such images. Since this change is the same every time, you don't even require any regex; a simple call to the `.replace()` string method will do the trick although I did end up going for regex for simplicity.

### LaTeX issues

In almost all cases, LaTeX works the same both with Hugo and with Hexo. I have however noticed some edge-cases that needed fixes. For a start, the `align*` environment (align environment without line numbering) does not work with Hexo.  This is because the asterisk is interpreted as italics before the MathJax engine renders the LaTeX code. Instead you can use the standard `align` environment which for some reason doesn't have line numbers when used with Hexo.

Another point to note is that the standard `//` new-line notation does not work as expected. This is because the first slash is used to escape the second, leaving only one slash for MathJax to render. The solution to this is simple - replace every occurrence of two slashes with four.

### Figure Options

When writing a blog post using Blogdown, it was possible to format the figure output of any block of code by using chunk options. Jupyter and Hexo do not offer such functionality although there is a work around. 

#### Figure Size

When creating Python plots using `matplotlib`, this is trivial; you simply specify the `figsize` parameter when calling `matplotlib.figure()`. But what about with other kernels? So far I have only been generating figures with R and so I only have a solution for that language, however I will edit this post with updates if/when I use others. 

To format figure output when using R, all you have to do is start the relevant code cell with a call to the `options()` function as so.
{% codeblock lang:R %}
options(repr.plot.width=8, 
        repr.plot.height=5,
        jupyter.plot_mimetypes = "image/png")
{% endcodeblock %}{% colorquote info %}
The MIME type can also be set to `image/svg+xml` which will output an SVG or `image/jpeg` for a JPEG.
{% endcolorquote %}{% colorquote warning %}
For this to run you will need to have install the `repr` package from GitHub with `devtools::install_github('IRkernel/repr')` though it doesn't need to be loaded.
{% endcolorquote %}
The call to this function can then be removed from the Markdown file using the following regular expression `r'options\((?:(?!\()(?:.|\s))*\)\s*'`

#### Figure Alignment

Using R notebook chunk properties, it is possible to set figure alignment to one of `left`, `center`, or `right`. I have not found a way to do this with Jupyter. This, however, has not presented an issue since I would like all my figures to be centred. Hence, I just tweaked the CSS properties related to blog post images to get the desired result.

#### Figure Caption

Another useful feature of the `blogdown` package is the ability to set a figure caption using chunk options. This is a feature that I really wanted to replicate but there appeared to be no standard way of doing so. The [source code](https://github.com/IRkernel/repr/blob/master/R/options.r) for the `options()` function makes no mention of figure captions. Instead, the caption created by `nbconvert` is just the file type of the image. For example if you used `image/svg+xml` for the MIME type, the figure caption would be `svg`. 

I decided that the best way to fix this was to use a Python script. This will run through each line of the outputted markdown file and look for the pattern `@caption="This is the caption"`. The script will then extract the caption text and then carry on searching through the file until it finds an caption-less image, denoted by `![svg](/path/to/image)` or similar. The script can then replace the default caption with the caption it is storing from the line above.

Therefore, to use this script, all you have to do is add a cell of type `Raw NBConvert` containing `@caption="..."` before your figure-producing cell and then the rest is handle automatically.

### Other Chunk Properties

The above fixes were really quite simple once I knew which direction to head in, but this last issue gave me a bit more of a headache. Never-the-less, I did eventually come to rather simple solutions. These problems revolve around the R notebook chunk options `eval` and `echo`. These, respectively, tell R to either not run a chunk of code or to only show the output of a chunk and not the code that produced it. 

The former of these is easy to replicate with Jupyter/Hexo. You simply replace the code cell with a `Raw NBConvert` cell containing manually entered codeblock tags.

The latter, however, required some thought. In the end, I decided to use a solution similar to the one before for figure captions. This means that before any cell you don't wish to echo, you need to add a `Raw NBConvert` cell containing the command `@noecho`. Then we can use the regular expression `r'@noecho(?:.|\s)*?endcodeblock %}'`. This uses the lazy regex quantifier `*?` to only remove code between the call for `@noecho` and the next closing codeblock tag.
{% colorquote danger %}
When using the script provided in the next section, it is import to make sure that any manually entered codeblocks following the `@noecho` tag are closed else any output/text between that block and the next will be removed.
{% endcolorquote %}
### Summary

I have packaged up these tweaks into a short Python script which can be run on a Markdown file outputted by `nbconvert`. It can be found [here](/files/markdown_formatter.py). It is worth noting that I have also added a few edits to the theme's CSS file. I did not make a list of these but none of them were difficult to discover by using the Chrome page inspector tool. 

That concludes the main part of this post. I do however have a few more words to add on the use of colourful quotes and the remaining problems which I have been unable to solve.

## Colourful Quotes

The author of the Icarus theme, [ppoffice](https://github.com/ppoffice/) has also created a Hexo theme called [Minos](https://github.com/ppoffice/hexo-theme-minos) (sensing a pattern?). The theme is a bit too minimalist for my liking but it does have a feature that I really love — colorquotes. You will see these dotted all over this site and even on this page. There are four variants as shown below.
{% colorquote info %}
**Info**
{% endcolorquote %}

{% colorquote success %}
**Success**
{% endcolorquote %}

{% colorquote warning %}
**Warning**
{% endcolorquote %}

{% colorquote danger %}
**Danger**
{% endcolorquote %}
These are not usually a part of the Icarus theme but can be added as so.

First you need to register a `colorquote` extend tag. This is done by creating a file called `colorquote.js` in the directory `themes/icarus/scripts` containing the following.
{% codeblock lang:js %}
/**
* Color Quote Block Tag
* @description Color Quote Block
* @example
*     <% colorquote [type] %>
*     content
*     <% endcolorquote %>
*/

hexo.extend.tag.register('colorquote', function (args, content) {
    var type =  args[0];
    var mdContent = hexo.render.renderSync({text: content, engine: 'markdown'});
    return '<blockquote class="colorquote ' + type + '">' + mdContent + '</blockquote>';
}, {ends: true});
{% endcodeblock %}
You can then edit the main CSS file for the theme. This can be found at `themes/icarus/source/css/style.styl`. All you need to do is add the following as a top-level declaration.
{% codeblock lang:css %}
blockquote
  position: static
  font-family: font-serif
  font-size: 1.1em
  padding: 10px 20px 10px 54px
  background: rgba(0,0,0,0.03)
  border-left: 5px solid #ee6e73
  &:before
    top: 20px
    left: -40px
    content: "\f10d"
    color: #e2e2e2
    font-size: 32px;
    font-family: FontAwesome
    text-align: center
    position: relative
  footer
    font-size: font-size
    margin: line-height 0
    font-family: font-sans
    cite
      &:before
        content: "—"
        padding: 0 0.5em
.colorquote
  position: relative;
  padding: 0.1em 1.5em;
  color: #4a4a4a;
  margin-bottom: 1em;
  &:before
    content: " ";
    position: absolute;

    top: 50%;
    left: -14.5px;
    margin-top: -12px;
    width: 24px;
    height: 24px;

    border-radius: 50%;
    text-align: center;

    color: white;
    background-size: 16px 16px;
    background-position: 4px 4px;
    background-repeat: no-repeat;
  &.info
    border-color: hsl(204, 86%, 53%);
    background-color: hsl(204, 86%, 93%);
    &:before
      background-color: hsl(204, 86%, 53%);
      background-image: url("../images/info.svg");
  &.success
    border-color: hsl(141, 71%, 48%);
    background-color: hsl(141, 70%, 88%);
    &:before
      background-color: hsl(141, 71%, 48%);
      background-image: url("../images/check.svg");
  &.warning
    border-color: hsl(48, 100%, 67%);
    background-color: hsl(48, 100%, 91%);
    &:before
      background-color: hsl(48, 100%, 67%);
      background-image: url("../images/question.svg");
  &.danger
    border-color: hsl(348, 100%, 61%);
    background-color: hsl(348, 100%, 85%);
    &:before
      background-color: hsl(348, 100%, 61%);
      background-image: url("../images/exclamation.svg");
{% endcodeblock %}
You will then need to copy the files `check.svg`, `exclamation.svg`, `info.svg`, and `question.svg` from the [Minos repository](https://github.com/ppoffice/hexo-theme-minos/tree/master/source/images) to the directory `themes/icarus/images`.

By this point, the colorquote blocks will work just fine as long as you do not intend to nest a codeblock inside of them. If you wish to do this then you will need to add one more JavaScript file called `tags.js` under `themes/icarus/scripts` with the following content.
{% codeblock lang:js %}
/**
* Tags Filter
* @description Fix the code block using ```<code>``` will render undefined in Nunjucks
*              https://github.com/hexojs/hexo/issues/2400
*/

const rEscapeContent = /<escape(?:[^>]*)>([\s\S]*?)<\/escape>/g;
const placeholder = '\uFFFD';
const rPlaceholder = /(?:<|&lt;)\!--\uFFFD(\d+)--(?:>|&gt;)/g;
const cache = [];
function escapeContent(str) {
  return '<!--' + placeholder + (cache.push(str) - 1) + '-->';
}
hexo.extend.filter.register('before_post_render', function(data) {
  data.content = data.content.replace(rEscapeContent, function(match, content) {
    return escapeContent(content);
  });
  return data;
});
hexo.extend.filter.register('after_post_render', function(data) {
  data.content = data.content.replace(rPlaceholder, function() {
    return cache[arguments[1]];
  });
  return data;
});
{% endcodeblock %}
## Remaining Issues

Before I close off this post, I would like to discuss the Jupyter/Hexo integration issues that I have not been able to solve. This may be just for cathartic purposes or perhaps someone may be able to suggest a workaround that I have not yet considered. If I do find a solution to any of these issues in the future then I will certainly update this next section.

### Inline Code

R notebooks offer a great feature where you can run code whilst in a markdown block using the notation `` `r print("Hello World")` ``. In these inline blocks you can also reference variables from the main code chunks. This is incredibly useful when your code has an element of randomness to it and you wish to quote the results that a main code block gave in some explanatory text below. I do not believe there is a simple way to do this and so I have instead resorted to setting random seeds. This works for some cases but not for those such as benchmarking.

### Caching

Another nifty feature of R notebooks is the ability to cache chunk outputs. This means that if you have a long-running piece of code, you can run it once and then store the output for future use. This is more an issue of convenience then actual practicality and so it's not a priority for me to solve right now.

### GIFs

As a proponent of animated visualisations, I am partial to the creation of GIFs in my posts. As mentioned before, the only valid MIME types for R output are PNG, JPEG, and SVG. Therefore GIFs have to be generated separately to the main post and embed using Markdown code. Again, this works fine, although seamless integration would be nice.
