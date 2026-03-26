import os   #python ke system folders access krne ke liye
class Config:    #project ka control
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev-code-ai-key'#system mein secret key hai ? YES->use it ; NO-> dev-code-key use karo(yeh secuity key hoti hai)
    BASE_DIR=os.path.abspath(os.path.dirname(__file__)) #project ka main folder ka path nikalo
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'app.db')#database kaha banega
    SQLALCHEMY_TRACK_MODIFICATIONS=False #database ke changes track mat karo, performance ke liye disable karte hain
    UPLOAD_FOLDER=os.path.join(BASE_DIR,'workspace') #jo ZIP upload hogi ,workspace folder mein saave hogi
    GEMINI_API_KEY='PASTE YOUR GEMINI API KEY HERE'