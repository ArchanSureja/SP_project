import datetime
import json
import os
from time import timezone
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from .models import Media, Note,Text,collabs, Template
from django.contrib.auth.decorators import login_required
from django import forms
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

@login_required
def templatesave(request, note_id, template_id):
    if request.method == 'POST':
        try:
            note = Note.objects.get(id=note_id)
            template = Template.objects.get(id=template_id)
            data = json.loads(request.body)
            content = json.dumps(data)  # Convert data back to JSON string
            template.content = content
            template.save()
            print(data)
            print(content)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def get_existing_rows(request, note_id, template_id):
    try:
        template = Template.objects.get(id=template_id)
        content = template.content  # Assuming content is stored as JSON in the template model
        existing_rows = json.loads(content)
        return JsonResponse({'success': True, 'rows': existing_rows})
    except Template.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Template not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

@login_required
def daily_schedule(request, note_id):
    note = Note.objects.get(id=note_id)
    return render(request, "note/Daily_Schedule.html", {'note':note})

@login_required
def week_schedule(request, note_id):
    note = Note.objects.get(id=note_id)
    return render(request, "note/week_Schedule.html", {'note':note})

@login_required
def todo(request, note_id):
    note = Note.objects.get(id=note_id)
    return render(request, "note/To_Do.html", {'note':note})


@login_required
def see_perticular_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    media = Media.objects.filter(belong_to=note)
    text = Text.objects.filter(belong_to=note)
    collab = collabs.objects.filter(note_id=note)
    return render(request, "note/see_note.html", {"note": note, "media": media, "text": text, "collab": collab})



@login_required
def create_note_form(request):
    users = User.objects.all()
    return render(request, "note/create_note.html", {'users' : users})

    
@login_required
def edit_note_form_m(request, note_id, error=None):
    note_with_text = Note.objects.get(id=note_id)
    media = Media.objects.filter(belong_to=note_id)
    text = Text.objects.filter(belong_to=note_id)
    collab = collabs.objects.filter(note_id = note_with_text)
    print(text)
    print(media)
    print(collab)
    return render(request, "note/edit.html", {"note": note_with_text, "media": media, "text": text, "collab": collab, "error": error})

@login_required
def edit_note_form_c(request, note_id):
    note_with_text = Note.objects.get(id=note_id)
    media = Media.objects.filter(belong_to=note_id)
    text = Text.objects.filter(belong_to=note_id)
    print(text)
    print(media)
    return render(request, "note/edit_collab.html", {"note": note_with_text, "media": media, "text": text})


@login_required
def edit_notes_c(request, note_id):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=note_id)
        note.lastModified = datetime.datetime.now()
        version = note.version
        note.version = version + 1
        note.modifications += f"\nLast modified by collaborator {request.user.username} at time  {note.lastModified}"
        # Update other attributes of the note as needed
        note.save()


        # Update related Text object(s)
        text_data = request.POST.get('data')
        is_bold = request.POST.get('IsBold') == '1'
        is_italic = request.POST.get('IsItalic') == '1'
        is_underline = request.POST.get('IsUnderline') == '1'
        align = request.POST.get('align')
        style = request.POST['style']
        texts = Text.objects.filter(belong_to=note)
        for text in texts:
            text.data = text_data
            text.IsBold = is_bold
            text.IsItalic = is_italic
            text.IsUnderline = is_underline
            text.align = align
            text.style = style
            # Update other attributes of Text object as needed
            text.save()

        # Update related Media object
        media_type = request.POST.get("media_type")
        if media_type:
            details = request.FILES.get('details')
            if details:
                media_folder = os.path.join(settings.MEDIA_ROOT, 'medias')
                if not os.path.exists(media_folder):
                    os.makedirs(media_folder)

                media_path = os.path.join(media_folder, details.name)
                with open(media_path, 'wb+') as destination:
                    for chunk in details.chunks():
                        destination.write(chunk)

                # Create or update Media object
                Media.objects.create(media_type=media_type, details=os.path.join('medias', details.name), belong_to=note)

        # Call function to send email to note creator
        modification = datetime.datetime.now()
        subject = 'Edit note by collaborator'
        message = f"""\
Title: {note.title}
Collaborator: {request.user.username}
Modification Time: {modification}
Version: {version}

Dear {note.createdBy.username},

We would like to inform you that your note has been edited by collaborator {request.user.username} 
at {modification}. The note is now in version {version}.

Best regards,
Your Collaborator
"""
        email_from = settings.EMAIL_HOST_USER
        recipient_email = [note.createdBy.email]  # Assuming createdBy is a User instance with email field
        send_mail(subject, message, email_from, recipient_email)


    return redirect('note:view_notes')




