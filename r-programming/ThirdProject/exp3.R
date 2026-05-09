# ===============================
# RESET & SETUP
# ===============================
graphics.off()

setwd("D:/R Programming 3-2/ThirdProject")

# Load datasets
data(iris)
data(airquality)
(airquality)
# ===============================
# PART A: IRIS DATASET
# ===============================

# 1. Count of Iris Species
species_count <- table(iris$Species)

png("iris_species_count.png", width = 800, height = 600)
barplot(
  species_count,
  main = "Count of Iris Species",
  xlab = "Species",
  ylab = "Count",
  col = c("lightblue", "lightgreen", "salmon"),
  border = "black"
)
dev.off()

# 2. Average Sepal Length by Species
sepal_means <- tapply(iris$Sepal.Length, iris$Species, mean)

png("iris_avg_sepal_length.png", width = 800, height = 600)
barplot(
  sepal_means,
  main = "Average Sepal Length by Species",
  xlab = "Species",
  ylab = "Mean Sepal Length",
  col = c("skyblue", "lightgreen", "orange"),
  border = "black"
)
dev.off()

# 3. Grouped Bar Chart (Sepal Width & Petal Width)
mean_values <- aggregate(
  cbind(Sepal.Width, Petal.Width) ~ Species,
  data = iris,
  mean
)

grouped_data <- t(mean_values[, 2:3])
colnames(grouped_data) <- mean_values$Species

png("iris_grouped_bar_width.png", width = 800, height = 600)
barplot(
  grouped_data,
  beside = TRUE,
  col = c("dodgerblue", "firebrick"),
  main = "Mean Sepal & Petal Width by Species",
  ylab = "Width (cm)",
  legend.text = rownames(grouped_data)
)
dev.off()

# 4. Stacked Bar Chart
png("iris_stacked_bar_width.png", width = 800, height = 600)
barplot(
  grouped_data,
  beside = FALSE,
  col = c("dodgerblue", "firebrick"),
  main = "Stacked Bar Chart - Sepal & Petal Width by Species",
  ylab = "Total Width",
  legend.text = rownames(grouped_data)
)
dev.off()

# ===============================
# PART B: AIRQUALITY DATASET
# ===============================

# Clean Ozone data
ozone <- na.omit(airquality$Ozone)

# 5. Histogram of Ozone
png("ozone_histogram.png", width = 800, height = 600)
hist(
  ozone,
  main = "Histogram of Ozone Concentration",
  xlab = "Ozone (ppb)",
  col = "lightblue",
  border = "black"
)
dev.off()

# 6. Boxplot of Ozone
png("ozone_boxplot.png", width = 800, height = 600)
boxplot(
  ozone,
  main = "Boxplot of Ozone Concentration",
  ylab = "Ozone (ppb)",
  col = "lightgreen"
)
dev.off()

# 7. Line Plot of Daily Ozone
png("ozone_line_plot.png", width = 800, height = 600)
plot(
  ozone,
  type = "l",
  main = "Daily Ozone Concentration",
  xlab = "Days",
  ylab = "Ozone (ppb)",
  col = "darkblue",
  lwd = 2
)
dev.off()

# 8. Boxplot of Ozone by Month
png("ozone_boxplot_by_month.png", width = 800, height = 600)
boxplot(
  Ozone ~ Month,
  data = airquality,
  main = "Ozone Concentration by Month",
  xlab = "Month",
  ylab = "Ozone (ppb)",
  col = "orange"
)
dev.off()

# ===============================
# CONFIRM SAVED FILES
# ===============================
list.files()
