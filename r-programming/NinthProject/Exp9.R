library(leaflet)
library(magrittr)

leaflet() %>%
  addTiles()

leaflet() %>%
  addTiles() %>%
  setView(lng = 78.9629, lat = 20.5937, zoom = 5)

leaflet() %>%
  addTiles() %>%
  addMarkers(lng = 77.5946, lat = 12.9716, popup = "Bangalore")

leaflet() %>%
  addTiles() %>%
  addCircles(lng = 77.2090, lat = 28.6139,
             radius = 50000,
             popup = "Delhi",
             color = "blue")

cities <- data.frame(
  name = c("Mumbai", "Chennai", "Kolkata"),
  lat = c(19.0760, 13.0827, 22.5726),
  lng = c(72.8777, 80.2707, 88.3639)
)

leaflet(cities) %>%
  addTiles() %>%
  addMarkers(~lng, ~lat, popup = ~name)

leaflet() %>%
  addProviderTiles(providers$Esri.WorldImagery) %>%
  setView(lng = 78.9629, lat = 20.5937, zoom = 4)