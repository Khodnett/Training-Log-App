
$(document).ready(function() {

$(".collapse").on("hidden.bs.collapse", function() {
  sessionStorage.setItem("coll_" + this.id, false);

  if ($("#colBtn"+this.id.slice(-11)).hasClass('minus')){
    $("#colBtn"+this.id.slice(-11)).removeClass('minus');
  }

  $("#colBtn"+this.id.slice(-11)).addClass('plus');
});

$(".collapse").on("shown.bs.collapse", function() {

  sessionStorage.setItem("coll_" + this.id, true);

  if ($("#colBtn"+this.id.slice(-11)).hasClass('plus')){
    $("#colBtn"+this.id.slice(-11)).removeClass('plus');
  }

$("#colBtn"+this.id.slice(-11)).addClass('minus');

});

$(".collapse").each(function() {

  if (sessionStorage.getItem("coll_" + this.id) == "false") {
    $(this).collapse("hide");
    $("#colBtn"+this.id.slice(-11)).addClass('plus');
  }
  else{
    $(this).collapse("show");

      $("#colBtn"+this.id.slice(-11)).addClass('minus');

  }
});

//$("#editform *").hide();
//document.getElementById('editform').style.visibility='hidden';
$("#editNote").click(function(){
  if ($("#editform").css("display","none")){
    $("#editform").css("display","block")
    $(".note").css("display","none")
  }else{
    $("#editform").css("display","none")
  }
});

$("#cancelNote").click(function(){
  if ($("#editform").css("display","block")){
    $("#editform").css("display","none")
    $(".note").css("display","block")
  }
});

});
