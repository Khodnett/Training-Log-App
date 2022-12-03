$(document).ready(function() {
  alert('shown onload');
$('#collapsewithlink').on('hidden.bs.collapse', function (e) {
  alert('hidden on #' + this.id);
});

$('#collapsewithlink').on('shown.bs.collapse', function (e) {
  alert('shown on #' + this.id);
});

});
