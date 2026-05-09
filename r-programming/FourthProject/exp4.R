# ===============================
# IRIS DATASET VISUALIZATIONS
# ===============================

# Load iris dataset
data("iris")

# View first few rows
head(iris)

# ---------- 1. Single Boxplot: Sepal Length ----------
png("iris_sepal_length_single.png", width = 800, height = 600)
boxplot(
  iris$Sepal.Length,
  main = "Boxplot of Sepal Length",
  ylab = "Sepal Length (cm)",
  col = "lightblue"
)
dev.off()

# ---------- 2. Sepal Length by Species ----------
png("iris_sepal_length_by_species.png", width = 800, height = 600)
boxplot(
  Sepal.Length ~ Species,
  data = iris,
  main = "Sepal Length by Species",
  xlab = "Species",
  ylab = "Sepal Length (cm)",
  col = c("lightblue", "lightgreen", "lightpink")
)
dev.off()

# ---------- 3. Multiple Boxplots (2x2) ----------
png("iris_all_features_by_species.png", width = 900, height = 900)
par(mfrow = c(2, 2))

boxplot(
  Sepal.Length ~ Species,
  data = iris,
  main = "Sepal Length",
  col = c("tomato", "skyblue", "palegreen")
)

boxplot(
  Sepal.Width ~ Species,
  data = iris,
  main = "Sepal Width",
  col = c("tomato", "skyblue", "palegreen")
)

boxplot(
  Petal.Length ~ Species,
  data = iris,
  main = "Petal Length",
  col = c("tomato", "skyblue", "palegreen")
)

boxplot(
  Petal.Width ~ Species,
  data = iris,
  main = "Petal Width",
  col = c("tomato", "skyblue", "palegreen")
)

par(mfrow = c(1, 1))
dev.off()

# ---------- 4. Boxplot using RColorBrewer ----------
library(RColorBrewer)

species_colors <- brewer.pal(3, "Set2")

png("iris_petal_length_palette.png", width = 800, height = 600)
boxplot(
  Petal.Length ~ Species,
  data = iris,
  main = "Petal Length by Species",
  col = species_colors,
  xlab = "Species",
  ylab = "Petal Length (cm)"
)
dev.off()


# ===============================
# AIRQUALITY DATASET VISUALIZATIONS
# ===============================

# Load dataset
data("airquality")

# View structure
str(airquality)

# ---------- 5. Individual Boxplots (2x2) ----------
png("airquality_individual_boxplots.png", width = 900, height = 900)
par(mfrow = c(2, 2))

boxplot(
  airquality$Ozone,
  main = "Ozone (ppb)",
  col = "lightblue",
  ylab = "ppb"
)

boxplot(
  airquality$Solar.R,
  main = "Solar Radiation",
  col = "orange",
  ylab = "Langley"
)

boxplot(
  airquality$Wind,
  main = "Wind Speed",
  col = "lightgreen",
  ylab = "mph"
)

boxplot(
  airquality$Temp,
  main = "Temperature",
  col = "tomato",
  ylab = "°F"
)

par(mfrow = c(1, 1))
dev.off()

# ---------- 6. Combined Boxplot ----------
air_data <- na.omit(airquality[, c("Ozone", "Solar.R", "Wind", "Temp")])

png("airquality_combined_boxplot.png", width = 800, height = 600)
boxplot(
  air_data,
  main = "Box Plots of Air Quality Parameters",
  col = c("lightblue", "orange", "lightgreen", "tomato"),
  ylab = "Value"
)
dev.off()
