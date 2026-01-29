from statsbombpy import sb
import pandas as pd
import os
import json

def extract_data():
    print("Starting data extraction for CAN 2023...")
    
    # Create data directory
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created 'data' directory.")

    # Competition and Season IDs for CAN 2023
    COMP_ID = 1267
    SEASON_ID = 107

    # 1. Matches
    print("Fetching matches...")
    matches = sb.matches(competition_id=COMP_ID, season_id=SEASON_ID)
    matches.to_csv('data/matches.csv', index=False)
    print(f"Saved {len(matches)} matches to 'data/matches.csv'.")

    # 2. Events
    print("Fetching events for all matches (this may take a few minutes)...")
    all_events = []
    match_ids = matches['match_id'].tolist()
    
    for i, m_id in enumerate(match_ids):
        try:
            events = sb.events(match_id=m_id)
            all_events.append(events)
            print(f"[{i+1}/{len(match_ids)}] Processed match {m_id}")
        except Exception as e:
            print(f"Error fetching match {m_id}: {e}")

    if all_events:
        events_df = pd.concat(all_events, ignore_index=True)
        
        # Pre-process locations to avoid complex parsing in Streamlit
        print("Processing locations...")
        # Extract location coordinates if lists
        def extract_coord(series, idx):
            if isinstance(series, list) and len(series) > idx:
                return series[idx]
            return None

        events_df['x'] = events_df['location'].apply(lambda x: extract_coord(x, 0))
        events_df['y'] = events_df['location'].apply(lambda x: extract_coord(x, 1))
        events_df['pass_end_x'] = events_df['pass_end_location'].apply(lambda x: extract_coord(x, 0))
        events_df['pass_end_y'] = events_df['pass_end_location'].apply(lambda x: extract_coord(x, 1))
        events_df['carry_end_x'] = events_df['carry_end_location'].apply(lambda x: extract_coord(x, 0))
        events_df['carry_end_y'] = events_df['carry_end_location'].apply(lambda x: extract_coord(x, 1))

        # Save to CSV
        # We use a compressed format if it's too large, but CSV is requested.
        # To avoid issues with large files, we might want to drop some very heavy columns if not needed.
        # But for now, let's keep it simple.
        events_df.to_csv('data/events.csv', index=False)
        print(f"Saved {len(events_df)} events to 'data/events.csv'.")
    
    print("Data extraction complete!")

if __name__ == "__main__":
    extract_data()
