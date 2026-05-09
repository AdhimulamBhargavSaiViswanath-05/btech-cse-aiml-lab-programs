data(HairEyeColor)

head(HairEyeColor)
typeof(HairEyeColor)
png("Hair_Eye_Sex_Mosaic.png", width = 800, height = 600)

mosaicplot(
  HairEyeColor,
  main = "Hair Color vs Eye Color vs Sex",
  color = TRUE,
  xlab = "Hair Color",
  ylab = "Eye Color"
)

dev.off()

png("Hair_Eye_Female_Mosaic.png", width = 800, height = 600)

mosaicplot(
  HairEyeColor[, , "Female"],
  main = "Hair vs Eye Color (Females)",
  color = TRUE,
  xlab = "Hair Color",
  ylab = "Eye Color"
)

dev.off()

png("Hair_Eye_Female_CustomColors.png", width = 800, height = 600)

mosaicplot(
  HairEyeColor[, , "Female"],
  main = "Hair vs Eye Color (Females)",
  color = c("lightblue", "lightgreen", "lightpink", "wheat"),
  xlab = "Hair Color",
  ylab = "Eye Color"
)

dev.off()

