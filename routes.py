from sqlalchemy.sql.functions import user
import api 
from flask import Flask, jsonify, request
 
app = Flask(__name__)
 
@app.route('/api/user/', methods=['POST'])
def create_user():
    payload = request.form.to_dict()
    result = api.add_user(**payload)
    if result:
        return jsonify(status='True', message='User created')
    return jsonify(status='False')

@app.route('/api/user/<id>', methods=['GET'])
def get_user(id):
    result = api.get_user_by_id(id)
    if result:
        return jsonify(status="True", 
                    result={"Nom":result.nom,
                            "Prenom":result.prenom,
                            "email":result.mail,
                            "Date de naissance": result.birth_date,
                            "Ville": result.id_city,
                            "Categorie": result.id_specific_category}
                        )
    return jsonify(status="False")

@app.route('/api/userSearch/<id_city>/<id_specific_category>/<available>', methods=['GET'])
def get_user_search(id_city, id_specific_category, available):
    result = api.get_user_by_search(id_city, id_specific_category, available)
    print(result)
    if result:
        return jsonify(status="True", 
                    result= [
                        {
                            "Nom":user.nom,
                            "Prenom":user.prenom,
                            "Date de naissance": user.birth_date,                        } 
                        for user in result.all() ])
    return jsonify(status="False")

@app.route('/api/user/<id>', methods=['PUT'])
def mofify_user(id):
    result = api.update_attribute(id, request.form.to_dict())
    if result:
        return jsonify(status="True",
                        message= "updated",
                        result={
                            "nom":result.nom,
                            "prenom":result.prenom}
                            )
    return jsonify(status= "False")

@app.route('/api/category', methods=['GET'])
def get_all_category():
    result = api.get_all_category()
    if result:
        return jsonify(status="True", 
        result= [
            {"nom":category.nom,
             "id": category.id} for category in result.all() ])
    return jsonify(status="False")

@app.route('/api/category/specific', methods=['GET'])
def get_all_specific_category():
    result = api.get_all_specific_category()
    if result:
        return jsonify(status="True", 
        result= [
            {"nom":specific_category.name_specific_category,
             "id_category":specific_category.id_category} for specific_category in result.all() ])
    return jsonify(status="False")

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)