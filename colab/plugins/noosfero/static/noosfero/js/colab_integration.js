
window.onload=transform_tags();

function  transform_tags()
{
       var tag = $('.software-community-dashboard');  
       var url = $(location).attr('pathname'); 
       var regex = new RegExp(/\/social\/(.+)\//g);
       var community = regex.exec(url)[1];
       var MAX = '7'
       var request_path = '/spb/get_list/'+'?list_name='+community+'&'+'MAX='+MAX;

       tag.load(request_path)
}
