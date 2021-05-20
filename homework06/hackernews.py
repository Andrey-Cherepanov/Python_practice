from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier

@route("/")
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s=session()
    row=s.query(News).filter(News.id == request.query.id).first()
    row.label=request.query.label
    s.commit()
    redirect("/news")

@route("/update")
def update_news():
    news = get_news('https://news.ycombinator.com/newest')
    s = session()
    for new in news:
        if not len(
        s.query(News).filter(News.author == new['author'], News.title == new['title']).all()
        ):
            s.add(News(
            author=new['author'],
            title=new['title'],
            points=new['points'],
            comments=new['comments'],
            url=new['url']
            ))
        s.commit()
    redirect("/news")

@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    ...

if __name__ == "__main__":
    run(host="localhost", port=8080)
