from django.urls import path
from testapp import views
from .middlewares.auth import  auth_middleware


urlpatterns = [
    path('emp_login/',views.emp_login, name='emp_login'),
    path('register/',views.register,name="register"),
    path('token/' , views.token_send , name="token_send"),
    path('success/' , views.success , name='success'),
    path('verify/<auth_token>' , views.verify , name="verify"),
    path('employee_logout/',views.employee_logout, name='employee_logout'),
    # path('employee_dashboard/',auth_middleware(views.employee_dashboard),name='emp_dash')
    path('customer_register/', auth_middleware(views.customer_register), name='cust_reg'),
    path('employee_profile_view/',auth_middleware(views.employee_profile_view), name='employee_profile_view'),
    path('customer_accepted/',auth_middleware(views.customer_accepted), name='customer_accepted'),
    path('customer_rejected/',auth_middleware(views.customer_rejected), name='customer_rejected')


]