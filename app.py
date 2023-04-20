from flask import Flask, render_template,request
import pickle
import numpy as np 


popular_df = pickle.load(open('static/popular.pkl', 'rb'))
pt = pickle.load(open('static/pt.pkl', 'rb'))
books = pickle.load(open('static/books.pkl', 'rb'))
similarity_scores = pickle.load(open('static/similarity_scores.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           Votes=list(popular_df['num_ratings'].values),
                            ratings=list(popular_df['avg_ratings'].values),
                           Author=list(popular_df['Book-Author'].values),
                           Images=list(popular_df['Image-URL-L'].values),
                           )

@app.route('/recomender')
def recomend_ui():
    return render_template('recomend.html'
                           )

@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recomend.html', data=data)
