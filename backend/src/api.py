import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks')
def retrieve_drinks():
  try:
    drinks = Drink.short.query.all()
    
    if len(drinks) == 0:
      abort(404)
      
    return jsonify({
      'success': True,
      'drinks': drinks
      })
  except:
    abort(422)

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
@requires_auth('get:drinks-details')
def retrieve_drinks_detail():
  try:
      drinks = Drink.long.query.all()

      if len(drinks) == 0:
        abort(404)

      return jsonify({
        'success': True,
        'drinks': drinks
        })
  except:
    abort(422)

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
@requires_auth('post:drinks')
def create_drink():
    body = request.get_json()
    
    new_title = body.get('title', None)
    new_recipe = body.get('recipe', None)
    search = body.get('search', None)
  
    try:
      drink = Drink(title=new_title, recipe=new_recipe)
      drink.insert()
      
      return jsonify({
        'success': True,
        'drinks': drink
        })
    except:
      abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
def update_book(drink_id):

    body = request.get_json()

    try:
      drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
      if drink is None:
        abort(404)

      if 'recipe' in body:
        drink.recipe = int(body.get('recipe'))

      drink.update()

      return jsonify({
        'success': True,
        'drinks': drink
      })
      
    except:
      abort(400)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(drink_id):
    try:
      drink = Drink.query.filter(Book.id == book_id).one_or_none()

      if drink is None:
        abort(404)

      drink.delete()

      return jsonify({
        'success': True,
        'delete': drink_id
      })

    except:
      abort(422)

## Error Handling
'''
Example error handling for unprocessable entity
'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': "Not Found"
      }), 404
  
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': "Unable to process the contained instructions"
      }), 422

@app.errorhandler(400)
def syntaxError(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': "Syntax error detected"
      }), 400  
      

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''

@app.errorhandler(AuthError)
def authError(error, status_code):
  return jsonify({
    'success': False,
    'error': error,
    'status_code': status_code
    })