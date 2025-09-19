document.addEventListener('DOMContentLoaded', () => {
  const url = likeUrl;  // глобальная переменная из шаблона
  const csrftokenValue = csrftoken; // глобальная переменная из шаблона

  const optionsBase = {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftokenValue,
      'X-Requested-With': 'XMLHttpRequest'
    },
    mode: 'same-origin'
  };

  const likeButton = document.querySelector('a.like');
  if (!likeButton) return;

  likeButton.addEventListener('click', function(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append('id', this.dataset.id);
    formData.append('action', this.dataset.action);

    const options = Object.assign({}, optionsBase, { body: formData });

    fetch(url, options)
      .then(response => response.json())
      .then(data => {
        if (data.status === 'ok') {
          const previousAction = this.dataset.action;
          const action = previousAction === 'like' ? 'unlike' : 'like';
          this.dataset.action = action;
          this.innerHTML = action;

          const likeCount = document.querySelector('span.count .total');
          if (likeCount) {
            let totalLikes = parseInt(likeCount.innerHTML);
            likeCount.innerHTML = previousAction === 'like' ? totalLikes + 1 : totalLikes - 1;
          }
        }
      })
      .catch(error => console.error('Error:', error));
  });
});

/*
  // AJAX для сохранения в альбом

    // Сохранение в альбом
    const saveForms = document.querySelectorAll('.save-form');
    saveForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const url = this.action;
            const messageDiv = this.nextElementSibling;
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => response.json())
            .then(data => {
                messageDiv.textContent = data.message;
                messageDiv.className = 'save-message ' + data.status;
                
                if (data.status === 'ok') {
                    this.reset(); // Очищаем форму
                    // Обновляем интерфейс при необходимости
                }
            })
            .catch(error => {
                console.error('Error:', error);
                messageDiv.textContent = 'Ошибка сохранения';
                messageDiv.className = 'save-message error';
            });
        });
    });
    // Удаление из альбома (на странице альбома)
    const removeButtons = document.querySelectorAll('.remove-from-album');
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const imageId = this.dataset.imageId;
            const albumId = this.dataset.albumId;
            const imageElement = this.closest('.image-item');
            
            if (confirm('Удалить изображение из альбома?')) {
                fetch(`/images/album/${albumId}/remove-image/${imageId}/`, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'ok') {
                        imageElement.remove(); // Плавно удаляем элемент
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    });


// Функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

{% block domready %}

  const url = '{% url "images:like" %}';
  var options = {
    method: 'POST',
    headers: {
    'X-CSRFToken': Cookies.get('csrftoken'),
    'X-Requested-With': 'XMLHttpRequest'
    },
    mode: 'same-origin'
  }


  document.querySelector('a.like')
          .addEventListener('click', function(e){
    e.preventDefault();
    var likeButton = this;

    // add request body
    var formData = new FormData();
    formData.append('id', likeButton.dataset.id);
    formData.append('action', likeButton.dataset.action);
    options['body'] = formData;

    // send HTTP request
    fetch(url, options)
    .then(response => response.json())
    .then(data => {
      if (data['status'] === 'ok')
      {
        var previousAction = likeButton.dataset.action;

        // toggle button text and data-action
        var action = previousAction === 'like' ? 'unlike' : 'like';
        likeButton.dataset.action = action;
        likeButton.innerHTML = action;

        // update like count
        var likeCount = document.querySelector('span.count .total');
        var totalLikes = parseInt(likeCount.innerHTML);
        likeCount.innerHTML = previousAction === 'like' ? totalLikes + 1 : totalLikes - 1;
      }
    })
  });


// Функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
{% endblock %}*/

/*const saveForms = document.querySelectorAll('.save-form');
    saveForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const url = this.action;
            const messageDiv = this.nextElementSibling;
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => response.json())
            .then(data => {
                messageDiv.textContent = data.message;
                messageDiv.className = 'save-message ' + data.status;
                
                if (data.status === 'ok') {
                    this.reset(); // Очищаем форму
                    // Обновляем интерфейс при необходимости
                }
            })
            .catch(error => {
                console.error('Error:', error);
                messageDiv.textContent = 'Ошибка сохранения';
                messageDiv.className = 'save-message error';
            });
        });
    });
        
      })*/