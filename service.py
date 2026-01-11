from time import sleep
from jnius import autoclass
from kivy.storage.jsonstore import JsonStore

# Android-specific classes for notifications
PythonService = autoclass('org.kivy.android.PythonService')
NotificationBuilder = autoclass('android.app.Notification$Builder')
Context = autoclass('android.content.Context')
NotificationManager = autoclass('android.view.Context').NOTIFICATION_SERVICE

def send_notification(title, message):
    service = PythonService.mService
    notification_service = service.getSystemService(Context.NOTIFICATION_SERVICE)
    
    # Modern Android Notification Channel (Required for API 33+)
    builder = NotificationBuilder(service)
    builder.setContentTitle(title)
    builder.setContentText(message)
    builder.setSmallIcon(service.getApplicationInfo().icon)
    
    notification_service.notify(1, builder.build())

if __name__ == '__main__':
    store = JsonStore('health_data.json')
    while True:
        # Check every 60 seconds if an alarm should trigger
        if store.exists('settings'):
            water_alarm = store.get('settings').get('water_alarm', False)
            if water_alarm:
                send_notification("Stay Hydrated!", "It's time to drink 250ml of water.")
        
        sleep(3600) # Check every hour for water