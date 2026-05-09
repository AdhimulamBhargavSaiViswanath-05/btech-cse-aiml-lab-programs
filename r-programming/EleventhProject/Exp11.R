# Load required package
library(corrplot)

# Load iris dataset
data(iris)

# Select only numeric columns
iris_num <- iris[, 1:4]

# Display first few rows
head(iris_num)

# Compute correlation matrix
cor_matrix <- cor(iris_num)

# Display correlation matrix
print(cor_matrix)

# Plot correlogram
corrplot(cor_matrix, method = "circle")

corrplot(cor_matrix, method = "color",
         col = colorRampPalette(c("red", "white", "blue"))(200),
         type = "upper", order = "hclust",
         addCoef.col = "black",  # Add correlation coefficients
         tl.col = "black", tl.srt = 45)

