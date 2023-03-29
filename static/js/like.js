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

function renderBtn(likeBtn) {
    const isLiked = likeBtn.dataset.isLiked === 'T';
    likeBtn.innerText = `${isLiked ? '♥' : '♡'} ${likeBtn.dataset.likeCount}`;
    likeBtn.style.color = isLiked ? 'red' : 'gray';
}

async function updateLikeState(likeBtn) {
    const count = parseInt(likeBtn.dataset.likeCount);
    const isLiked = likeBtn.dataset.isLiked === 'T';
    const csrftoken = getCookie('csrftoken');
    const headers = new Headers({
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    });
    const response = await fetch(`/tweets/${likeBtn.dataset.pk}/${isLiked ? 'unlike' : 'like'}/`, {
        method: 'POST',
        headers: headers,
    });
    if (response.ok) {
        likeBtn.dataset.likeCount = count + (isLiked ? -1 : 1);
        likeBtn.dataset.isLiked = isLiked ? 'F' : 'T';
        renderBtn(likeBtn);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    for (const likeBtn of document.getElementsByClassName('likebtn')) {
        renderBtn(likeBtn);
        likeBtn.addEventListener('click', async () => {
            await updateLikeState(likeBtn);
        });
    }
});

