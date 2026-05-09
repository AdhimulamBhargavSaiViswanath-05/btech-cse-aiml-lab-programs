import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

# -------------------------------------------------------------------
# Configuration Class
# -------------------------------------------------------------------
class Config:
    """Configuration for analysis parameters"""
    def __init__(self):
        self.file_path = "comprehensive_social_media_india_1000.csv"
        self.target_location = None
        self.start_time = None
        self.end_time = None
        self.top_n = 10
        self.min_hashtag_count = 1
        self.entity_patterns = {
            'ORGANIZATION': [r'@\w+', r'\b([A-Z][a-z]*(?:[A-Z][a-z]*)+)\b', r'\b([A-Z]{2,}(?:[a-z]+)?)\b'],
            'PERSON': [r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\b'],
            'LOCATION': [r'\b([A-Z][a-z]{3,}(?:\s+[A-Z][a-z]+)?)\b'],
            'HASHTAG': [r'#(\w+)']
        }
        self.stopwords = {
            'The', 'This', 'That', 'Massive', 'Terrible', 'Good', 'Great', 'Amazing', 'Best', 
            'Worst', 'Just', 'Very', 'Really', 'Finally', 'Please', 'Help', 'Need', 'Want', 
            'Like', 'Love', 'Hate', 'April', 'January', 'February', 'March', 'April Fools', 
            'AprilFools', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
        }
        self.analyze_platform = True
        self.target_platform = None

# -------------------------------------------------------------------
# Core Analysis Function
# -------------------------------------------------------------------
def analyze_tweets(config):
    """Analyze tweets to identify trends and named entities"""
    try:
        df = pd.read_csv(config.file_path)
        if not all(col in df.columns for col in ['text', 'created_at']):
            return None
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce', utc=True)
    df.dropna(subset=['created_at'], inplace=True)
    
    filtered_df = df.copy()
    
    if config.target_platform and 'platform' in df.columns:
        filtered_df = filtered_df[filtered_df['platform'].astype(str).str.contains(
            config.target_platform, case=False, na=False)]
    
    platform_counts = filtered_df['platform'].value_counts() if 'platform' in filtered_df.columns else pd.Series([], dtype='int64')
    
    if config.target_location and 'location' in df.columns:
        filtered_df = filtered_df[filtered_df['location'].astype(str).str.contains(
            config.target_location, case=False, na=False)]
    if config.start_time:
        filtered_df = filtered_df[filtered_df['created_at'] >= pd.to_datetime(config.start_time, utc=True)]
    if config.end_time:
        filtered_df = filtered_df[filtered_df['created_at'] <= pd.to_datetime(config.end_time, utc=True)]

    if filtered_df.empty:
        return None

    def clean_and_extract(text):
        text = str(text)
        mentions = re.findall(r'@\w+', text)
        hashtags = re.findall(r'#\w+', text)
        cleaned = re.sub(r"http\S+|www\.\S+|@\w+", "", text)
        cleaned = re.sub(r"#(\w+)", r"\1", cleaned)
        cleaned = re.sub(r"[^\w\s-]", " ", cleaned)
        return re.sub(r'\s+', ' ', cleaned).strip(), mentions, hashtags

    results = filtered_df['text'].apply(clean_and_extract)
    filtered_df['cleaned_text'] = results.apply(lambda x: x[0])
    filtered_df['mentions'] = results.apply(lambda x: x[1])
    filtered_df['hashtags'] = results.apply(lambda x: x[2])

    all_hashtags = [h.lower() for hashtag_list in filtered_df['hashtags'] for h in hashtag_list]
    hashtag_counts = Counter({k: v for k, v in Counter(all_hashtags).items() if v >= config.min_hashtag_count})
    all_mentions = [m.lower() for mention_list in filtered_df['mentions'] for m in mention_list]
    mention_counts = Counter(all_mentions)
    sentiment_counts = filtered_df['sentiment'].value_counts() if 'sentiment' in filtered_df.columns else pd.Series([], dtype='int64')

    def extract_entities(text, patterns_dict, stopwords):
        entities = {}
        for entity_type, patterns in patterns_dict.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text):
                    entity = (match.group(1) if match.lastindex else match.group(0)).strip()
                    if entity and len(entity) > 1 and entity not in stopwords and (entity not in entities or entity_type == 'PERSON'):
                        entities[entity] = entity_type
        return entities

    all_entities = [(entity, etype) for _, row in filtered_df.iterrows() 
                    for entity, etype in extract_entities(row['text'], config.entity_patterns, config.stopwords).items()]
    entity_counts = Counter(all_entities)
    
    filtered_df['date'] = filtered_df['created_at'].dt.date
    daily_counts = filtered_df.groupby('date').size()
    location_counts = filtered_df['location'].value_counts() if 'location' in filtered_df.columns else pd.Series([], dtype='int64')

    return {
        'filtered_df': filtered_df,
        'hashtag_counts': hashtag_counts,
        'mention_counts': mention_counts,
        'sentiment_counts': sentiment_counts,
        'entity_counts': entity_counts,
        'daily_counts': daily_counts,
        'location_counts': location_counts,
        'platform_counts': platform_counts,
        'config': config
    }

