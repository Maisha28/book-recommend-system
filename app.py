import streamlit as st
import pickle
import numpy as np

st.set_page_config(
    page_title="BookMind",
    page_icon="📚",
    layout="wide"
)

@st.cache_resource
def load_data():

    pt = pickle.load(open("model/pt.pkl", "rb"))

    similarity_scores = pickle.load(
        open("model/similarity_scores.pkl", "rb")
    )

    books = pickle.load(
        open("model/books.pkl", "rb")
    )

    return pt, similarity_scores, books


pt, similarity_scores, books = load_data()

book_metadata = books.drop_duplicates(
    "Book-Title"
)[
    ["Book-Title", "Book-Author", "Image-URL-M"]
]


def recommend(book_name):

    index = np.where(
        pt.index == book_name
    )[0][0]

    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:9]

    recommendations = []

    for item in similar_items:

        book = book_metadata[
            book_metadata["Book-Title"]
            == pt.index[item[0]]
        ]

        recommendations.append({
            "title": book["Book-Title"].values[0],
            "author": book["Book-Author"].values[0],
            "image": book["Image-URL-M"].values[0],
            "score": round(item[1] * 100, 1)
        })

    return recommendations


st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.stApp {
    background-color: #0b1120;
}

.block-container {
    max-width: 1450px;
    padding-top: 1rem;
}

h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

.hero {
    background: linear-gradient(
        135deg,
        #1e293b,
        #0f172a
    );

    border-radius: 28px;

    padding: 75px 50px;

    text-align: center;

    margin-bottom: 35px;

    border: 1px solid rgba(
        255,
        255,
        255,
        0.08
    );
}

.hero h1 {

    font-size: 76px;

    font-weight: 800;

    margin-bottom: 10px;

    color: white;

    text-shadow:
    0 0 35px rgba(
        255,
        255,
        255,
        0.12
    );
}

.hero p {

    color: #cbd5e1;

    font-size: 22px;
}

.book-card {

    background: #111827;

    border-radius: 18px;

    padding: 12px;

    text-align: center;
}

.book-title {

    color: white;

    font-size: 15px;

    font-weight: 700;

    margin-top: 10px;

    min-height: 65px;

    line-height: 1.35;
}

.book-author {

    color: #94a3b8;

    font-size: 13px;
}

.score-badge {

    background: #2563eb;

    color: white;

    display: inline-block;

    padding: 5px 12px;

    border-radius: 20px;

    font-size: 12px;

    font-weight: 600;

    margin-top: 8px;
}

div.stButton > button {

    width: 100%;

    height: 60px;

    border-radius: 14px;

    font-size: 18px;

    font-weight: 700;
}

.stSelectbox label {

    font-size: 18px;

    color: white !important;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero">

<h1>📚 BookMind</h1>

<p>
Discover books you'll love through intelligent recommendations
</p>

</div>
""", unsafe_allow_html=True)


selected_book = st.selectbox(
    "Search a Book",
    pt.index.values,
    index=None,
    placeholder="Start typing a book title..."
)


if selected_book:

    selected_data = book_metadata[
        book_metadata["Book-Title"]
        == selected_book
    ]

    if len(selected_data):

        cover = selected_data[
            "Image-URL-M"
        ].values[0]

        author = selected_data[
            "Book-Author"
        ].values[0]

        col1, col2 = st.columns(
            [1.2, 3]
        )

        with col1:

            st.image(
                cover,
                width=280
            )

        with col2:

            st.markdown(
                f"""
                <div style="
                color:white;
                font-size:44px;
                font-weight:800;
                line-height:1.2;
                margin-top:15px;
                max-width:900px;
                ">
                {selected_book}
                </div>

                <div style="
                color:#cbd5e1;
                font-size:26px;
                margin-top:20px;
                ">
                {author}
                </div>

                <div style="
                color:#e2e8f0;
                font-size:20px;
                line-height:1.8;
                margin-top:25px;
                max-width:750px;
                ">
                Discover books enjoyed by readers with similar tastes and reading patterns.
                </div>
                """,
                unsafe_allow_html=True
            )

st.write("")


if st.button("📖 Explore Recommendations"):

    if selected_book is None:

        st.warning(
            "Please select a book first."
        )

    else:

        with st.spinner(
            "Finding similar books..."
        ):

            recommendations = recommend(
                selected_book
            )

        st.markdown(
            f"""
            <h2 style="
            margin-top:25px;
            margin-bottom:30px;
            ">
            Recommended because you enjoyed
            <span style="
            color:#60a5fa;
            ">
            {selected_book}
            </span>
            </h2>
            """,
            unsafe_allow_html=True
        )

        row1 = st.columns(4)

        for i in range(4):

            book = recommendations[i]

            with row1[i]:

                st.image(
                    book["image"],
                    width=210
                )

                st.markdown(
                    f"""
                    <div class="book-title">
                    {book["title"]}
                    </div>

                    <div class="book-author">
                    {book["author"]}
                    </div>

                    <div class="score-badge">
                    {book["score"]}% Match
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.write("")

        row2 = st.columns(4)

        for i in range(4, 8):

            book = recommendations[i]

            with row2[i - 4]:

                st.image(
                    book["image"],
                    width=210
                )

                st.markdown(
                    f"""
                    <div class="book-title">
                    {book["title"]}
                    </div>

                    <div class="book-author">
                    {book["author"]}
                    </div>

                    <div class="score-badge">
                    {book["score"]}% Match
                    </div>
                    """,
                    unsafe_allow_html=True
                )