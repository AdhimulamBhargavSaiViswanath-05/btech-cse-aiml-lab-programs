# Social Media Analysis Algorithm

## Overview
This algorithm analyzes social media data to identify trends, sentiment patterns, and key metrics.

---

## Algorithm Steps

### 1. **Data Loading & Validation**
- Load CSV file containing social media posts
- Verify required columns (text, created_at)
- Handle missing or invalid data

### 2. **Data Preprocessing**
- Convert timestamps to datetime format
- Remove rows with invalid dates
- Create filtered dataset copy

### 3. **Text Cleaning & Extraction**
- Extract mentions (@username)
- Extract hashtags (#tag)
- Remove URLs and links
- Remove special characters
- Normalize whitespace

### 4. **Feature Extraction**
- Extract all hashtags and convert to lowercase
- Extract all user mentions
- Count frequency of hashtags (apply minimum threshold)
- Count frequency of mentions
- Extract sentiment labels if available

### 5. **Named Entity Recognition**
- Apply regex patterns for different entity types:
  - ORGANIZATION
  - PERSON
  - LOCATION
  - HASHTAG
- Filter entities using stopword list
- Count entity frequencies

### 6. **Temporal Analysis**
- Extract date from timestamp
- Group posts by date
- Calculate daily post counts

### 7. **Location Analysis**
- Extract location information
- Count posts per location
- Identify top locations

### 8. **Platform Analysis**
- Count posts per platform
- Generate platform distribution

### 9. **Report Generation**
- Display total post count
- Show time period range
- List top 5 trending hashtags
- Show sentiment distribution with percentages
- Display top 3 locations

### 10. **Visualization**
- Create sentiment distribution pie chart
- Apply color coding (Positive=Green, Negative=Red, Neutral=Gray)
- Save visualization as PNG file
- Display chart to user

---

## Data Structures Used

- **Pandas DataFrame**: Store and manipulate social media data
- **Counter**: Count frequencies of hashtags, mentions, entities
- **Dictionary**: Store configuration parameters and results
- **List**: Store extracted features and entities

---

## Output

1. **Console Report**: Text-based statistics and insights
2. **Visualization**: Sentiment analysis pie chart (PNG file)

---

## Key Features

- No user input required (fully automated)
- Analyzes all data without filters
- Focuses on sentiment as primary metric
- Clean output without emojis/symbols
- Single focused visualization
