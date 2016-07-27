$(function (){

  $('#search_list').on('click', function(event) {
    searchMailingLists();
  });

  $('#list_name').on('input', function(event) {
    searchMailingLists();
  });
  
  function searchMailingLists(){
    var userName = $('#user_name').val();

    $.ajax({
      url: "/archives/"+ userName +"/subscriptions"+ location.search,
      type: 'post',
      data: { listname: $('#list_name').val(), user: '{{ user_.pk }}' },
      success: function(data){
        $("#subscription_lists").html(data);
      },
      beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
      }
    });
  }

  // Make sure to pass listname when page changes
  $(document).on('click', 'span.step-links a', function(){ this.href += '&list_name=' + $('#list_name').val();});
});
