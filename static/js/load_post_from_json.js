function onLoad(post_id) {
    fetch('http://127.0.0.1:5000/api/post/' + post_id)
        .then((res) => res.json())
        .then((data) => {
            if (Object.keys(data).length === 0) {
                document.getElementById('api-title').innerHTML = "Post not found - 404"
            } else {
                document.getElementById('api-title').innerHTML = data.title

                document.getElementById('api-author-link').setAttribute("href", "http://127.0.0.1:5000" + "/users/" + data.owner)
                document.getElementById('api-post-owner-name').innerHTML = data.display_name
                document.getElementById('api-created').innerHTML = "Written on: " + data.date_created
                document.getElementById('api-modified').innerHTML = "Last edited on: " + data.date_modified
                document.getElementById('api-post-text').innerHTML = data.text

                var del = document.getElementById("api-delete");
                var edit = document.getElementById("api-edit");

                if (data.active_user == data.owner || data.active_user == 'admin') {
                    del.style.display = "block";
                    del.setAttribute("href", "http://127.0.0.1:5000/" + data.post_id + "/delete")

                    edit.style.display = "block";
                    edit.setAttribute("href", "http://127.0.0.1:5000/" + data.post_id + "/update")
                } else {
                    del.style.display = "none";
                    edit.style.display = "none";
                }
            }
        })
        .catch((error) => console.log(error))
}
