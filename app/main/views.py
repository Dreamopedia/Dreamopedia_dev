import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from . import main
from forms import SearchForm, AddForm
from app import db
from app.models import Dream
from flask import Flask, request, make_response, redirect, abort, render_template, url_for, flash

@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        results = Dream.query.whoosh_search(form.search.data).all()
        if len(results)>1:
            return redirect(url_for('main.results',dream=form.search.data))
        elif len(results)==1:
            id=results[0].id
            return redirect(url_for('main.dream',id=id))
        else:
            return render_template('notfound.html', form=form)
    return render_template('index.html', form=form)
    
@main.route('/dream/<int:id>', methods=['GET','POST'])
def dream(id):
    form=SearchForm()
    dream = Dream.query.filter_by(id=id).first()
    return render_template('dream.html',dream=dream,form=form)
    
@main.route('/search', methods=['GET','POST'])
def search():
    form=SearchForm()
    name=request.form['search']
    results = Dream.query.whoosh_search(name).all()
    if len(results)>1:
            return render_template('results.html', results=results,form=form)
    elif len(results)==1:
        id=results[0].id
        return redirect(url_for('main.dream',id=id))
    else:
        flash('No dreams found, sorry :(')
        return redirect(url_for('main.index'))

@main.route('/results/<dream>', methods=['GET', 'POST'])
def results(dream):
    form = SearchForm()
    results = Dream.query.whoosh_search(dream).all()
    return render_template('results.html', results=results, form=form)
    

@main.route('/add', methods=['GET','POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        dream = Dream(name = form.name.data, description = form.description.data)
        db.session.add(dream)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add.html', form=form)



