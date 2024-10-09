from rest_framework import routers
from django.urls import path, include
from .views import CreateChatbotDesign , ChatbotFileURLView , ChatView , SmsDashboard, chatbotView , CreateChatView , UserFormView , LogoutView, EmailDashboard , HumanAssistantButtonView , AdminFormView

router = routers.DefaultRouter()
# router.register('SellerCompanyOverview', SellerCompanyOverviewView)

router.register(r'Chatbot', chatbotView, basename='Chatbot')
router.register(r'ChatbotDesign', CreateChatbotDesign, basename='ChatbotDesign')
router.register(r'ChatbotURL', ChatbotFileURLView, basename='ChatbotURL')
router.register(r'ChatView', ChatView, basename='ChatView')
router.register(r'CreateChat', CreateChatView, basename='CreateChatView')
# router.register(r'FormView', FormView, basename='FormView')
router.register(r'UserFormView', UserFormView, basename='UserFormView')
router.register(r'AdminFormView', AdminFormView, basename='AdminFormView')
router.register(r'Logout', LogoutView, basename='Logout')
router.register(r'EmailDashboard', EmailDashboard, basename='EmailDashboard')
router.register(r'SmsDashboard', SmsDashboard, basename='SmsDashboard')
router.register(r'HumanAssistant', HumanAssistantButtonView, basename='HumanAssistant')
# router.register(r'ALL', CombinedView, basename='ALL')



# urlpatterns = [
#     path('Chatbot/EmailDashboard/<int:pk>/reply/', EmailDashboard.as_view({'post': 'reply_to_email'}), name='reply-to-email'),
#     path('Chatbot/EmailDashboard/<int:pk>/conversation/', EmailDashboard.as_view({'get': 'get_conversation'}), name='get-conversation'),
#     path('', include(router.urls)),
#     # other paths
# ]


urlpatterns = [
    path('Chatbot/EmailDashboard/<int:pk>/reply/', EmailDashboard.as_view({'post': 'reply_to_email'}), name='reply-to-email'),
    path('Chatbot/EmailDashboard/<int:pk>/conversation/', EmailDashboard.as_view({'get': 'get_conversation'}), name='get-conversation'),
    path('', include(router.urls)),
    # other paths
]


