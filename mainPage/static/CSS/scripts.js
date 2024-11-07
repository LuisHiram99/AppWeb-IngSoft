let postIdCounter = 0;

function editPost(id) {

    fetch(`/reportes/${id}/edit/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('postTitle').value = data.title;
            document.getElementById('postArea').value = data.area;
            document.getElementById('postCategory').value = data.category;
            document.getElementById('postContent').value = data.content;
            // Si necesitas manejar la imagen, puedes hacerlo de forma similar.
        })
        .catch(error => console.error('Error al editar el post:', error));
}

function deletePost(id) {
    fetch(`/reportes/${id}/delete/`, { method: 'DELETE' })
        .then(response => {
            if (response.ok) {
                const postElement = document.querySelector(`.post[data-id='${id}']`);
                if (postElement) {
                    postElement.remove();
                }
            } else {
                alert('Error al eliminar el post');
            }
        })
        .catch(error => console.error('Error al eliminar el post:', error));
}

function clearForm() {
    document.getElementById('postTitle').value = '';
    document.getElementById('postArea').value = '';
    document.getElementById('postCategory').value = '';
    document.getElementById('postContent').value = '';
    document.getElementById('postImage').value = '';
}
