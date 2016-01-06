#from app.models import Data
from app import app

@app.route("/api/test",methods=["GET","POST"])
def api_testing():
    return "Congradulations!  You've successfully authenticated to gi bill comparison tool.  But unfortunately we don't offer shell support"




