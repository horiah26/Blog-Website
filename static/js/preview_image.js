img.onchange = evt => {
    const [file] = img.files
    if (file) {
        preview.src = URL.createObjectURL(file)
    }
}