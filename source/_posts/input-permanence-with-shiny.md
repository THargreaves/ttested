---
title: "Enforcing Input Permanence with Shiny"
date: '2019-10-07'
excerpt: "Shiny is an incredibly tool for building online dashboards and web apps. The crux of Shiny is the concept reactive programming, allowing you to build visualisations and analyses which automatically update with changing user input. Reactivity is complicated though and doesn't always work as you expect so in this post I tackle an issue which I have repeatedly faced in my work and to which a solution I am yet to find online."
thumbnail: /gallery/thumbnails/input-permanence-with-shiny.jpg
toc: true
categories:
- [Data Science]
tags:
- shiny
- tutorial
---

As part of my job at AstraZeneca as a Data Scientist, I have spent a lot of time building [Shiny](https://shiny.rstudio.com/) dashboards. In this work, I have come across a recurring problem in which reactive UI elements have a tendency to reset their stored values to the default. 

This blog post will be extremely short. I plan to detail the problem that I have been facing and then offer a quick solution that I came up with after working on this problem for a while. I couldn't find any discussion of this issue on [Stack Overflow](https://stackoverflow.com/) or on the RStudio forums yet I am sure that it is an issue affecting many people so I hope that this post can be used as a reference for solving the issue.

### The Problem

To help explain the problem that I was encountering, I have made a minimal reproducible example. The code for this is as follows.
{% codeblock lang:R %}
# only run this example in interactive R sessions
if (interactive()) {

    ui <- fluidPage(
    
        titlePanel("Value Permanence"),
    
        sidebarLayout(
            sidebarPanel(
                checkboxInput(
                    'non_primary',
                    'Allow non-primary colours', 
                    value = FALSE),
                uiOutput(
                    'colour_selector'
                )
            ),
    
            mainPanel(
               plotOutput("iris_plot")
            )
        )
    )
    
    server <- function(input, output) {
    
        output$colour_selector <- renderUI({
            palette <- c('blue', 'red', 'yellow')
            if (input$non_primary) {
                palette <- append(palette, c('green', 'orange', 'purple'))
            }
            selectInput(
                'colour',
                'Colour',
                choices = palette
            )
        })
    
        output$iris_plot <- renderPlot({
            plot(
                x = iris$Sepal.Length,
                y = iris$Sepal.Width,
                col = input$colour
            )
        })
    }
    
    shinyApp(ui = ui, server = server)

}
{% endcodeblock %}


To summarise the above code, we create a UI with a side panel and main panel. The side panel contains two inputs. The first is a check box which lets you select whether to use only the primary colours as your palette or to also include secondary colours. The second is a reactive select input. This lets you choose a colour from the current palette. Therefore this select input is a reactive dependent of the check box input. The main panel then contains a plot of the iris data set with the colours of the points set to whichever colour was chosen with the select input. The output looks like this.
![Our Minimal Reproducible Example](/images/input-permanence-with-shiny/example.png)
We can now change the colour selector to update the plot colour without any trouble.
![Changing the Plot Colour](/images/input-permanence-with-shiny/change_colour.png)
The problem arises if we now try to extend the palette to secondary colours by toggling the check box. This will re-render the select input so that its choices include secondary colours but in doing so it will reset the value to the default (blue - since this is the first item in the vector of choices).
![The Colour Has Been Reset](/images/input-permanence-with-shiny/input_reset.png)
We are now free to set the colour input to any primary or secondary colour.
![Using Secondary Colours](/images/input-permanence-with-shiny/extra_colours.png)
This may not seem like much of an issue but imagine if we scale up this app. We now have 10 inputs all dependent on one other input. Changing the parent input may only need us to change a few of the dependent inputs or perhaps even none and yet they will all get reset every time we make a change. With behaviour like that, it would be unlikely that any user would be bothered to make it passed 5 minutes of use with your app.

### The Solution

The solution is annoying simple. It took me a while to get to this and I had many failed attempts but now that I have a working solution, I'm glad that it is very easy to implement. The only tweaks that need to be made are to the server code so I will just show that and walk through the changes made right after.
{% codeblock lang:R %}
server <- function(input, output) {
    
    # make sure this is before output$colour_selector
    current_colour <- eventReactive(input$non_primary, {
        input$colour
    })
    
    output$colour_selector <- renderUI({
        palette <- c('blue', 'red', 'yellow')
        if (input$non_primary) {
            palette <- append(palette, c('green', 'orange', 'purple'))
        }
        selectInput(
            'colour',
            'Colour',
            choices = palette
            selected = current_colour()
        )
    })

    output$iris_plot <- renderPlot({
        plot(
            x = iris$Sepal.Length,
            y = iris$Sepal.Width,
            col = input$colour
        )
    })
}
{% endcodeblock %}


There are two additions to the original code. The first is creating a reactive value `current_colour` which is invalidated every time that the check box is toggled. The other is setting `select = current_colour()` in the `selectInput` definition.

To explain why these changes fix our problem, let's walk through the reactive process when we first toggle the check box input to add secondary colours.

Suppose that we currently have selected some colour other than the default blue. We toggle the check box and this invalidates both `current_colour()` and `output$colour_selector` (and in turn, `output$iris_plot`). Since `current_colour` is defined before the colour selector, this is re-rendered first, setting its value to the current colour selected. We then move on to re-rendering the select input with the updated palette. The difference is that we now set the default value of this updated input to be `current_colour()` which we know currently stores the previous colour and so the input is preserved.

The reactive-conscious of you may worry about the change to `input$colour` by resetting the selecting leading to a further update of `current_colour()` and hence an infinite loop. Thankfully, this does not happen as the the second argument of `eventReactive()` is isolated from reactivity.

Another concern may be what happens when we toggle the checkbox back to primary colours only when we have a secondary colour selected; won't we then be setting `selected` to an invalid value. The answer is, yes, we are. But that's nothing to worry about. When we pass an invalid selection to a `selectInput` declaration, it just defaults to the first value in the choices vector and so we go back to blue. In this case, it makes sense to reset the input so this isn't a problem.

Try out the improved code for yourself and verify that it does indeed work. I hope you have fun implementing input permanence in your future Shiny projects.
