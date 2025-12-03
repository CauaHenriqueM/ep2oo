from bottle import request
import bcrypt
from models.user import UserModel, User

class UserService:
    def __init__(self):
        self.user_model = UserModel()

    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def _check_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def get_all(self):
        users = self.user_model.get_all()
        return users


    def save(self):
        last_id = max([u.id for u in self.user_model.get_all()], default=0)
        new_id = last_id + 1
        name = request.forms.get('name')
        email = request.forms.get('email')
        
        user = User(id=new_id, name=name, email=email)
        self.user_model.add_user(user)


    def get_by_id(self, user_id):
        return self.user_model.get_by_id(user_id)
    
    

    def register(self, name: str, email: str, password: str):
        users = self.user_model.get_all()
        #aqui preciso colocar um verificador de email ja existente
        if any(u.email == email for u in users):
            return None  #-> nesse caso o email ja existe
        last_id = max([u.id for u in users], default=0)
        new_id = last_id + 1 #aqui o copilot falou q eu tava errando em botar o len(users)+1
        #                     ent eu deixei o copilot trabalhar la ele mil vezes
        hashed_password = self._hash_password(password)
        user = User(id=new_id, name=name, email=email, password=hashed_password) 
        self.user_model.add_user(user)
        return user
    
    def login(self, email: str, password: str):
        users = self.user_model.get_all()
        user = next((u for u in users if u.email == email), None)
        if user and self._check_password(password, user.password): #só um check pra ver se a senha ta certa mesmo
            return user
        return None

    def edit_user(self, user, name: str, email: str, new_password: str):
        if not all([user.id, user.name, user.email]):
            return  # Dados incompletos
        user.name = name
        user.email = email
        
        #dai agora sim mete a senha
        if new_password:
            user.password = self._hash_password(new_password)
        self.user_model.update_user(user)


    def delete_user(self, user_id):
        self.user_model.delete_user(user_id)
