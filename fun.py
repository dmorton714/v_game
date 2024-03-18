import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np
from sqlite3 import connect


df = pd.read_csv('vgchartz-2024.csv')

def cleaning(df):
    df = df.copy()
    df['release_date'] = pd.to_datetime(df['release_date'])
    df.drop(['img', 'last_update'], axis=1, inplace=True)
    df = df.dropna(subset=['release_date'])
    columns_to_fill_zero = ['critic_score', 'total_sales', 'na_sales', 'jp_sales', 'pal_sales', 'other_sales']
    df.loc[:, columns_to_fill_zero] = df.loc[:, columns_to_fill_zero].fillna(0)
    
    return df

df = cleaning(df)

def check_missing_items(all_items, df_column):
    all_items_lower = [item.lower().strip() for item in all_items]
    unique_values_lower = set(df_column.str.lower().str.strip().unique())
    return set(all_items_lower) - unique_values_lower

def assign_console_mfg(df):
    categories = {
        'nintendo': ['3DS', 'ds', 'Wii', 'WiiU', 'NS', 'GB', 'NES', 'SNES', 'GBC', 'N64'],
        'pc': ['Linux', 'OSX', 'PC', 'Arc', 'All'],
        'xbox': ['X360', 'XOne', 'Series'],
        'sony': ['PS', 'PS2', 'PS3', 'PS4', 'PS5', 'PSP', 'PSV', 'PSN'],
        'mobile': ['iOS', 'And'],
        'sega': ['GG', 'MSD', 'MS', 'GEN', 'SCD'],
        'atari': ['2600', '7800'],
        'commodore': ['amig', 'C64'],
        'other': ['Ouya', 'OR', 'ACPC', 'AST', 'ApII', 'PCE', 'ZXS', 'Lynx', 'NG', 'ZXS']
    }

    all_items = [item for sublist in categories.values() for item in sublist]

    missing_items = check_missing_items(all_items, df['console'])

    if missing_items:
        print(f"Missing items: {missing_items}")
    else:
        print("All items are covered.")

    conditions = [df['console'].isin(items) for items in categories.values()]
    values = list(categories.keys())

    df['console_mfg'] = np.select(conditions, values, default='unknown')


assign_console_mfg(df)


def filter_and_group_by_year(df, target_year):
    df['release_date'] = pd.to_datetime(df['release_date'])
    df_filtered = df[df['release_date'].dt.year == target_year]
    result = df_filtered.groupby(['release_date', 'console'])['total_sales'].sum().reset_index()
    result['release_date'] = result['release_date'].dt.year  
    result = result.groupby(['release_date', 'console'])['total_sales'].sum().reset_index()
    return result

for year in range(1971, 2024):
    df_name = f"sales_{year}"
    globals()[df_name] = filter_and_group_by_year(df, year)


def single_graph(date_range, console):
    
    df['release_date'] = pd.to_datetime(df['release_date'])
    
    
    filtered_df = df[(df['release_date'].dt.year >= date_range[0]) & 
                     (df['release_date'].dt.year <= date_range[1]) & 
                     (df['console'] == console)]

    
    sales_by_year = filtered_df.groupby(filtered_df['release_date'].dt.year)['total_sales'].sum().reset_index()

    
    plt.figure(figsize=(10, 6))
    
    
    plt.bar(sales_by_year['release_date'], sales_by_year['total_sales'], label='Total Sales')
    
    # Trend curve
    x = sales_by_year['release_date']
    y = sales_by_year['total_sales']
    
    z = np.polyfit(x, y, 2)
    p = np.poly1d(z)

    # Clip values below 0
    trend_line = np.maximum(p(x), 0)  
    
    plt.plot(x, trend_line, 'r--', label='Trend Curve')
    
    plt.xlabel('Year')
    plt.ylabel('Total Sales')
    plt.title(f'Total Sales of {console} from {date_range[0]} to {date_range[1]}')
    
    plt.legend()
    
    plt.show()


