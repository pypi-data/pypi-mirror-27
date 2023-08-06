function validateFileSize(input, maxSize, message) {
    message = message || "File size ({size}) exceeds limit ({limit})"
    if (input.files[0].size > maxSize) {
        alert(message.replace('{size}', input.files[0].size).replace('{limit}', maxSize));
        input.value = '';
    }
}