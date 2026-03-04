import streamlit as st
import sqlite3

# 1. This function stays in memory so searching is instant
@st.cache_data
def get_all_books():
    conn = sqlite3.connect('maigret.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, title, alt_titles, original_title, pub_year, read_status, notes FROM books ORDER BY pub_year ASC")
    data = cursor.fetchall()
    conn.close()
    return data

st.set_page_config(page_title="Maigret Tracker", page_icon="🕵️‍♂️")

# --- Logic to handle updates ---
def update_db(query, params):
    conn = sqlite3.connect('maigret.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    st.cache_data.clear() # This forces the app to "re-read" the DB after a change

st.title("🕵️‍♂️ Maigret Archive")

# Fetch Data
books_data = get_all_books()

# --- New Metric Header ---
read_count = sum(1 for b in books_data if b[5] == 1)
total_books = 75

col1, col2 = st.columns(2)
col1.metric("📚 Total Maigret Books", total_books)
col2.metric("📖 Total Read", read_count)

st.divider()

# --- Filters ---
search_query = st.text_input("🔍 Search...", "").lower()
show_unread_only = st.toggle("🛒 Shop Mode (Hide Read)")

# --- Filter Logic (Done in Python now, which is faster than SQL for 80 rows) ---
for book in books_data:
    db_id, title, alts, original, year, read, notes = book
    
    # Filter by Search
    if search_query and not any(search_query in str(field).lower() for field in [title, alts, original, str(year)]):
        continue
        
    # Filter by Toggle
    if show_unread_only and read:
        continue
        
    with st.expander(f"{'✅' if read else '📚'} {title} ({year})", expanded=not read):
        st.write(f"**Original:** {original}")
        
        # Notes Section
        new_note = st.text_input("Notes", value=notes if notes else "", max_chars=100, key=f"note_{db_id}")
        if new_note != notes:
            update_db("UPDATE books SET notes = ? WHERE rowid = ?", (new_note, db_id))
            st.toast(f"Note saved for {title}!")
            st.rerun()

        # Toggle Button
        btn_label = "Mark as Read" if not read else "Mark as Unread"
        if st.button(btn_label, key=f"btn_{db_id}", use_container_width=True):
            new_status = 0 if read else 1
            update_db("UPDATE books SET read_status = ? WHERE rowid = ?", (new_status, db_id))
            st.rerun()
