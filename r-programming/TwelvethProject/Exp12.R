

# Load libraries
library(maps)
library(mapdata)
library(mapproj)

# Display world map
map("world",
    fill = TRUE,
    col = "lightblue",
    bg = "lightgray")


map("world",
    fill = TRUE,
    col = "lightblue",
    bg = "lightgray",
    border = "black")


map("world",
    regions = "India",
    fill = TRUE,
    col = "orange",
    bg = "lightblue")

map("usa",
    fill = TRUE,
    col = "lightgreen",
    bg = "lightgray")
map("state", fill = TRUE, col = rainbow(50))
map("worldHires", regions = c("India", "China", "Nepal", "Pakistan"),
    fill = TRUE, col = c("green", "orange", "red", "blue"))


