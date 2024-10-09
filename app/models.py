from django.db import models
from Auth.models import Auth



class chatbot(models.Model):
    ID=models.AutoField(primary_key=True)
    AuthID=models.ForeignKey(Auth , on_delete=models.CASCADE)
    Avatar=models.ImageField(upload_to='avatars/', null=True, blank=True)
    AuthEmail=models.CharField(max_length=255 , blank=False)
    Role = models.CharField(max_length=20, default='owner')
    createAT=models.DateTimeField(blank=True)
    LastMessageAT=models.DateTimeField(null=True,blank=True)
    chats = models.IntegerField(default=0)
    messages = models.IntegerField(default=0)
    

# class ChatbotDesign(models.Model):
#     ID = models.AutoField(primary_key=True)
#     chatbotID = models.ForeignKey(chatbot, on_delete=models.CASCADE)
#     ChatbotName = models.CharField(max_length=255 , blank=False)
#     ChatbotAssistant = models.CharField(max_length=255 , blank=False)
#     ChatChatbotColorOptions=(
#         ("PURPLE" , "PURPLE" ),( "RED" , "RED" ) , ("BLUE" , "BLUE"), ("LIGHT-BLUE" , "LIGHT-BLUE")
#     )
#     ChatbotColor = models.CharField(max_length=255  ,  choices=ChatChatbotColorOptions , blank=False) 
#     WidgetIcon = models.ImageField(upload_to='WidgetIcon/', null=True, blank=True)
#     WidgetIconColor = models.CharField(max_length=7, null=True , blank=False)  
#     LogoURL = models.URLField(max_length=200, null=True, blank=True)
#     Avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
#     AvatarURL = models.URLField(max_length=200, null=True, blank=True)
#     WelcomeMessage = models.TextField(null=True, blank=True)
#     UnableRelevantResponse = models.TextField(null=True, blank=True)
#     ToolTipsMessage = models.TextField(null=True, blank=True)
#     QuickPrompt = models.TextField(null=True, blank=True)
#     StartTime = models.CharField(max_length=255, null=True, blank=True)
#     EndTime = models.CharField(max_length=500 , null=True, blank=True)
#     WorkingDays = models.CharField(max_length=255, null=True, blank=True)  
#     EmailNotifMessage = models.TextField(null=True, blank=True)


class ChatbotDesign(models.Model):
    ID = models.AutoField(primary_key=True)
    chatbotID = models.ForeignKey(chatbot, on_delete=models.CASCADE)
    ChatbotName = models.CharField(max_length=255 , blank=False)
    Avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    WelcomeMessage = models.TextField(null=True, blank=True)
    UnableRelevantResponse = models.TextField(null=True, blank=True)
    is_enabled = models.BooleanField(default=False)
    monday_start = models.CharField(max_length=255 ,null=True, blank=True)
    monday_end = models.CharField(max_length=255 ,null=True, blank=True)
    tuesday_start = models.CharField(max_length=255 , null=True, blank=True)
    tuesday_end = models.CharField(max_length=255 , null=True, blank=True)
    wed_start = models.CharField(max_length=255 , null=True, blank=True)
    wed_end = models.CharField(max_length=255 , null=True, blank=True)
    thur_start = models.CharField(max_length=255 , null=True, blank=True)
    thur_end = models.CharField(max_length=255 , null=True, blank=True)
    fri_start = models.CharField(max_length=255 , null=True, blank=True)
    fri_end = models.CharField(max_length=255 , null=True, blank=True)


class ChatbotFileURL(models.Model):
    ID =models.AutoField(primary_key=True)
    chatbotDesignID = models.ForeignKey(ChatbotDesign, on_delete=models.CASCADE)
    chatbotID = models.ForeignKey(chatbot, on_delete=models.CASCADE)
    FilePath = models.CharField(max_length=233)  # Assuming file path won't exceed 255 characters


class WebsiteFileURL(models.Model):
    ID =models.AutoField(primary_key=True)
    chatbotDesignID = models.ForeignKey(ChatbotDesign, on_delete=models.CASCADE)
    chatbotID = models.ForeignKey(chatbot, on_delete=models.CASCADE)
    WebURL = models.JSONField(max_length=233)  # Assuming file path won't exceed 255 characters


class Chat(models.Model):
    ID=models.AutoField(primary_key=True)
    Title=models.CharField(max_length=255, blank=True)
    chatbotID = models.ForeignKey(chatbot, on_delete=models.CASCADE)


class QA(models.Model):
    ID= models.AutoField(primary_key=True)
    chatID = models.ForeignKey(Chat, on_delete=models.CASCADE)
    QAL=models.JSONField()
    # ChatTitle=models.CharField()


class HumanAssistant(models.Model):
    ID = models.AutoField(primary_key=True)
    chatbotID = models.ForeignKey(chatbot, on_delete=models.CASCADE)
    chatID = models.ForeignKey(Chat, on_delete=models.CASCADE)

class Form(models.Model):
    ID = models.AutoField(primary_key=True)
    HumanAssistantID = models.ForeignKey(HumanAssistant, on_delete=models.CASCADE)
    Name = models.CharField(max_length=255, blank=True)
    Phone = models.CharField(max_length=255, blank=True)
    Email = models.CharField(max_length=255, blank=True)
    Subject = models.CharField(max_length=255, blank=True)
    Message = models.TextField(blank=True)
    method= models.CharField(max_length=255, blank=True)

class SMS(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    message_body = models.TextField()
    message_sid = models.CharField(max_length=64)
    status = models.CharField(max_length=20)
    sent_at = models.DateTimeField(auto_now_add=True)

class Email(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=255)
    message_body = models.TextField()
    status = models.CharField(max_length=20)
    sent_at = models.DateTimeField(auto_now_add=True)
    method= models.CharField(max_length=255)


class ReplySMS(models.Model):
    ID = models.AutoField(primary_key=True)
    SMSID = models.ForeignKey(SMS, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    reply_body = models.TextField()
    message_sid = models.CharField(max_length=64)
    status = models.CharField(max_length=20)
    sent_at = models.DateTimeField(auto_now_add=True)

class ReplyEmail(models.Model):
    ID = models.AutoField(primary_key=True)
    EmailID = models.ForeignKey(Email, on_delete=models.CASCADE)
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=255)
    reply_body = models.TextField()
    status = models.CharField(max_length=20)
    sent_at = models.DateTimeField(auto_now_add=True)




