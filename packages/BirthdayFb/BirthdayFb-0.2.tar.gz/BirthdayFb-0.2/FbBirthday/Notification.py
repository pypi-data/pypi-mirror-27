from gi.repository import Notify,GdkPixbuf
from Facebook_Creds import Event_Url,App_Name		
Notify.init(App_Name)
def notify_event():
	notification = Notify.Notification.new('Some of your Friends might have Birthday today')
	image = GdkPixbuf.Pixbuf.new_from_file("Resource/birthday.png")
	return notification

def no_birthday_today():
	notification = Notify.Notification.new("No assHoles Born Today","isn't this great")
	image = GdkPixbuf.Pixbuf.new_from_file("Resource/assholes.svg")
	notification.set_icon_from_pixbuf(image)
	notification.set_image_from_pixbuf(image)
	return notification



def success_notification():
	notification = Notify.Notification.new("Happy Birthday","wishing your friends happy birthday")
	image = GdkPixbuf.Pixbuf.new_from_file("Resource/birthday.png")
	notification.set_icon_from_pixbuf(image)
	notification.set_image_from_pixbuf(image)
	return notification


	