# -------------------------------------------------------------------
# Report Generation
# -------------------------------------------------------------------
def print_report(data):
    """Display basic analysis report"""
    if not data:
        return

    df = data['filtered_df']
    
    print("\n" + "=" * 60)
    print("SOCIAL MEDIA ANALYSIS REPORT".center(60))
    print("=" * 60)
    print(f"\nSTATISTICS:")
    print(f"   Total Posts: {len(df)}")
    print(f"   Period: {df['created_at'].min().date()} to {df['created_at'].max().date()}")
    if not data['location_counts'].empty:
        print(f"   Top Location: {data['location_counts'].index[0]} ({data['location_counts'].iloc[0]} posts)")
    
    if data['hashtag_counts']:
        print(f"\nTOP 5 TRENDING HASHTAGS:")
        for i, (hashtag, count) in enumerate(data['hashtag_counts'].most_common(5), 1):
            print(f"   {i}. #{hashtag} - {count} times")
    
    if not data['sentiment_counts'].empty:
        print(f"\nSENTIMENT:")
        total = data['sentiment_counts'].sum()
        for sentiment, count in data['sentiment_counts'].items():
            pct = (count / total) * 100
            print(f"   {sentiment}: {count} ({pct:.1f}%)")
    
    if not data['location_counts'].empty:
        print(f"\nTOP 3 LOCATIONS:")
        for i, (location, count) in enumerate(data['location_counts'].head(3).items(), 1):
            print(f"   {i}. {location} - {count} posts")
    
    print("\n" + "=" * 60)

# -------------------------------------------------------------------
# Visualization
# -------------------------------------------------------------------
def visualize_results(data):
    """Generate single visualization - Sentiment Distribution"""
    if not data:
        return

    if data['sentiment_counts'].empty:
        print("\nNo sentiment data available for visualization")
        return

    sns.set_style("whitegrid")
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    colors = {'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'}
    sentiment_colors = [colors.get(s, '#3498db') for s in data['sentiment_counts'].index]
    
    wedges, texts, autotexts = ax.pie(
        data['sentiment_counts'], 
        labels=data['sentiment_counts'].index,
        autopct='%1.1f%%', 
        startangle=90, 
        colors=sentiment_colors,
        explode=[0.05] * len(data['sentiment_counts']),
        textprops={'fontsize': 12, 'weight': 'bold'}
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
    
    ax.set_title('Sentiment Distribution Analysis', fontweight='bold', fontsize=16, pad=20)
    
    plt.tight_layout()
    plt.savefig('sentiment_analysis.png', dpi=200, bbox_inches='tight', facecolor='white')
    print(f"\nVisualization saved: 'sentiment_analysis.png'")
    plt.show()

def main():
    """Main execution: Analyze social media data"""
    print("\n" + "=" * 60)
    print("SOCIAL MEDIA ANALYSIS TOOL".center(60))
    print("=" * 60)
    
    config = Config()
    
    print(f"\nLoading data from: {config.file_path}")
    print("Analyzing all locations and time periods...")
    
    results = analyze_tweets(config)
    
    if results:
        print_report(results)
        visualize_results(results)
        print("\nAnalysis complete!\n")
    else:
        print("\nAnalysis failed. Check your data file.\n")

if __name__ == "__main__":
    main()
