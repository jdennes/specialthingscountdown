var current_index = 0;
var special_things = [];

var getRandomInt = function(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
};

var refreshSpecialThings = function() {
  $.get("/things", function(data) {
    special_things = data;
    $("#specialthingsdata").html(JSON.stringify(special_things));
  }, "json");
};

var showMessage = function(message) {
  $("#message").html(message);
  $("#message").fadeIn("fast");
  setTimeout(function(){ $("#message").fadeOut("slow"); }, 2500);
};

var addSpecialThing = function() {
  if ($("#newthing").val().trim() == "") {
    showMessage("Your new special thing can't be empty!");
    return;
  }
  var new_thing = $("#newthing").val();
  $.post("/add", $("#addform").serialize(),
    function(data) {
      if (data.status) {
        $("#newthing").val("");
        refreshSpecialThings();
      }
      showMessage(data.message);
    });
};

$(document).ready(function() {
  special_things = JSON.parse($("#specialthingsdata").html());
  current_index = getRandomInt(0, special_things.length - 1);
  $("#specialthing").html(special_things[current_index]);
  $("div#next a").click(function() {
    if (current_index == special_things.length - 1) { 
      current_index = 0;
    } else {
      current_index += 1;
    }
    $("#specialthing").html(special_things[current_index]);
  });
  $("div#add a").click(function() { addSpecialThing(); });
});
