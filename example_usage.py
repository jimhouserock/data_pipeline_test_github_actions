"""
Example usage of the pipeline data.
Demonstrates how to work with the generated embeddings and data.
"""

import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import pandas as pd
from typing import List, Dict, Tuple

class VideoSearchEngine:
    """Simple semantic search engine for video data."""
    
    def __init__(self, data_file='data/video_data.json'):
        """Initialize with video data."""
        self.data_file = data_file
        self.videos = []
        self.embeddings = []
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.load_data()
    
    def load_data(self):
        """Load video data and embeddings."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.videos = json.load(f)
            
            # Extract embeddings
            self.embeddings = []
            valid_videos = []
            
            for video in self.videos:
                if video.get('embeddings') and video['embeddings'].get('combined'):
                    self.embeddings.append(video['embeddings']['combined'])
                    valid_videos.append(video)
            
            self.videos = valid_videos
            self.embeddings = np.array(self.embeddings)
            
            print(f"Loaded {len(self.videos)} videos with embeddings")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            self.videos = []
            self.embeddings = np.array([])
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for videos similar to the query."""
        if len(self.videos) == 0:
            print("No video data available")
            return []
        
        # Generate query embedding
        query_embedding = self.model.encode([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for i, idx in enumerate(top_indices):
            video = self.videos[idx].copy()
            video['similarity_score'] = float(similarities[idx])
            video['rank'] = i + 1
            results.append(video)
        
        return results
    
    def print_search_results(self, results: List[Dict]):
        """Print search results in a formatted way."""
        if not results:
            print("No results found")
            return
        
        print(f"\nFound {len(results)} results:")
        print("-" * 80)
        
        for result in results:
            print(f"Rank {result['rank']}: {result['title']}")
            print(f"Similarity: {result['similarity_score']:.3f}")
            print(f"Views: {result.get('view_count', 'N/A')}")
            print(f"Published: {result.get('published_at', 'N/A')}")
            
            # Show transcript preview if available
            transcript = result.get('transcript')
            if transcript:
                preview = transcript[:200] + "..." if len(transcript) > 200 else transcript
                print(f"Transcript preview: {preview}")
            
            print("-" * 80)


def analyze_video_data():
    """Analyze the video data and show statistics."""
    try:
        with open('data/video_data.json', 'r', encoding='utf-8') as f:
            videos = json.load(f)
        
        if not videos:
            print("No video data found")
            return
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(videos)
        
        print("VIDEO DATA ANALYSIS")
        print("=" * 50)
        
        # Basic statistics
        print(f"Total videos: {len(df)}")
        print(f"Videos with transcripts: {df['transcript'].notna().sum()}")
        print(f"Videos with embeddings: {df['embeddings'].notna().sum()}")
        
        # View statistics
        if 'view_count' in df.columns:
            df['view_count'] = pd.to_numeric(df['view_count'], errors='coerce')
            print(f"Total views: {df['view_count'].sum():,}")
            print(f"Average views: {df['view_count'].mean():.0f}")
            print(f"Most viewed: {df['view_count'].max():,}")
        
        # Date analysis
        if 'published_at' in df.columns:
            df['published_at'] = pd.to_datetime(df['published_at'])
            print(f"Date range: {df['published_at'].min()} to {df['published_at'].max()}")
        
        # Top videos by views
        if 'view_count' in df.columns:
            print("\nTOP 5 VIDEOS BY VIEWS:")
            top_videos = df.nlargest(5, 'view_count')[['title', 'view_count']]
            for idx, row in top_videos.iterrows():
                print(f"  {row['title'][:60]}... - {row['view_count']:,} views")
        
        print("=" * 50)
        
    except Exception as e:
        print(f"Error analyzing data: {e}")


def demonstrate_search():
    """Demonstrate the search functionality."""
    print("SEMANTIC SEARCH DEMONSTRATION")
    print("=" * 50)
    
    # Initialize search engine
    search_engine = VideoSearchEngine()
    
    if len(search_engine.videos) == 0:
        print("No video data available for search")
        return
    
    # Example searches
    queries = [
        "machine learning",
        "data science",
        "python programming",
        "artificial intelligence",
        "data visualization"
    ]
    
    for query in queries:
        print(f"\nSearching for: '{query}'")
        results = search_engine.search(query, top_k=3)
        search_engine.print_search_results(results)


def export_for_analysis():
    """Export data in formats useful for further analysis."""
    try:
        with open('data/video_data.json', 'r', encoding='utf-8') as f:
            videos = json.load(f)
        
        if not videos:
            print("No video data to export")
            return
        
        # Create simplified dataset for analysis
        simplified_data = []
        for video in videos:
            simplified = {
                'video_id': video.get('video_id'),
                'title': video.get('title'),
                'view_count': video.get('view_count'),
                'like_count': video.get('like_count'),
                'comment_count': video.get('comment_count'),
                'published_at': video.get('published_at'),
                'has_transcript': bool(video.get('transcript')),
                'transcript_length': len(video.get('transcript', '')),
                'has_embeddings': bool(video.get('embeddings'))
            }
            simplified_data.append(simplified)
        
        # Save as CSV
        df = pd.DataFrame(simplified_data)
        df.to_csv('data/videos_analysis.csv', index=False)
        print("Exported analysis data to data/videos_analysis.csv")
        
        # Save embeddings separately for ML use
        embeddings_data = []
        for video in videos:
            if video.get('embeddings'):
                embeddings_data.append({
                    'video_id': video['video_id'],
                    'title': video['title'],
                    'title_embedding': video['embeddings'].get('title'),
                    'combined_embedding': video['embeddings'].get('combined')
                })
        
        if embeddings_data:
            with open('data/embeddings_export.json', 'w') as f:
                json.dump(embeddings_data, f, indent=2)
            print("Exported embeddings to data/embeddings_export.json")
        
    except Exception as e:
        print(f"Error exporting data: {e}")


def main():
    """Main function to demonstrate all features."""
    print("PIPELINE DATA USAGE EXAMPLES")
    print("=" * 60)
    
    # Check if data exists
    import os
    if not os.path.exists('data/video_data.json'):
        print("No video data found. Please run the pipeline first:")
        print("  python data_pipeline.py")
        return
    
    # Run demonstrations
    analyze_video_data()
    print("\n")
    demonstrate_search()
    print("\n")
    export_for_analysis()
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("1. Use the CSV file for data analysis in Excel/Google Sheets")
    print("2. Use embeddings for building ML models")
    print("3. Build a web interface for the search functionality")
    print("4. Connect to a database for production use")
    print("=" * 60)


if __name__ == "__main__":
    main()