def stacked_graph(date_range, *consoles):
    
    df['release_date'] = pd.to_datetime(df['release_date'])
    
    
    filtered_df = df[(df['release_date'].dt.year >= date_range[0]) & 
                     (df['release_date'].dt.year <= date_range[1]) & 
                     (df['console'].isin(consoles))]

    
    sales_by_year = filtered_df.groupby(['release_date', 'console'])['total_sales'].sum().reset_index()

    
    plt.figure(figsize=(12, 8))
    
    for console in consoles:
        console_data = sales_by_year[sales_by_year['console'] == console]
        x = console_data['release_date'].dt.year  
        y = console_data['total_sales']
        
        # Trend curve
        z = np.polyfit(x, y, 2)
        p = np.poly1d(z)
         # Clip values below 0
        trend_line = np.maximum(p(x), 0) 
        
        # Bar plot
        plt.bar(x, y, label=f'Total Sales - {console}')
        
        # Trend curve plot
        plt.plot(x, trend_line, '--', label=f'Trend Curve - {console}')

    plt.xlabel('Year')
    plt.ylabel('Total Sales')
    plt.title(f'Total Sales Comparison of Consoles from {date_range[0]} to {date_range[1]}')
    
    # Display legend
    plt.legend()
    
    plt.show()



def graph(date_range, *consoles):
   
    df['release_date'] = pd.to_datetime(df['release_date'])
    

    filtered_df = df[(df['release_date'].dt.year >= date_range[0]) & 
                     (df['release_date'].dt.year <= date_range[1]) & 
                     (df['console'].isin(consoles))]

    
    sales_by_year = filtered_df.groupby(['release_date', 'console'])['total_sales'].sum().reset_index()

    
    plt.figure(figsize=(12, 8))
    
    for i, console in enumerate(consoles):
        console_data = sales_by_year[sales_by_year['console'] == console]
        x = console_data['release_date'].dt.year  
        y = console_data['total_sales']
        
        # Trend curve
        z = np.polyfit(x, y, 2)
        p = np.poly1d(z)
        # Clip values below 0
        trend_line = np.maximum(p(x), 0)  
        
        cmap = plt.get_cmap('tab10')
        bar_color = cmap(i)
        darker_bar_color = tuple(c * 0.6 for c in bar_color)
        
        
        plt.bar(x + i * 0.3, y, width=0.3, color=bar_color, label=f'Total Sales - {console}')

        
        plt.plot(x, trend_line, '-', color=darker_bar_color, linewidth=2, label=f'Trend Curve - {console}', zorder=10)

    plt.xlabel('Year')
    plt.ylabel('Total Sales')
    plt.title(f'Total Sales Comparison of Consoles from {date_range[0]} to {date_range[1]}')
    
    
    plt.legend()
    
    plt.show()


def graph(date_range, *consoles):
   
    df['release_date'] = pd.to_datetime(df['release_date'])
    

    filtered_df = df[(df['release_date'].dt.year >= date_range[0]) & 
                     (df['release_date'].dt.year <= date_range[1]) & 
                     (df['console'].isin(consoles))]

    
    sales_by_year = filtered_df.groupby(['release_date', 'console'])['total_sales'].sum().reset_index()

    
    plt.figure(figsize=(12, 8))
    
    for i, console in enumerate(consoles):
        console_data = sales_by_year[sales_by_year['console'] == console]
        x = console_data['release_date'].dt.year  
        y = console_data['total_sales']
        
        # Trend curve
        z = np.polyfit(x, y, 2)
        p = np.poly1d(z)
        # Clip values below 0
        trend_line = np.maximum(p(x), 0)  
        
        cmap = plt.get_cmap('tab10')
        bar_color = cmap(i)
        darker_bar_color = tuple(c * 0.6 for c in bar_color)
        
        
        plt.bar(x + i * 0.3, y, width=0.3, color=bar_color, label=f'Total Sales - {console}')

        
        plt.plot(x, trend_line, '-', color=darker_bar_color, linewidth=2, label=f'Trend Curve - {console}', zorder=10)

    plt.xlabel('Year')
    plt.ylabel('Total Sales')
    plt.title(f'Total Sales Comparison of Consoles from {date_range[0]} to {date_range[1]}')
    
    
    plt.legend()
    
    plt.show()


