function pagehit(path_info) {
    jQuery.ajax({
        url: '/api/hit/',
        type: 'POST',
        data: {'path_info': path_info},
    });
}
