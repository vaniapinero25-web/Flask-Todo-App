from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    data_created = db.Column(db.DateTime, default = datetime.utcnow)
   
    def __repr__(self) -> str: 
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET','POST'])
def my_todo():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc) 
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)
   



@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo) 
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')   
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

    
if __name__== "__main__ " : 
     app.run(debug=True)

categories = {}
category_id_counter = 1

@app.route('/api/categories', methods=['POST'])
def create_category():
    global category_id_counter
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Bad Request: 'name' is required"}), 400
    
    new_category = {"id": category_id_counter, "name": data['name']}
    categories[category_id_counter] = new_category
    category_id_counter += 1
    return jsonify(new_category), 201

@app.route('/api/categories', methods=['GET'])
def get_all_categories():
    return jsonify(list(categories.values())), 200

@app.route('/api/categories/<int:cat_id>', methods=['GET'])
def get_category(cat_id):
    category = categories.get(cat_id)
    if not category:
        return jsonify({"error": "Not Found"}), 404
    return jsonify(category), 200

@app.route('/api/categories/<int:cat_id>', methods=['PUT'])
def update_category(cat_id):
    data = request.get_json()
    category = categories.get(cat_id)
    
    if not category:
        return jsonify({"error": "Not Found"}), 404
    if not data or 'name' not in data:
        return jsonify({"error": "Bad Request: 'name' is required"}), 400
        
    category['name'] = data['name']
    return jsonify(category), 200

@app.route('/api/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    if cat_id in categories:
        del categories[cat_id]
        return jsonify({"message": "Category deleted successfully"}), 200
    return jsonify({"error": "Not Found"}), 404
   

    