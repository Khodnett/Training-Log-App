$(document).ready(function() {


 //default
  $("#user").attr('required');
  $("#pass").attr('required');

  $("#newUser").removeAttr('required');
  $("#email").removeAttr('required');
  $("#pass1").removeAttr('required');
  $("#pass2").removeAttr('required');

  //Sign-up Form
  $("#tab-2").click(function() {
    $("#user").removeAttr('required');
    $("#pass").removeAttr('required');

    $("#newUser").attr('required');
    $("#email").attr('required');
    $("#pass1").attr('required');
    $("#pass2").attr('required');
  });
//Login Form
  $("#tab-1").click(function() {
    $("#user").attr('required');
    $("#pass").attr('required');

    $("#newUser").removeAttr('required');
    $("#email").removeAttr('required');
    $("#pass1").removeAttr('required');
    $("#pass2").removeAttr('required');
  });




});
