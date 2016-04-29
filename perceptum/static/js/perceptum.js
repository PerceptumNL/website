$(document).ready(function(){
  $('.slider').slider({full_width: true});
  $('.ajax-form').submit(function(event){
    var data = $(this).serialize();
    var url = $(this).attr('action');
    var form = this;
    $.post(url, data, function(result){
      $(form).replaceWith(result);
    });
    event.preventDefault();
  });
});

