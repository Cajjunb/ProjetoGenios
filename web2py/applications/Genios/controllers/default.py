#Metodo principal
def index():
    message= "WHAAT?"
    return dict(message=message)

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
