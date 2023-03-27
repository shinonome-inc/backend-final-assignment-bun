function renderBtn(likeBtn) {
  const isLiked = likeBtn.dataset.isLiked === 'T'
  likeBtn.innerText = `${isLiked ? '♥' : '♡'} ${likeBtn.dataset.likeCount}`
  likeBtn.style.color = isLiked ? 'red' : 'gray'
}
for (const likeBtn of document.getElementsByClassName('likebtn')) {
  renderBtn(likeBtn)
  likeBtn.addEventListener('click',
    async () => {
      const count = parseInt(likeBtn.dataset.likeCount)
      const isLiked = likeBtn.dataset.isLiked === 'T'
      await fetch(
        `/tweets/${likeBtn.dataset.pk}/${isLiked ? 'unlike' : 'like'}/`,
        { method: 'POST', headers: { 'X-CSRFToken': '{{ csrf_token }}' } },
      )
      likeBtn.dataset.likeCount = count + (isLiked ? -1 : 1)
      likeBtn.dataset.isLiked = isLiked ? 'F' : 'T'
      renderBtn(likeBtn)
    }
  )
}
