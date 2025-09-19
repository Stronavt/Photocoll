document.addEventListener('DOMContentLoaded', function() {
    const url = followUrl; 
  const csrftokenValue = csrftoken;

  const optionsBase  = {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftokenValue
    },
    mode: 'same-origin'
  };

  const followButton = document.querySelector('a.follow');
  if (!followButton) return;

  followButton.addEventListener('click', function(e){
    e.preventDefault();
    var followButton = this;

    const formData = new FormData();
    formData.append('id', followButton.dataset.id);
    formData.append('action', followButton.dataset.action);
    const options = Object.assign({}, optionsBase, { body: formData });

    fetch(url, options)
    .then(response => response.json())
    .then(data => {
      if (data['status'] === 'ok')
      {
        var previousAction = followButton.dataset.action;

        var action = previousAction === 'follow' ? 'unfollow' : 'follow';
        followButton.dataset.action = action;
        followButton.innerHTML = action;

        var followerCount = document.querySelector('span.count .total');
        var totalFollowers = parseInt(followerCount.innerHTML);
        followerCount.innerHTML = previousAction === 'follow' ? totalFollowers + 1 : totalFollowers - 1;
      }
    });
  });
});