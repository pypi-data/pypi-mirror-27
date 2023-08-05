function closeEdemSidebar() {
  $('.JS-openSidebar').removeClass('-active');
  $('body').removeClass('-sidebaropen');
}

function openEdemSidebar(option) {
  var contentSelector = '.JS-' + option + 'Content';
  var linkSelector = '.JS-openSidebar[data-sidebar-content="' + option + '"]';

  $('body').addClass('-sidebaropen');
  $('.JS-sidebarContent').removeClass('-show');
  $('.JS-openSidebar').removeClass('-active');
  $(linkSelector).addClass('-active');
  $(contentSelector).addClass('-show');
  resizeRecaptcha();
}

function resizeRecaptcha() {
  if (!$('.JS-signupContent').hasClass('JS-signupFinished')){ // Only run if signup is not completed
    var accessWidth = $('.JS-signUpForm')[0].getBoundingClientRect().width; // Get value with decimals
    var captchaWidth = 302;
    var captchaHeight = 78;
    var captchaDynamicHeight = $('.g-recaptcha')[0].getBoundingClientRect().height;
    var scaleRatio = accessWidth / captchaWidth;
    var scaleHeight = captchaHeight * scaleRatio;

    $('.g-recaptcha').css({
      'transform' : 'scale('+scaleRatio+')',
      '-webkit-transform' : 'scale('+scaleRatio+')',
      '-ms-transform' : 'scale('+scaleRatio+')',
      '-o-transform' : 'scale('+scaleRatio+')',
      'transform-origin' : '0 0',
      '-webkit-transform-origin' : '0 0',
      '-ms-transform-origin' : '0 0',
      '-o-transform-origin' : '0 0',
      'height' : scaleHeight
    });
  }
}

function showError(errorMessage) {
  $('.JS-accessErrorBox').removeAttr('hidden');
  $('.JS-accessError').text(errorMessage);
}

function showSuccessSignupMessage() {
// Replace signup content html with our success message.
  var userEmail = $('#mail').val();
  var successMessage = "Para ativar sua conta, siga as instruções enviadas para o email que você forneceu (<span class='highlight'>" + userEmail + "</span>).";
  var thanksElement = $('<p/>').addClass('success').text('Obrigado por se cadastrar!')
  var successElement = $('<p/>').addClass('success').html(successMessage);

  $('.JS-signupContent').addClass('JS-signupFinished').html(thanksElement).append(successElement);
}

// Resize reCAPTCHA on window resize
$(window).resize(function(){
  if ($('body').hasClass('-sidebaropen')) {
    resizeRecaptcha();
  }
});

// Create and append to body an overlay div for when the sidebar is opened
$('<div/>', {class: 'edem-overlay'}).appendTo('.edem-content-wrapper');

// Open sidebar via the topbar
$('.JS-openSidebar').click(function() {
  if ($(this).hasClass('-active')) {
    closeEdemSidebar();
  } else {
    openEdemSidebar($(this).data('sidebarContent'));
  }
});

// eDemocracia sidebar close button
$('.JS-closeSidebar').click(function(){
  closeEdemSidebar();
});

// Close sidebar if click on the overlay
$('.edem-overlay').click(function(){
  closeEdemSidebar();
});

// Toggle topbar items when on mobile
$('.JS-toggleTopbarMenu').click(function(){
  if ($(this).hasClass('-active')){
    $(this).removeClass('-active');
    $('.JS-topbarMenuHandler').removeClass('-menuopen');
  } else {
    $(this).addClass('-active');
    $('.JS-topbarMenuHandler').addClass('-menuopen');
  }
});

// Detect when input is filled
$('.JS-formInput').focus(function() {
  $(this).closest('.form-field').addClass('-filled');
});

$('.JS-formInput').blur(function() {
  if (!$(this).val() == '') {
    $(this).closest('.form-field').addClass('-filled');
  } else {
    $(this).closest('.form-field').removeClass('-filled');
  }
});

// Toggle country/state input
$('.JS-inputActionState').on('mousedown', function(e){
  e.preventDefault();
  $(this).closest('.form-field').attr('hidden','').removeClass('-filled');
  $(this).siblings('.JS-formInput').val('');
  $('.JS-inputActionCountry').closest('.form-field').removeAttr('hidden');
});

$('.JS-inputActionCountry').on('mousedown', function(e){
  e.preventDefault();
  $(this).closest('.form-field').attr('hidden','').removeClass('-filled');
  $(this).siblings('.JS-formInput').val('');
  $('.JS-inputActionState').closest('.form-field').removeAttr('hidden');
});

// Toggle show password
$('.JS-fieldActionPassword').on('mousedown', function(e){
  var input = $(this).siblings('.JS-formInput');
  e.preventDefault();
  if (input.attr('type') === 'text') {
    input.attr('type', 'password');
    $(this).text('Mostrar Senha');
  } else {
    input.attr('type', 'text');
    $(this).text('Esconder Senha');
  }
});

// Close error message
$('.JS-closeAccessError').click(function(){
  $('.JS-accessErrorBox').attr('hidden', '');
});

// Ajax calls for login and signup
$('.JS-loginForm').submit(function(event) {
  event.preventDefault();
  $.ajax({
    type:"POST",
    url: '/ajax/login/',
    data: $(event.target).serialize(),
    success: function(response){
      location.reload();
    },
    error: function(jqXRH){
      if (jqXRH.status == 0) {
        showError("Verifique sua conexão com a internet.")
      } else if (jqXRH.status == 401) {
        $('.JS-inputError').text('');
        $(event.target)
          .find('.JS-inputError')
          .text(jqXRH.responseJSON['data'])
          .removeAttr('hidden');
      } else {
        showError("Ocorreu um erro no servidor, tente novamente em alguns instantes.");
      }
    }
  });
});

$('.JS-signUpForm').submit(function(event) {
  event.preventDefault();
  if (grecaptcha.getResponse() == ""){
    showError("Por favor preencha o reCAPTCHA.");
  } else {
    $.ajax({
      type:"POST",
      url: '/ajax/signup/',
      data: $(event.target).serialize(),

      success: function(response){
        showSuccessSignupMessage();
      },

      error: function(jqXRH) {
        grecaptcha.reset();
        $("#g-recaptcha-response").val("");
        if (jqXRH.status == 0) {
          showError('Verifique sua conexão com a internet.');
        } else if (jqXRH.status == 400) {
          $('.JS-inputError').text('');
          $.each(jqXRH.responseJSON["data"], function(key, value) {
            if (key != '__all__') {
              $(event.target)
                .find('[data-input-name="'+key+'"]')
                .text(value)
                .removeAttr('hidden');
            } else {
              showError(value);
            }
          });
        } else if (jqXRH.status == 401) {
          showError(jqXRH.responseJSON["data"])
        } else {
          showError("Ocorreu um erro no servidor, tente novamente em alguns instantes.");
        }
      }
    });
  }
});

// XXX This should be exclusively on Audiencias Plugin whenever is possible
if (location.href.match(/audiencias/)) {
  $(document).on('click', 'a[href^="/home/?next="]', function(e){
    e.preventDefault();
    openEdemSidebar('signin');
  });
}