@login_required
def edit_notes_m(request, note_id):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=note_id)
        note.title = request.POST['title']
        note.label = request.POST['label']
        note.lastModified = datetime.datetime.now()
        version = note.version
        note.version = version + 1
        note.modifications += f"\nLast modified by {note.createdBy.username} at time  {note.lastModified}"
        # Update other attributes of the note as needed
        note.save()

        # Update related Text object(s)
        text_data = request.POST['data']
        is_bold = request.POST.get('IsBold') == '1'
        is_italic = request.POST.get('IsItalic') == '1'
        is_underline = request.POST.get('IsUnderline') == '1'
        align = request.POST['align']
        style = request.POST['style']
        print(style)
        texts = Text.objects.filter(belong_to=note)
        for text in texts:
            text.data = text_data
            text.IsBold = is_bold
            text.IsItalic = is_italic
            text.IsUnderline = is_underline
            text.align = align
            text.style = style
            # Update other attributes of Text object as needed
            text.save()

        # Update related Media object
        media_type = request.POST.get("media_type")
        if media_type:
            details = request.FILES.get('details')
            if details:
                media_folder = os.path.join(settings.MEDIA_ROOT, 'medias')
                if not os.path.exists(media_folder):
                    os.makedirs(media_folder)

                media_path = os.path.join(media_folder, details.name)
                with open(media_path, 'wb+') as destination:
                    for chunk in details.chunks():
                        destination.write(chunk)

                # Create or update Media object
                Media.objects.create(media_type=media_type, details=os.path.join('medias', details.name), belong_to=note)

        # Update collaborator information
        error_messages = ""
        collaborator_names = request.POST.getlist('collaborator_name')
        collaborator_permissions = request.POST.getlist('collaborator_permission')
        for name, permission in zip(collaborator_names, collaborator_permissions):
            if name and permission:
                try:
                    collaborator_user = User.objects.get(username=name)
                    collaborator, created = collabs.objects.get_or_create(user_id=collaborator_user, note_id=note)
                    collaborator.permission = permission
                    collaborator.save()
                except User.DoesNotExist:
                    error_messages = f"User '{name}' does not exist."
                    return redirect('note:edit_note_form_m', note_id=note_id, error = error_messages)

    return redirect('note:view_notes')





@login_required
def delete_media(request, media_id):
    media = Media.objects.get(pk = media_id)
    media.delete()
    return redirect('note:view_notes')


@login_required
def delete_note(request, note_id):
    note = Note.objects.get(pk = note_id)
    note.delete()
    return redirect('note:view_notes')


@login_required
def delete_collab(request, c_id):
    c = collabs.objects.get(pk = c_id)
    c.delete()
    return redirect('note:view_notes')


