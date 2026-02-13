import streamlit as st
import sqlite3

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('maigret.db', check_same_thread=False)
    return conn

st.set_page_config(page_title="Maigret Tracker", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ Maigret Library")

# --- Search Logic ---
search_query = st.text_input("Search by title, original French, or year...", "").lower()

# --- Database Operations ---
conn = get_db_connection()
cursor = conn.cursor()

# Query the database
if search_query:
    cursor.execute("""
        SELECT rowid, title, alt_titles, original_title, pub_year, read_status 
        FROM books 
        WHERE title LIKE ? OR alt_titles LIKE ? OR original_title LIKE ? OR pub_year LIKE ?
    """, (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
else:
    cursor.execute("SELECT rowid, title, alt_titles, original_title, pub_year, read_status FROM books ORDER BY pub_year ASC")

books = cursor.fetchall()

# --- UI Display ---
st.write(f"Showing {len(books)} books")

for book in books:
    db_id, title, alts, original, year, read = book
    
    # Create a nice container for each book
    with st.container():
        col1, col2 = st.columns([0.8, 0.2])
        
        with col1:
            st.subheader(f"{title} ({year})")
            st.write(f"**French:** {original}")
            if alts:
                st.caption(f"**Also known as:** {alts}")
        
        with col2:
            # Checkbox to toggle read status
            new_read_val = st.checkbox("Read", value=bool(read), key=f"check_{db_id}")
            
            # If the user clicks the checkbox, update the DB immediately
            if new_read_val != bool(read):
                cursor.execute("UPDATE books SET read_status = ? WHERE rowid = ?", (int(new_read_val), db_id))
                conn.commit()
                st.rerun()
        
        st.divider()

conn.close()
