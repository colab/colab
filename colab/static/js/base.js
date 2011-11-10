
function vote_callback(msg_id, step) {
    return function() {
        jQuery('#msg-' + msg_id + ' .plus span').text(function(self, count) {
            return parseInt(count) + step;
        });
        jQuery('#msg-' + msg_id + ' .minus').toggleClass('hide');
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
        console.debug(msg_id);
        jQuery('.plus img', this).bind('click', function() {
            vote(msg_id);
        });
        jQuery('.minus a', this).bind('click', function() {
            unvote(msg_id);
            return false;
        });
    });
});