$(document).ready(function(){
  $('.slider').slider({full_width: true});
  $('.ajax-form').submit(function(event){
    var data = $(this).serialize();
    var url = $(this).attr('action');
    var form = this;
    $.post(url, data, function(result, textStatus, jqXHR){
      if(jqXHR.getResponseHeader('X-Form-Status') === "valid"){
        $(form).replaceWith(result);
      }else{
        $(form).find('.ajax-form-snippet').first().html(result);
      }
    });
    event.preventDefault();
  });
  $('.ajax-form-snippet').each(function(){
    var url = $(this).attr('data-url');
    var container = this;
    $.get(url, function(result){
      $(container).html(result);
    });
  });
});

