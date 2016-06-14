$(function (){

  ENTER_BUTTON = 13;
  searchMaillingLists();

  $('#search_list').on('click', function(event) {
    searchMaillingLists();
  });

  $('#list_name').on('keypress', function(event) {
    if (event.which == ENTER_BUTTON) {
      event.preventDefault();
    }
    $('#search_list').trigger('click');
  });
  
  function searchMaillingLists(){
    var userName = $('#user_name').val();
    $.ajax({
      url: "/archives/"+userName+"/subscriptions",
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
  
});