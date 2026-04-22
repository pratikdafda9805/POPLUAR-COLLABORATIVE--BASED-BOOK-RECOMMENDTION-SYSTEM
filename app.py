from flask import Flask,render_template,request
import pickle as pkl
# import numpy as np
import pandas as pd
import numpy as np
app = Flask(__name__)
books = pkl.load(open('top50books.pkl','rb'))
finalbooks = pd.read_csv('finalbooks.csv')
book_pivot = pd.read_csv('book_pivot.csv',index_col=0)
books_option = list(book_pivot.index)
model = pkl.load(open('model_book.pkl','rb'))
@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(books['Book-Title'].values),
                           book_author=list(books['Book-Author'].values),
                           book_img=list(books['Image-URL-M'].values),
                           book_rating=list(round(books['avg_rating'],2).values),
                           book_publisher=list(books['Publisher'].values),

                           )
@app.route('/recommend')
def recommend():
    return render_template('recommend.html',
                           books_option=books_option
                           )

@app.route('/recommend_books',methods=['POST'])
def recommend_books():
    def recommend_book(book_name):
        book_id = np.where(book_pivot.index == book_name)[0][0]
        distances, suggestions = model.kneighbors(
            book_pivot.iloc[book_id, :].values.reshape(1, -1),
            n_neighbors=6
        )
        recommended_books = []
        for i in suggestions[0]:
            recommended_books.append(book_pivot.index[i])
        return recommended_books[1:]

    books = request.form.getlist('books')
    book_name = request.form.get('book_name')
    list = recommend_book(book_name)

    poster_list=[]
    name_list=[]
    author_list=[]
    publser_list=[]
    for book in list:
        poster = finalbooks[finalbooks['name'] == book]['poster'].values[0]
        name = finalbooks[finalbooks['name'] == book]['name'].values[0]
        author = finalbooks[finalbooks['name'] == book]['author'].values[0]
        publisher = finalbooks[finalbooks['name'] == book]['Publisher'].values[0]
        poster_list.append(poster)
        name_list.append(name)
        author_list.append(author)
        publser_list.append(publisher)

    return render_template('recommend.html',
                           book_name = name_list,
                           book_img= poster_list,
                           book_author = author_list,
                           book_publisher = publser_list,
                           books_option = books_option
                           )

if __name__ == '__main__':
    app.run(debug=True)