@login_required
def create_notes(request):
    if request.method == 'POST':
        # Note
        title = request.POST['title']
        createdBy = request.user
        label = request.POST['label']
        version = 1
        lastModified = datetime.datetime.now()
        modifications = f"last modified by {createdBy.username} at time {lastModified}"
        templateUsedTitle = request.POST['templateUsed']

        temTitle = templateUsedTitle
        temCreatedBy = request.user
        temContent = ""

        templateUsed = Template.objects.create(
            title = temTitle,
            createdBy = temCreatedBy,
            content = ""
        )
        # Note object
        note = Note.objects.create(
            title=title,
            createdBy=createdBy,
            label=label,
            version=version,
            lastModified=lastModified,
            modifications=modifications,
            templateUsed=templateUsed
        )

        # Text
        data = request.POST['data']
        is_bold = request.POST.get('IsBold') == 'on'
        is_italic = request.POST.get('IsItalic') == 'on'
        is_underline = request.POST.get('IsUnderline') == 'on'
        align = request.POST.get("align")
        # Text Object
        text = Text.objects.create(
            data=data,
            style="",       
            IsBold=is_bold,
            IsItalic=is_italic,
            IsUnderline=is_underline,
            align=align,
            belong_to=note       
        )

        # Media
        media_type = request.POST.get("media_type")
        if media_type:
            details = request.FILES.get('details')
            if details:
                media_folder = os.path.join(settings.MEDIA_ROOT, 'medias')
                if not os.path.exists(media_folder):
                    os.makedirs(media_folder)

                media_path = os.path.join(media_folder, details.name)
                with open(media_path, 'wb+') as destination:
                    for chunk in details.chunks():
                        destination.write(chunk)

                # Create or update Media object
                Media.objects.create(media_type=media_type, details=os.path.join('medias', details.name), belong_to=note)


        return redirect('note:view_notes')
    else:
        return render(request, "note/create_note.html")

    

@login_required
def view_notes(request):
    user_notes = get_user_notes(request.user.id)
    collabs_notes = get_collabs_notes(request.user.id)
    users = User.objects.all()
    return render(request, 'note/view_note.html', {'user_notes': user_notes, 'collabs_notes': collabs_notes, 'users':users})    


@login_required
def add_collabs(request):
    if request.method == 'POST':
        username = request.POST.get("user_id")  # Updated to match the HTML form field name
        note_id = request.POST.get("note_id")
        permission = request.POST.get("permission")
        
        # Attempt to get the user by username with error handling
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Handle the case where the user does not exist
            return HttpResponse(f"User '{username}' does not exist.<br><button onclick='window.history.back()'>OK</button>")
    
        try:
            note = Note.objects.get(pk=note_id)
        except Note.DoesNotExist:
            # Handle the case where the note does not exist
            return HttpResponse(f"Note with ID '{note_id}' does not exist.<br><button onclick='window.history.back()'>OK</button>", status=404)
    
        # Check if the collaboration already exists
        if collabs.objects.filter(user_id=user, note_id=note).exists():
            return HttpResponse("Collaboration already exists.<br><button onclick='window.history.back()'>OK</button>", status=400)
    
        # Create the collaboration
        collab = collabs.objects.create(
            note_id=note,
            user_id=user,
            permission=permission
        )
        
        # Send email notification
        print("Preparing to send email notification")
        subject = 'Added as Collaborator'
        message = 'You have been added as a collaborator to a ShareNote note by '+ request.user.username
        email_from = settings.EMAIL_HOST_USER
        recipient_email = [user.email]  # Assuming user has an email attribute
        send_mail(subject, message, email_from, recipient_email)
        print("Email sent successfully")
        
    return redirect('note:view_notes')

# @login_required
# def add_collabs(request):
#     if request.method == 'POST':
#         user_id = request.POST.get("user_id")
#         note_id = request.POST.get("note_id")
#         permission = ""

        
#         note = Note.objects.get(pk = note_id)
#         user = User.objects.get(username=user_id)
#         collab = collabs.objects.create(
#             note_id = note,
#             user_id = user,
#             permission = permission
#         )
    
#     return redirect('note:view_notes')


# functions for getting user's notes with it's texts and medias and 
def get_user_notes(user_id):
    user = User.objects.get(id=user_id)
    notes_with_text = Note.objects.filter(createdBy=user).prefetch_related('text_set','media_set', 'collabs_set')
    return notes_with_text


def get_collabs_notes(user_id):
     collaborator_notes = Note.objects.filter(collabs__user_id=user_id).prefetch_related('text_set', 'media_set', 'collabs_set')
     return collaborator_notes






class NewNoteForm(forms.Form):
    title = forms.CharField(label="title")
    label = forms.CharField(label="label")
# def create_notes(request):
#     return render(request, 'note/create_note.html')

    