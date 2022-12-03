
$(document).ready(function() {


  $("li .side").each(function(){
             if (window.location.pathname.includes($(this).attr("href"))){
                     $(this).addClass("active");
             }
     });

    if (window.location.href.includes('signup')){

             $("#user").removeAttr('required');
             $("#pass").removeAttr('required');

             $("#user").val('');
             $("#pass").val('');

             $("#newUser").attr('required');
             $("#email").attr('required');
             $("#pass1").attr('required');
             $("#pass2").attr('required');

    }
    else{

      //default
       $("#user").attr('required');
       $("#pass").attr('required');

       $("#newUser").removeAttr('required');
       $("#email").removeAttr('required');
       $("#pass1").removeAttr('required');
       $("#pass2").removeAttr('required');


    }



  //Sign-up Form
  $("#tab-2").click(function() {

    $("#newUser").prop('required',true);
    $("#email").prop('required',true);
    $("#pass1").prop('required',true);
    $("#pass2").prop('required',true);

    $("#user").removeAttr('required');
    $("#pass").removeAttr('required');

    $("#user").val('');
    $("#pass").val('');


  });
//Login Form
  $("#tab-1").click(function() {

    $("#user").prop('required',true);
    $("#pass").prop('required',true);

    $("#newUser").removeAttr('required');
    $("#email").removeAttr('required');
    $("#pass1").removeAttr('required');
    $("#pass2").removeAttr('required');
  });



});
