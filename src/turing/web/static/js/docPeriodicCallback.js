function t_doc_callback() {
    $.ajax({
        url: '/callback',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(dict),
        success: function (response) {
            console.log(response)
        }
    });
}

setInterval(t_doc_callback, 100)