from flask import Flask #сам микрофреймворк
from flask import render_template, redirect #визуализация html-шаблона и автопереход на указанную страницу
from flask_wtf import FlaskForm #работа с формами
from wtforms import StringField, IntegerField, SubmitField, RadioField, FileField #импорт типов полей форм
from wtforms.validators import DataRequired, Email #.validators для автоматической проверки полей
                                                    #Нужно установить 'email_validator'
#from flask_uploader.validators import FileRequired нужно pip install Flask-Reuploaded
from werkzeug.utils import secure_filename #для защиты сервера от имени файла'''
import os #создание пути файла

app = Flask(__name__) #объект сайта

jsusers = { "diusers": [ {"id": 1, "name": "John", "gender": "Male", "image": None} ] }


#Создание wtf-формы для ввода значений регистрации
class RegistrationWTF(FlaskForm): #класс-наследник от класса FlaskForm
    id = IntegerField(validators=[DataRequired()]) #DataRequired - обязательно для ввода
    name = StringField(validators=[DataRequired()])
    '''phone = TelField()
    email = StringField(validators=[InputRequired(), Email() ])'''
    gender = RadioField("Укажите свой пол",
                        choices = [('Male', 'Male'),
                                   ("Female", 'Female')])
    image = FileField('Фото профиля', validators=[DataRequired()]) #проверка факта отправки файла (FileRequired). Если его нет-создается пуста ячейка и ошибка при обработке не вылетает

    submit = SubmitField(label= ('Sumbit')) #кнопка для отправки формы

#декоратор, отвечающий за показ главной страницы (принимает запрос для нее)
@app.route('/') #Параметр "/" значит, что открывается главная (первая) страница сайта
#после захода на главную страницу, запускается функция
def mapage():
    #отображение html-шаблона на главной странице
    return render_template('mainpage.html') 


#регистарция
@app.route('/registration', methods=['GET', 'POST']) #POST-запрос - отправка данных на сервер 
#По умолчанию декоратор принимает только GET-запросы (отправка данных с сервера)
#функция срабатывает после заполнения формы
def registration():
    #global jsusers
    form = RegistrationWTF() #объект класса (экземпляр формы)

    #если был отправлен post-запрос (пользователь отправил заполненную форму)
    if form.validate_on_submit(): #Проверяем, была ли форма отправленна  пользователем и прошла ли валидацию
        #Получаем данные из полей формы
        id, name, gender, image = form.id.data, form.name.data, form.gender.data, form.image.data

        filename = secure_filename(image.filename) #Защита сервера от имени файла (замена имени) (img.png = img_.png)
        print(filename) #Wojak.png
        image.save( os.path.join(app.instance_path, 'uploads', filename).replace('/','\\')) #app.instance_path - более развернутый путь (начиная с диска C)
        #imgsaferoad = os.path.join('uploads', filename).replace('/','\\') #'Image\\Wojak.png'
        #image.save(imgsaferoad)#os.path.join - соединение имени папки и имени файла для создания пути, 
                                                    #по которому будет сохранено изображение (img.save(путь))

        #добавление нового пользователя в словарь с пользователями
        newus = {"id": id, "name": name, "gender": gender, "image": filename}
        print(newus)
        jsusers["diusers"].append(newus)
        
        return redirect('welcome.html', name=name, filename=filename) #f'{name}, registration complited successfully!'

    #если был отправлен get-запрос (на получение формы) или если условие не сработало, 
    #возвращаем html с формой. И объект form для передачи полей формы, которые надо заполнить, в html документ
    return render_template('wtf_form.html', form=form) #обозначаем, что переменную form мы будем использовать в html-файле
                                                        #чтобы wtf_form видел переменную form из файла app.py


#вывод информации о зарегестрированном пользователе
@app.route('/users', defaults={'id': None}) #если id не указан
@app.route('/users/<id>') #параметр id в запросе
def users(id):
    if id == None:

        return render_template('userpage.html', data = jsusers, allusers = len(jsusers["diusers"]))
    else: #Перебираем весь словарь diusers, сравнивая id пользователя с id в параметре
        for user in jsusers["diusers"]:
            if user["id"] == int(id):
                return f'Name: {user["name"]},  ID: {user["id"]}, Gender {user["gender"]}'
        #Если ни одно id не совпало
        return f'Such user does not exist'
    
@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

#Код для запуска любой программы на Flask
if __name__=="__main__":
    app.config['WTF_CSRF_ENABLED']=False #для формы, чтобы при ее запросе не вылетала ошибка A secret key is required to use CSRF.
    app.run(debug=True) 

