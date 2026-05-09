# Load built-in dataset
data("AirPassengers")
# View the start of the dataset
head(AirPassengers)
## Jan Feb Mar Apr May Jun
## 1949 112 118 132 129 121 135
# Simple line chart
plot(AirPassengers,
     main = "Monthly Air Passengers (1949–1960)",
     xlab = "Year",
     ylab = "Number of Passengers (in thousands)",
     col = "blue",
     type = "l",
     lwd = 2)
