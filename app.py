import streamlit as st
import sqlite3

def get_db_connection():
    return sqlite3.connect('maigret.db', check_same_thread=False)

st.set_page_config(page_title="Maigret Tracker", page_icon="🕵️‍♂️")

conn = get_db_connection()
cursor = conn.cursor()

st.title("🕵️‍♂️ Maigret Archive")

# Stats
total_books = 75
read_count = cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 1").fetchone()[0]
progress = read_count / total_books

st.progress(progress)
st.write(f"📊 **Progress:** {read_count}/{total_books} ({int(progress*100)}%)")

# Filters
search_query = st.text_input("🔍 Search...", "").lower()
show_unread_only = st.toggle("📚 Shop Mode (Hide Read)")

# Data Fetching (Including the new 'notes' column)
if search_query:
    cursor.execute("""
        SELECT rowid, title, alt_titles, original_title, pub_year, read_status, notes 
        FROM books 
        WHERE title LIKE ? OR alt_titles LIKE ? OR original_title LIKE ? OR pub_year LIKE ?
    """, (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
else:
    cursor.execute("SELECT rowid, title, alt_titles, original_title, pub_year, read_status, notes FROM books ORDER BY pub_year ASC")

books = cursor.fetchall()

for book in books:
    db_id, title, alts, original, year, read, notes = book
    
    if show_unread_only and read:
        continue
        
    with st.expander(f"{'✅' if read else '📖'} {title} ({year})", expanded=not read):
        st.write(f"**Original:** {original}")
        
        # Notes Section
        new_note = st.text_input("Notes (max 100 chars)", value=notes if notes else "", max_chars=100, key=f"note_{db_id}")
        
        # Save note if it changed
        if new_note != notes:
            cursor.execute("UPDATE books SET notes = ? WHERE rowid = ?", (new_note, db_id))
            conn.commit()
            st.toast(f"Note saved for {title}!")

        # Toggle Button
        btn_label = "Mark as Read" if not read else "Mark as Unread"
        if st.button(btn_label, key=f"btn_{db_id}", use_container_width=True):
            new_status = 0 if read else 1
            cursor.execute("UPDATE books SET read_status = ? WHERE rowid = ?", (new_status, db_id))
            conn.commit()
            st.rerun()

conn.close()
