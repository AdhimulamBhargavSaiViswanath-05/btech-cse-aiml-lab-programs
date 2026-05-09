# ===============================
# IRIS DATASET – SCATTER PLOTS
# ===============================

# Load dataset
data("iris")

# View first few rows
head(iris)

# Define colors for species
colors <- c(
  "setosa" = "red",
  "versicolor" = "green",
  "virginica" = "blue"
)

# ---------- 1. Basic Scatter Plot ----------
png("iris_sepal_length_vs_width.png", width = 800, height = 600)

plot(
  iris$Sepal.Length,
  iris$Sepal.Width,
  main = "Sepal Length vs Sepal Width",
  xlab = "Sepal Length (cm)",
  ylab = "Sepal Width (cm)",
  col = "blue",
  pch = 19
)

dev.off()

# ---------- 2. Scatter Plot by Species ----------
png("iris_petal_length_vs_width_by_species.png", width = 800, height = 600)

plot(
  iris$Petal.Length,
  iris$Petal.Width,
  main = "Petal Length vs Petal Width by Species",
  xlab = "Petal Length (cm)",
  ylab = "Petal Width (cm)",
  col = colors[iris$Species],
  pch = 19
)

legend(
  "topleft",
  legend = names(colors),
  col = colors,
  pch = 19,
  title = "Species"
)

dev.off()

# ---------- 3. Scatter Plot Matrix ----------
png("iris_scatter_plot_matrix.png", width = 900, height = 900)

pairs(
  iris[, 1:4],
  main = "Scatter Plot Matrix of Iris Data",
  col = colors[iris$Species],
  pch = 19
)

dev.off()

# ---------- 4. Enhanced Scatter Plot Matrix ----------
png("iris_scatter_plot_matrix_colored.png", width = 900, height = 900)

pairs(
  iris[, 1:4],
  main = "Iris Feature Relationships by Species",
  pch = 21,
  bg = colors[iris$Species],
  upper.panel = NULL
)

dev.off()
