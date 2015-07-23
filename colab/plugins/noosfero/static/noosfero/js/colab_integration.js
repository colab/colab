
window.onload=transform_tag_Welcome();

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
}


function  transform_tag_Welcome()
{
   var tag = document.getElementsByClassName('foswikiToc');
   var text = httpGet('http://localhost:8000/spb/get_list/?list_name=ListB&MAX=5');
   tag[0].innerHTML= text;

   var current = url = window.location.href 
}
