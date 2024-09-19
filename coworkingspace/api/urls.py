from .views import (CustomAuthToken, CustomRegisterToken, GetWorkspace, 
                    AddWorkspace, GetWorkspaceById, GetLocations, SearchByLocation)
from django.urls import path

urlpatterns = [
    path('login/', CustomAuthToken.as_view()),
    path('register/', CustomRegisterToken.as_view()),
    path('get-workspaces/', GetWorkspace.as_view()),
    path('add-workspaces/', AddWorkspace.as_view()),
    path('get-workspaces/<int:pk>/', GetWorkspaceById.as_view()),
    path('get-locations/', GetLocations.as_view()),
    path('search-workspaces/', SearchByLocation.as_view()),
]