conn = connect(':memory:')

df.to_sql("df", conn)

def sql(a_string):
    return(pd.read_sql(a_string, conn))


def graph_genre(date_range, *genres):
   
    df['release_date'] = pd.to_datetime(df['release_date'])
    
    filtered_df = df[(df['release_date'].dt.year >= date_range[0]) & 
                     (df['release_date'].dt.year <= date_range[1]) & 
                     (df['genre'].isin(genres))]
    
    sales_by_year = filtered_df.groupby(['release_date', 'genre'])['total_sales'].sum().reset_index()

    plt.figure(figsize=(12, 8))
    
    for i, genre in enumerate(genres):
        genre_data = sales_by_year[sales_by_year['genre'] == genre]
        x = genre_data['release_date'].dt.year  
        y = genre_data['total_sales']
        
        # Trend curve
        z = np.polyfit(x, y, 2)
        p = np.poly1d(z)
        # Clip values below 0
        trend_line = np.maximum(p(x), 0)  
        
        cmap = plt.get_cmap('tab10')
        bar_color = cmap(i)
        darker_bar_color = tuple(c * 0.6 for c in bar_color)
        
        plt.bar(x + i * 0.3, y, width=0.3, color=bar_color, label=f'Total Sales - {genre}')
        
        plt.plot(x, trend_line, '-', color=darker_bar_color, linewidth=2, label=f'Trend Curve - {genre}', zorder=10)

    plt.xlabel('Year')
    plt.ylabel('Total Sales')
    plt.title(f'Total Sales Comparison of Genres from {date_range[0]} to {date_range[1]}')
    
    plt.legend()
    
    plt.show()


def graph_genre_quarterly(date_range, *genres):
   
    df['release_date'] = pd.to_datetime(df['release_date'])
    
    filtered_df = df[(df['release_date'].dt.year >= date_range[0]) & 
                     (df['release_date'].dt.year <= date_range[1]) & 
                     (df['genre'].isin(genres))].copy()
    
    filtered_df['quarter'] = filtered_df['release_date'].dt.to_period("Q")
    
    sales_by_quarter = filtered_df.groupby(['quarter', 'genre'])['total_sales'].sum().reset_index()

    plt.figure(figsize=(15, 8))
    
    quarters = sales_by_quarter['quarter'].unique().astype(str)
    width = 0.2  # Adjusted width to make bars side-by-side
    
    for i, genre in enumerate(genres):
        genre_data = sales_by_quarter[sales_by_quarter['genre'] == genre]
        x = np.arange(len(quarters)) + i * width  # Adjusted x positions for side-by-side bars
        y = genre_data.groupby('quarter')['total_sales'].sum().reindex(quarters).fillna(0)
        
        cmap = plt.get_cmap('tab10')
        bar_color = cmap(i)
        
        plt.bar(x, y, width=width, color=bar_color, label=genre)
    
    plt.xlabel('Quarter')
    plt.ylabel('Total Sales')
    plt.title(f'Total Sales Comparison of Genres from {date_range[0]} to {date_range[1]} (Quarterly)')
    
    plt.legend(loc='upper left')
    plt.xticks(ticks=np.arange(len(quarters)) + width * (len(genres) - 1) / 2, labels=quarters, rotation=90)
    
    plt.show()


def top_genre(genre):
    genre_df = df[df['genre'] == genre]
    
    if genre_df.empty:
        print(f"No data found for the genre: {genre}")
        return None
    
    top_titles = genre_df.nlargest(20, 'total_sales')[['title', 'total_sales']]
    
    return top_titles


def genre(df, target_year):
    df['release_date'] = pd.to_datetime(df['release_date'])
    df_filtered = df[df['release_date'].dt.year == target_year]
    result = df_filtered.groupby(['release_date', 'genre'])['total_sales'].sum().reset_index()
    result['release_date'] = result['release_date'].dt.year  
    result = result.groupby(['release_date', 'genre'])['total_sales'].sum().reset_index()
    return result

for year in range(1971, 2024):
    df_name = f"genre_{year}"
    globals()[df_name] = genre(df, year)