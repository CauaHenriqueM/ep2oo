from bottle import Bottle, request, response
from config import Config
from .base_controller import BaseController
from services.user_service import UserService

class UserController(BaseController):
    def __init__(self, app):
        super().__init__(app)

        self.setup_routes()
        self.user_service = UserService()


    # Rotas User
    def setup_routes(self):
        self.app.route('/login', method=['GET', 'POST'], callback=self.login)
        self.app.route('/users', method='GET', callback=self.list_users)
        self.app.route('/users/register', method=['GET', 'POST'], callback=self.register)
        self.app.route('/users/add', method=['GET', 'POST'], callback=self.add_user)
        self.app.route('/users/edit/<user_id:int>', method=['GET', 'POST'], callback=self.edit_user)
        self.app.route('/users/delete/<user_id:int>', method='POST', callback=self.delete_user)

    def login(self):
        if request.method == 'GET':
            return self.render('login', error=None, email=None)
        email = request.forms.get('email')
        password = request.forms.get('password')
        if not email or not password: 
            return self.render('login', error="Email e senha são obrigatórios", email=email)
        user = self.user_service.login(email, password)
        if user:
            response.set_cookie("user_id", str(user.id), 
                                 secret=Config.SECRET_KEY, 
                                 httponly=True, 
                                 path='/')
            response.set_cookie("user_name", user.name, 
                                 secret=Config.SECRET_KEY, 
                                 httponly=True, 
                                 path='/')
            return self.redirect("/users")#aqui eu quero fazer um bool pra privilegios de admin futuramente
        else:
            return self.redirect('/login')
    
    def list_users(self):
        users = self.user_service.get_all()
        return self.render('users', users=users)


    def add_user(self):
        if request.method == 'GET':
            return self.render('user_form', user=None, action="/users/add")
        else:
            # POST - salvar usuário
            self.user_service.save()
            self.redirect('/users')


    def edit_user(self, user_id):
        user = self.user_service.get_by_id(user_id)
        if not user:
            return "Usuário não encontrado"

        if request.method == 'GET':
            return self.render(
                'user_form',
                user=user,
                action=f"/users/edit/{user_id}"
            )
        else:
            # POST - atualizar usuário ps: eu tive uma dificuldade da porra pra arrumar essa parte aqui, só depois que fui entender q tava dando erro no maldito form
            name = request.forms.get('name')
            email = request.forms.get('email')
            new_password = request.forms.get('password')
            if not new_password:
                new_password = None
            self.user_service.edit_user(user, name, email, new_password)
            self.redirect('/users')


    def delete_user(self, user_id):
        self.user_service.delete_user(user_id)
        self.redirect('/users')

    def register(self):
        if request.method == 'GET':
            return self.render('register', 
                                 error=None, 
                                 name='', 
                                 email='')
        else: # POST
            name = request.forms.get('name')
            email = request.forms.get('email')
            password = request.forms.get('password')

            try:
                self.user_service.register(name, email, password)
                return self.redirect('/login') 
            except ValueError as e:
                return self.render('register', 
                                     error=str(e), 
                                     name=name, 
                                     email=email)
            except Exception as e:
                print(f"ERRO INESPERADO NO REGISTRO: {str(e)}")
                return self.render('register', 
                                     error=f"Erro interno: {type(e).__name__} - {str(e)}", 
                                     name=name, 
                                     email=email)

user_routes = Bottle()
user_controller = UserController(user_routes)
