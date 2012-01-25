
function vote_callback(msg_id, step) {
    return function() {
        jQuery('#msg-' + msg_id + ' .plus span').text(function(self, count) {
            return parseInt(count) + step;
        });
        jQuery('#msg-' + msg_id + ' .minus').toggleClass('hide');
        jQuery('#vote-notification').addClass('hide');
    }
}

function get_vote_ajax_dict(msg_id, type_) {
    if (type_ === 'DELETE') {
        step = -1;
    } else if (type_ === 'POST') {
        step = 1;
    } else {
        return {};
    }
    
    return {
        url: "/api/message/" + msg_id + "/vote",
        type: type_,
        success: vote_callback(msg_id, step),
        error: function (jqXHR, textStatus, errorThrown) {
            
            error_msg = '<b>Seu voto não foi computado.</b>'
            if (jqXHR.status === 401) {
                error_msg += ' Você deve estar autenticado para votar.';
            } else {
                error_msg += ' Erro desconhecido ao tentando votar.';
            }
            
            jQuery('#vote-notification').html(error_msg).removeClass('hide');
            scroll(0, 0);
        }
    }
}

function vote(msg_id) {
    jQuery.ajax(get_vote_ajax_dict(msg_id, 'POST'));
}

function unvote(msg_id) {
    jQuery.ajax(get_vote_ajax_dict(msg_id, 'DELETE'));
}

jQuery(document).ready(function() {
    jQuery('.email_message').each(function() {
        var msg_id = this.getAttribute('id').split('-')[1];
        jQuery('.plus img', this).bind('click', function() {
            vote(msg_id);
        });
        jQuery('.minus a', this).bind('click', function() {
            unvote(msg_id);
            return false;
        });
    });
});

function pagehit(path_info) {
    jQuery.ajax({
        url: '/api/hit/',
        type: 'POST',
        data: {'path_info': path_info},
    });
}
