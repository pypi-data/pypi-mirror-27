<script>
  $('.category-list__button')
    .click(function() {
      var element = $(this);
      var input = $('.input--filter');
      var inputFilter = null;
      if (element.hasClass('active')) {
        element.removeClass('active');
        inputFilter = input.val().split(',');
        inputFilter.pop($(this).attr('slug'));
      } else {
        element.addClass('active');
        inputFilter = input.val().split(',');
        inputFilter.push($(this).attr('slug'));
      }
      input.val(inputFilter.join(','));
  });
</script>