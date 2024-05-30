from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('proyecto/<str:nombre>/', views.proyecto, name='proyecto'),
    path('proyecto/edit_proyecto', views.edit, name='edit'),
    path('proyecto/add_tarea', views.add_tarea, name='add_tarea'),
    path('tarea/<int:id>', views.tarea, name='tarea'),
    path('tarea/edit_task', views.edit_task, name='edit_task'),
    path('tarea/eliminar/<str:nombre>/<int:id>', views.eliminar_tarea, name='eliminarTarea'),
    path('proyecto/eliminar/<int:id>', views.eliminar_proyecto, name='eliminarProyecto'),
    path('proyecto/actualizarEstado/<int:id>', views.actualizarEstado, name='actualizarEstado'),
]