from flask import Flask, render_template, request, make_response
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.common.exceptions import WebDriverException
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
# from lib2to3.fixes.fix_imports import MAPPING

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/output/')
def output():
    return render_template('output.html')

@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/submit', methods=["POST"])
def submit():
    output = []
    if request.method == "POST":
        the_url = request.form['hotelUrl']
        driver = webdriver.Chrome('/Users/Adam/Downloads/chromedriver')
        driver.get(str(the_url))
        time.sleep(5)

        # xPath to all More elemets.
        more = driver.find_elements_by_xpath("//*[text() = 'More']")

        for x in range(0, len(more)):
            # expands the reviews if they are expandable.
            # if the_more_buttons[x].is_displayed():
            try:
                more[x].click()
            except WebDriverException:
                print("Element is not clickable")

        r = driver.page_source
        soup = BeautifulSoup(r, "lxml")
        letters = soup.find_all("p", class_="partial_entry")

        for letter in letters:
            output.append(letter.get_text())
            print(letter.get_text())

        #TODO: Take the list of reviews -- letters -- and run them through training code.
        #TODO: Return a list of text as the results for the user.

        filename = '/Users/Adam/PycharmProjects/ReviewMania/RandomForest_model.sav'

        loaded_model = pickle.load(open(filename, 'rb'))

        saved_vectorizer = '/Users/Adam/PycharmProjects/ReviewMania/vectorizer.pk'
        saved_lsa = '/Users/Adam/PycharmProjects/ReviewMania/lsa.pk'

        # load the model from disk
        loaded_model = pickle.load(open(filename, 'rb'))
        loaded_lsa = pickle.load(open(saved_lsa, 'rb'))
        loaded_vectorizer = pickle.load(open(saved_vectorizer, 'rb'))
        test1_transformed = loaded_vectorizer.transform(output)
        test1_lsa = loaded_lsa.transform(test1_transformed)
        result = loaded_model.predict(test1_lsa)

        # result = loaded_model.predict(output)
        print(result)

        return render_template('output.html', reviews=output)

# Static file rendering.
# for testing static files
# @app.route('/<string:page_name>/')
# def static_page(page_name):
#     return render_template('%s.html' % page_name)

if __name__ == '__main__':
    app.run()
