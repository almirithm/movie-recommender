from flask import Flask,request,render_template
from clean_movies import recommend


from clean_movies import recommend
from fetch_data import movie

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])

def home():
    if request.method=='POST':
        movie=request.form['movie']
        recommendations = recommend(movie)
        return render_template('index.html',movie=movie,recommendations=recommendations)
    return render_template('index.html',movie=None,recommendations=None)

if __name__=='__main__':
    app.run(debug=True)