import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from . import main
from forms import SearchForm, AddForm
from app import db
from app.models import Dream
from flask import Flask, request, make_response, redirect, abort, render_template, url_for, flash, current_app

@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    # if form.validate_on_submit():
    #     results = Dream.query.whoosh_search(form.search.data).all()
    #     if len(results)>1:
    #         return redirect(url_for('main.results',dream=form.search.data))
    #     elif len(results)==1:
    #         id=results[0].id
    #         return redirect(url_for('main.dream',id=id))
    #     else:
    #         return render_template('notfound.html', form=form)
    return render_template('index.html', form=form)
    
@main.route('/dream/<int:id>', methods=['GET','POST'])
def dream(id):
    form=SearchForm()
    dream = Dream.query.filter_by(id=id).first()
    """Creating a link to other dream """
    if '[' in dream.description:
        _to = dream.description.index('[')
        _from = dream.description.index(']')
        link_dream  =  Dream.query.filter_by(name = dream.description[_from+6:-1]).first()
        if link_dream is not None:
            name = dream.name
            description = dream.description[:_to]
            return render_template('dream.html',dream=dream,form=form, link_dream=link_dream, 
                                    name = name, description = description
                                    )
        # else:
        #     pointed = dream.description[_from+6:-1]
        #     return redirect(url_for('main.results', dream=pointed))
        else:
            name = dream.name
            description = dream.description[:_to]
            return render_template('dream.html',dream=dream,form=form, link_dream=link_dream, 
                                    name = name, description = description
                                    )
    else:
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
        return render_template('notfound.html', form=form)

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


# @main.route('/add_all', methods = ['GET', 'POST'])
# def add_all():
    
#     import xml.etree.ElementTree as ET
#     from collections import OrderedDict as OrD
#     tree = ET.parse(current_app.config['XML_DREAMS'])
#     root = tree.getroot()
#     dreams = OrD() #ordered dictionary for getting last key added
#     to_database = {}
    
#     for page in root.findall('page'):

#     	if int(page.attrib['number']) > 33 and (int(page.attrib['number']))<394 : 
#     		for text in page:
#     			if int(text.attrib['font']) == 0: 				#font for description
#     				last_key=list(dreams.items())[-1][0]		#geting last key from dictionary
#     				dreams[last_key].append(text.text)			#and adding value to it
    
#     			elif int(text.attrib['font']) == 6: 			#font for dream
#     				for dream in text:							
#     					dreams[dream.text] = []					#addding new key - dream, to the dreams
    


#     for k,v in dreams.items():                                  #adding from ordered dictionary to unordered
#     	to_database[k] = str(' '.join(v))
#     try:
#         for k, v in to_database.items():
#             dream = Dream(name = k, description = v)
#             db.session.add(dream)
#             db.session.commit()
#         return redirect(url_for('main.index'))
#     except:
#         return "Oops something went wrong"