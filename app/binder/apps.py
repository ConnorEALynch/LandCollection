from django.apps import AppConfig



class BinderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'binder'
    

    #def ready(self):
        #send app is ready signal for getting BinderInfo
        #app_ready.connect(binderInfo_callback, sender=self)
        #app_ready.send(sender=self)







  
