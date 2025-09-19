document.addEventListener('DOMContentLoaded', function() {
  const loadMoreBtn = document.getElementById('load-more');
  const imageList = document.getElementById('image-list');

  if (!loadMoreBtn) return;  // Если кнопки нет — пагинация не нужна

  loadMoreBtn.addEventListener('click', function() {
    const nextPage = this.getAttribute('data-next-page');

    // Блокируем кнопку, чтобы избежать повторных кликов
    loadMoreBtn.disabled = true;
    loadMoreBtn.textContent = 'Loading...';

    fetch(`?images_only=1&page=${nextPage}`)
      .then(response => response.text())
      .then(html => {
        if (html.trim() === '') {
          // Нет больше страниц — скрываем кнопку
          loadMoreBtn.style.display = 'none';
        } else {
          // Добавляем новые изображения в список
          imageList.insertAdjacentHTML('beforeend', html);

          // Обновляем номер следующей страницы
          const newNextPage = parseInt(nextPage) + 1;

          // Проверяем, есть ли следующая страница (можно передавать это из backend через data-атрибут)
          // Для простоты считаем, что если пришёл html — следующая страница есть
          loadMoreBtn.setAttribute('data-next-page', newNextPage);
          loadMoreBtn.disabled = false;
          loadMoreBtn.textContent = 'Load More';
        }
      })
      .catch(error => {
        console.error('Error loading more images:', error);
        loadMoreBtn.disabled = false;
        loadMoreBtn.textContent = 'Load More';
      });
  });
});
