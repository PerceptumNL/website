$(document).ready(function(){
  $('.slider').slider({full_width: true});
  $('.ajax-form-snippet').each(function(){
    var loadingContent = $(this).html();
    var url = $(this).attr('data-url');
    var container = this;
    var onSubmitFn = function(event){
      var data = $(this).serialize();
      var url = $(this).attr('action');
      var form = this;
      $.post(url, data, function(result, textStatus, jqXHR){
        $(container).html(result);
        $(container).find('form').submit(onSubmitFn);
      });
      $(container).html(loadingContent);
      event.preventDefault();
    }
    $.get(url, function(result){
      $(container).html(result);
      $(container).find('form').submit(onSubmitFn);
    });
  });
});
