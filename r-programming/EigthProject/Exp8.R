# Load dataset
data(mtcars)

# View first few rows
head(mtcars)

# Scale the dataset
mtcars_scaled <- scale(mtcars)

# View scaled data
head(mtcars_scaled)

# -------------------------------
# Heatmap using base R
# -------------------------------

png("mtcars_heatmap_base.png", width = 800, height = 600)

heatmap(
  mtcars_scaled,
  main = "Heatmap of mtcars Dataset",
  col = heat.colors(256),
  scale = "none"
)

dev.off()


# -------------------------------
# Heatmap using pheatmap package
# -------------------------------

library(pheatmap)

png("mtcars_heatmap_pheatmap.png", width = 800, height = 600)

pheatmap(
  mtcars_scaled,
  main = "Heatmap of mtcars Dataset",
  color = colorRampPalette(c("navy", "white", "firebrick3"))(50),
  cluster_rows = TRUE,
  cluster_cols = TRUE
)

dev.off()