# ===============================
# HEXBIN PLOTS – DIAMONDS DATASET
# ===============================

# Load required libraries
library(ggplot2)
library(hexbin)

# Load diamonds dataset
data("diamonds")

# View dataset
diamonds

# View structure and size
str(diamonds)
nrow(diamonds)   # Over 53,000 rows


# ---------- 1. Basic Hexbin Plot ----------
p1 <- ggplot(diamonds, aes(x = carat, y = price)) +
  geom_hex(bins = 50) +
  scale_fill_viridis_c() +
  labs(
    title = "Hexbin Plot: Carat vs Price",
    x = "Carat",
    y = "Price",
    fill = "Count"
  ) +
  theme_minimal()

# Save PNG in current working directory
ggsave(
  filename = "diamonds_hexbin_carat_vs_price.png",
  plot = p1,
  width = 8,
  height = 6,
  dpi = 300
)


# ---------- 2. Hexbin Plot with Plasma Palette ----------
p2 <- ggplot(diamonds, aes(x = carat, y = price)) +
  geom_hex(bins = 40) +
  scale_fill_viridis_c(option = "plasma") +
  labs(
    title = "Hexbin Plot with Plasma Palette",
    x = "Carat",
    y = "Price",
    fill = "Density"
  ) +
  theme_bw()

# Save PNG in current working directory
ggsave(
  filename = "diamonds_hexbin_plasma.png",
  plot = p2,
  width = 8,
  height = 6,
  dpi = 300
)
