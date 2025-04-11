import streamlit as st
import json
import os

# File path
LIBRARY_FILE = "library.json"

# Load library
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save library
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

library = load_library()

# Custom CSS
custom_css = """
<style>
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

body {
    background: linear-gradient(-45deg, #4e54c8, #8f94fb, #a18cd1, #fbc2eb);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    font-family: 'Segoe UI', sans-serif;
    color: #fff;
}

h1 {
    color: #ffffff;
    text-align: center;
    font-size: 3rem;
    text-shadow: 1px 1px 5px rgba(0,0,0,0.2);
}

.css-1d391kg {
    background-color: rgba(0,0,0,0.85) !important;
}

button {
    background: #222;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: 0.3s ease;
}
button:hover {
    background: #fff;
    color: #222;
    border: 1px solid #222;
    transform: scale(1.05);
}

input, select {
    width: 100%;
    padding: 10px;
    margin: 6px 0;
    border-radius: 6px;
    border: 1px solid #ccc;
}
input:focus, select:focus {
    outline: none;
    border-color: #a18cd1;
    box-shadow: 0 0 8px #a18cd180;
}

.book-card {
    background: rgba(255, 255, 255, 0.08);
    padding: 15px;
    margin: 12px 0;
    border-radius: 10px;
    box-shadow: 2px 2px 12px rgba(0,0,0,0.25);
    transition: 0.3s;
}
.book-card:hover {
    transform: scale(1.02);
    box-shadow: 4px 4px 20px rgba(0,0,0,0.3);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# App Title
st.title("Personal Library Manager")

# Sidebar Menu
menu = ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics", "Exit"]
choice = st.sidebar.radio("Select an option", menu)

# Add a Book
if choice == "Add a Book":
    st.subheader("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author Name")
    year = st.number_input("Publication Year", min_value=1000, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read_status = st.radio("Read this book?", ["Yes", "No"]) == "Yes"

    if st.button("Add Book"):
        new_book = {"title": title, "author": author, "year": year, "genre": genre, "read": read_status}
        library.append(new_book)
        save_library(library)
        st.success(f"Book '{title}' added to your library!")

# Remove a Book
elif choice == "Remove a Book":
    st.subheader("Remove a Book")
    book_titles = [book["title"] for book in library]
    if book_titles:
        selected_book = st.selectbox("Select a book to remove", book_titles)
        if st.button("Remove Book"):
            library = [book for book in library if book["title"] != selected_book]
            save_library(library)
            st.warning(f"Book '{selected_book}' removed!")
    else:
        st.info("Library is empty.")

# Search a Book
elif choice == "Search for a Book":
    st.subheader("Search a Book")
    search_type = st.radio("Search by:", ["Title", "Author"])
    search_query = st.text_input("Enter your search...")

    if st.button("Search"):
        results = [book for book in library if search_query.lower() in book[search_type.lower()].lower()]
        if results:
            for book in results:
                st.markdown(f"""
                <div class="book-card">
                    <strong>{book['title']}</strong> by {book['author']} ({book['year']})  
                    <br>Genre: {book['genre']}  
                    <br>{'Read' if book['read'] else 'Unread'}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("No matches found.")

# Display All Books
elif choice == "Display All Books":
    st.subheader("Your Library Collection")
    if library:
        for book in library:
            st.markdown(f"""
            <div class="book-card">
                <strong>{book['title']}</strong> by {book['author']} ({book['year']})  
                <br>Genre: {book['genre']}  
                <br>{'Read' if book['read'] else 'Unread'}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Your library is empty!")

# Display Stats
elif choice == "Display Statistics":
    st.subheader("Library Statistics")
    total_books = len(library)
    read_books = sum(book["read"] for book in library)
    unread_books = total_books - read_books
    percentage = (read_books / total_books * 100) if total_books > 0 else 0

    st.write(f"Total Books: {total_books}")
    st.write(f"Books Read: {read_books}")
    st.write(f"Unread Books: {unread_books}")
    st.write(f"Completion Rate: {percentage:.2f}%")

# Exit
elif choice == "Exit":
    st.balloons()
    st.success("Library saved! Come back soon!")
