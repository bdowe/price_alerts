from flask import Blueprint, render_template, request, json, url_for
from werkzeug.utils import redirect

from src.models.stores.store import Store

import src.models.users.decorators as user_decorators

store_blueprint = Blueprint('stores', __name__)

@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('stores/store_index.html', stores=stores)

@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    return render_template('stores/store.html', store=Store.get_by_id(store_id) )

@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@user_decorators.requires_admin_permissions
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        title_tag_name = request.form['title_tag_name']
        title_query = json.loads(request.form['title_query'])
        price_tag_name = request.form['price_tag_name']
        price_query = json.loads(request.form['price_query'])

        store.name = name
        store.url_prefix = url_prefix
        store.title_tag_name = title_tag_name
        store.title_query = title_query
        store.price_tag_name = price_tag_name
        store.price_query = price_query

        store.save_to_mongo()

        return redirect(url_for('.index'))
    return render_template('stores/edit_store.html', store=store)

@store_blueprint.route('/delete/<string:store_id>')
@user_decorators.requires_admin_permissions
def delete_store(store_id):
    Store.get_by_id(store_id).delete()
    return redirect(url_for('.index'))


@store_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_admin_permissions
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        title_tag_name = request.form['title_tag_name']
        title_query = json.loads(request.form['title_query'])
        price_tag_name = request.form['price_tag_name']
        price_query = json.loads(request.form['price_query'])

        Store(name, url_prefix, title_tag_name, title_query, price_tag_name, price_query).save_to_mongo()

        return redirect(url_for('.index'))
    return render_template('stores/new_store.html')

