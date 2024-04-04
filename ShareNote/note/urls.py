from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views 
app_name="note"
urlpatterns = [
    path("", views.view_notes, name="view_notes"),
    path("create_note_form/", views.create_note_form, name="create_note_form"),
    path("create/", views.create_notes, name="create_notes"),
    path("add_collabs", views.add_collabs, name="add_collabs"),
    path("main/<int:note_id>/<str:error>", views.edit_note_form_m, name="edit_note_form_m"),
    path("main_edit/<int:note_id>/", views.edit_notes_m, name="edit_notes_m"),

    path("collab/<int:note_id>", views.edit_note_form_c, name="edit_note_form_c"),
    path("collab_edit/<int:note_id>/", views.edit_notes_c, name="edit_notes_c"),

    path("note/<int:note_id>", views.see_perticular_note, name="see_perticular_note"),

    path("delete_media/<int:media_id>/", views.delete_media, name="delete_media"),
    path("delete_note/<int:note_id>/", views.delete_note, name="delete_note"),
    path("delete_collab/<int:c_id>/", views.delete_collab, name="delete_collab"),


    path("daily_schedule/<int:note_id>/", views.daily_schedule, name="daily_schedule"),
    path("templatesave/<int:note_id>/<int:template_id>/", views.templatesave, name='template_save'),
    path("get_existing_rows/<int:note_id>/<int:template_id>/", views.get_existing_rows, name='get_existing_rows'),

    
    path("week_schedule/<int:note_id>/", views.week_schedule, name="week_schedule"),
    path("todo/<int:note_id>/", views.todo, name="todo"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

