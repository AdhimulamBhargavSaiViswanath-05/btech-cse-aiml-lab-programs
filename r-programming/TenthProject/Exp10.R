# Load required libraries
library(car)
library(lattice)
library(latticeExtra)

# Load dataset
data(iris)

# Display first rows
head(iris)

# 3D Scatter Plot
scatter3d(Sepal.Length ~ Sepal.Width + Petal.Length,
          data = iris,
          groups = iris$Species,
          surface = FALSE,
          ellipsoid = TRUE)

# 3D Cloud Plot
cloud(Sepal.Length ~ Sepal.Width * Petal.Length,
      data = iris,
      groups = Species,
      auto.key = TRUE,
      screen = list(x = -60, y = 60),
      par.settings = list(axis.line = list(col = "transparent")))

# XY Plot
xyplot(Sepal.Length ~ Petal.Length | Species,
       data = iris,
       groups = Species,
       layout = c(3, 1),
       auto.key = TRUE,
       type = c("p", "r"),
       col = c("blue", "green", "red"))