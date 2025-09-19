from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm, AddImageToAlbumForm, CommentForm, AlbumForm
from django.shortcuts import get_object_or_404
from .models import Image, Album, SavedImage
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from actions.utils import create_action



@login_required
def image_delete(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)

    if image.user != request.user:
        messages.error(request, 'У Вас нет прав для удаления изображения')
        return redirect('user_detail', request.user.username)

    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Изображение успешно удалено')
        return redirect('user_detail', request.user.username)  
    return render(request, 'images/image/delete_form.html', {'image': image})    



@login_required
def image_create_form(request):
    tags = Tag.objects.all().order_by('name')   

    if request.method == 'POST':
        form = ImageCreateForm(request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            form.save_m2m()
            albums = form.cleaned_data.get('albums')
            for album in albums:
                exists = SavedImage.objects.filter( user=request.user, image=new_image, album=album).exists()

            if not exists:
                SavedImage.objects.create(user=request.user, image=new_image, album=album)

            
            create_action(request.user, 'has created the image', new_image)
            messages.success(request, 'Image added successfully')
            return redirect('user_detail', request.user.username)
    else:
        form = ImageCreateForm(user=request.user)
    return render(request,
                  'images/image/create_image_form.html',
                  {
                   'form': form, 'tags': tags})


@login_required
def image_update_form(request, image_id):
    image = get_object_or_404(Image, id=image_id, user=request.user)
    tags = Tag.objects.all().order_by('name')

    if request.method == 'POST':
        form = ImageCreateForm(request.user, data=request.POST, files=request.FILES, instance=image)
        if form.is_valid():
            update_image = form.save(commit=False)

            update_image.user = request.user
            tags = Tag.objects.all().order_by('name')
            update_image.save()
            form.save_m2m()
            messages.success(request, 'Image update successfully')
            create_action(request.user, 'изменил(а) изображение', update_image)
            return redirect('images:list')
    else:
        form = ImageCreateForm(request.user, instance=image)
    return render(request, 'images/image/update_image_form.html',
                  {'form': form, 'tags': tags})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    comments = image.comments.filter(active=True)
    form = CommentForm()
    print('image: ', image.tags)
    return render(request, 'images/image/detail.html', {'section': 'images',
                   'image': image, 'comments': comments, 'form':form})


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                try:
                    create_action(request.user, 'likes', image)
                except Exception as e:
                    print(f"Error in create_action: {e}")
                
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def save_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    created = SavedImage.objects.get_or_create(user=request.user, image=image)
    if created:
        create_action(user=request.user, verb='saved image', target=image)
        messages.success(request, 'Image saved to your collection.')
    else:
        messages.info(request, 'Image is already in your collection.')
    return redirect('images:image_detail', id=image.id, slug=image.slug)


@login_required
def image_list(request, tag_slug=None):
    images = Image.objects.all().order_by('-created')

    search_input = request.GET.get('search-area') or ''
    if search_input:
        images = images.filter(title__icontains = search_input)

    tag = None
    if tag_slug: 
        tag = get_object_or_404(Tag, slug=tag_slug) 
        images = images.filter(tags__in=[tag])

    paginator = Paginator(images, 8)
    page = request.GET.get('page', 1)
    images_only = request.GET.get('images_only')


    try:
        images = paginator.get_page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
 



    if images_only:
        return render(request, 'images/image/list.html', 
                      {'section': 'images', 'images': images, 'search_input':search_input, 'tag': tag})
    return render(request, 'images/image/list.html', 
                  {'section': 'images', 'images': images, 'search_input':search_input, 'tag': tag})



@require_POST
@login_required
def add_image_to_album(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    form = AddImageToAlbumForm(request.user, request.POST)

    if form.is_valid():
        albums = form.cleaned_data['albums'] 

        for album in albums:
            exists = SavedImage.objects.filter( user=request.user, image=image, album=album).exists()

        if not exists:
            SavedImage.objects.create(user=request.user, image=image, album=album)
            create_action(request.user, 'сохранил(а) изображение в альбом', target=image)
            messages.success(request, 'Изображение сохранено')
            return redirect('images:list')
            #return JsonResponse({'status': 'ok', 'message': 'Изображение сохранено!'})
        messages.error(request, 'Уже сохранено в этом альбоме')
        return redirect('images:list')  
        #return JsonResponse({'status': 'error', 'message': 'Уже в этом альбоме'})
    else:
        errors = form.errors.as_json()
        return JsonResponse({ 'status': 'error', 'message': 'Ошибка валидации формы', 'errors': errors}, status=400)



@login_required
def remove_image_from_album(request, image_id, album_id):
    image = get_object_or_404(Image, id=image_id)
    album = get_object_or_404(Album, id=album_id, user=request.user)
    album.images.remove(image)
    SavedImage.objects.filter(user=request.user, image=image, album=album).delete()
    messages.success(request, "Изображение удалено")
    return redirect('images:list')





def album_detail(request, album_id, album_slug):
    album = get_object_or_404(Album,  id=album_id, slug=album_slug, user=request.user)
    images = Image.objects.filter(saved_by__album=album)
    # Если связь ForeignKey через Image.album:
    # images = Image.objects.filter(album=album) 

    return render(request, 'images/image/album_detail.html',{'album': album, 'images': images})



def add_comment(request, image_id):
    image = get_object_or_404(Image, id=image_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user 
            comment.image = image
            comment.save()    
            messages.success(request, 'comment added')   
            return redirect('images:detail', id=image.id, slug=image.slug)
    else:
        form = CommentForm()
    return render(request, 'images/image/comment_form.html', {'form':form, 'image':image})                



@login_required
def create_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            new_album = form.save(commit=False)
            new_album.user = request.user
            new_album.save()
            messages.success(request, 'album created')
            return redirect('user_detail', request.user.username )
    else:
        form = AlbumForm()
    return render(request, 'images/image/album_create_form.html', {'form': form})    

