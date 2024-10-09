from rest_framework import serializers
from .models import ChatbotFileURL , ChatbotDesign , QA , SMS, Email, chatbot , WebsiteFileURL , Chat ,  Form  , HumanAssistant , ReplyEmail , ReplySMS


class chatbotserializer(serializers.ModelSerializer):

    class Meta:
        model=chatbot
        fields='__all__'



class ChatbotFileURLSerializers(serializers.ModelSerializer):
        
    FilePath = serializers.ListField(child=serializers.CharField(max_length=255))
    
    class Meta:
        model=ChatbotFileURL
        fields="__all__"


class WebURLSerializers(serializers.ModelSerializer):
        
    
    class Meta:
        model=WebsiteFileURL
        fields="__all__"


class ChatbotDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model=ChatbotDesign
        fields='__all__'

    def to_internal_value(self, data):
        if self.instance and 'chatbotID' in data:
            data.pop('chatbotID')  # Remove chatbotID from update data
        return super().to_internal_value(data)



class CreateChatSerializer(serializers.ModelSerializer):
    class Meta:
        model= Chat 
        fields='__all__'

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model=QA
        fields='__all__'


class HumanAssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model=HumanAssistant
        fields='__all__'

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model=Form
        fields='__all__'

class EmailSerializer(serializers.ModelSerializer):
    formatted_email = serializers.SerializerMethodField()

    class Meta:
        model = Email
        fields = ['recipient_email', 'subject', 'message_body', 'status', 'sent_at', 'formatted_email']

    def get_formatted_email(self, obj):
        return f"""
        To: {obj.recipient_email}
        Subject: {obj.subject}
        
        {obj.message_body}
        
        Status: {obj.status}
        Sent at: {obj.sent_at.strftime('%Y-%m-%d %H:%M:%S')}
        """
class SmsSerializer(serializers.ModelSerializer):
    formatted_sms = serializers.SerializerMethodField()

    class Meta:
        model = SMS
        fields = ['phone_number', 'message_body', 'status', 'sent_at', 'formatted_sms']

    def get_formatted_sms(self, obj):
        return f"""
        To: {obj.phone_number}

        {obj.message_body}
        
        Status: {obj.status}
        Sent at: {obj.sent_at.strftime('%Y-%m-%d %H:%M:%S')}
        """


class EmailReplySerializer(serializers.ModelSerializer):
    class Meta:
        model=ReplyEmail
        fields='__all__'

class SMSReplySerializer(serializers.ModelSerializer):
    class Meta:
        model=ReplySMS
        fields='__all__'


