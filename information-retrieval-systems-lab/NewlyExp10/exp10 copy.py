"""
Experiment 10: PageRank on Scholarly Citation Network
Author: AdhimulamBhargavSaiViswanath-05
Date: 2025-11-04
"""

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)

def load_citation_dataset(filepath='citation_dataset.csv'):
    """Load citation dataset from CSV file"""
    df = pd.read_csv(filepath)
    df['citations'] = df['citations'].apply(lambda x: eval(x) if pd.notna(x) else [])
    return df

def build_citation_graph(df):
    """Build directed graph from citation data"""
    G = nx.DiGraph()
    for idx, row in df.iterrows():
        G.add_node(row['paper_id'], title=row['title'], authors=row['authors'], 
                   year=row['year'], venue=row['venue'])
    
    for idx, row in df.iterrows():
        for cited_paper in row['citations']:
            if cited_paper in G.nodes():
                G.add_edge(row['paper_id'], cited_paper)
    return G

def analyze_pagerank_results(df, G, pagerank_scores):
    """Analyze PageRank results and create report"""
    results = []
    for node in G.nodes():
        paper_data = df[df['paper_id'] == node].iloc[0]
        results.append({
            'paper_id': node, 'title': paper_data['title'], 'authors': paper_data['authors'],
            'year': paper_data['year'], 'venue': paper_data['venue'],
            'pagerank_score': pagerank_scores[node], 'in_degree': G.in_degree(node),
            'out_degree': G.out_degree(node), 'citations_received': G.in_degree(node)
        })
    
    results_df = pd.DataFrame(results).sort_values('pagerank_score', ascending=False).reset_index(drop=True)
    results_df['rank'] = range(1, len(results_df) + 1)
    return results_df
def visualize_citation_network(G, pagerank_scores, title="Citation Network"):
    """Visualize citation network with node sizes based on PageRank"""
    plt.figure(figsize=(18, 14))
    pos = nx.spring_layout(G, k=2.5, iterations=50, seed=42)
    
    node_sizes = [pagerank_scores[node] * 40000 for node in G.nodes()]
    in_degrees = [G.in_degree(node) for node in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=in_degrees, 
                          cmap='YlOrRd', alpha=0.8, edgecolors='black', linewidths=1.5)
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.3, arrows=True, 
                          arrowsize=10, arrowstyle='->', width=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    
    sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=min(in_degrees), vmax=max(in_degrees)))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=plt.gca(), shrink=0.8, pad=0.02)
    cbar.set_label('Citations Received (In-Degree)', fontsize=12)
    
    plt.title(f'{title}\n(Node size = PageRank score)', fontsize=16, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()

def print_report(results_df, G, top_n=10):
    """Print essential analysis report"""
    print("\n" + "="*100)
    print(" "*30 + "PAGERANK CITATION NETWORK ANALYSIS REPORT")
    print("="*100)
    
    print(f"\nNetwork Summary:")
    print(f"   Total Papers: {len(G.nodes())}")
    print(f"   Total Citations: {len(G.edges())}")
    print(f"   Average Citations per Paper: {len(G.edges()) / len(G.nodes()):.2f}")
    print(f"   Network Density: {nx.density(G):.4f}")
    
    print(f"\nPageRank Statistics:")
    print(f"   Mean PageRank: {results_df['pagerank_score'].mean():.6f}")
    print(f"   Std Dev: {results_df['pagerank_score'].std():.6f}")
    print(f"   Max PageRank: {results_df['pagerank_score'].max():.6f}")
    print(f"   Min PageRank: {results_df['pagerank_score'].min():.6f}")
    
    print(f"\nTop {top_n} Most Influential Papers (by PageRank):")
    print("-"*100)
    print(f"{'Rank':<6}{'Paper ID':<12}{'Title':<40}{'PR Score':<12}{'Citations':<12}{'Year':<8}")
    print("-"*100)
    for idx, row in results_df.head(top_n).iterrows():
        title_short = row['title'][:37] + '...' if len(row['title']) > 40 else row['title']
        print(f"{row['rank']:<6}{row['paper_id']:<12}{title_short:<40}"
              f"{row['pagerank_score']:<12.6f}{row['citations_received']:<12}{row['year']:<8}")
    print("\n" + "="*100)

def main():
    """Main execution function"""
    print("\n" + "="*100)
    print(" "*25 + "PAGERANK ON SCHOLARLY CITATION NETWORK")
    print(" "*30 + "Experiment 10 - Implementation")
    print("="*100)
    
    df = load_citation_dataset('citation_dataset.csv')
    G = build_citation_graph(df)
    pagerank_scores = nx.pagerank(G, alpha=0.85, max_iter=100)
    results_df = analyze_pagerank_results(df, G, pagerank_scores)
    
    print_report(results_df, G, top_n=10)
    
    visualize_citation_network(G, pagerank_scores, title="Scholarly Citation Network")
    plt.savefig('citation_network.png', dpi=300, bbox_inches='tight')
    print("\nVisualization saved as 'citation_network.png'")
    plt.show()
    
    print("\n" + "="*100)
    print(" "*35 + "EXPERIMENT COMPLETED SUCCESSFULLY")
    print("="*100)

if __name__ == "__main__":
    main()
