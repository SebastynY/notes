from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('notes-list/', views.get_notes, name='notes_list'),
    path('add-notes/', views.add_notes, name='add_notes'),
    path('notes/delete/<int:note_id>/', views.delete_notes, name='delete_notes'),
    path('edit-notes/<int:note_id>/', views.edit_notes, name='edit_notes'),
]
