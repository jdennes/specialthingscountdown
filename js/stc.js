var current_index = 0;
var special_things = [];

var getRandomInt = function(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
};

var refreshSpecialThings = function() {
  $.get("/things", function(data) {
    special_things = data;
    $("#specialthingsdata").html(JSON.stringify(special_things));
    current_index = 0;
    $("#specialthing").html(special_things[current_index].thing);
    $("#specialthingadded").html(special_things[current_index].added);
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

var forward = function() {
  if (current_index == special_things.length - 1) { 
    current_index = 0;
  } else {
    current_index += 1;
  }
  if (special_things.length > 0) {
    $("#specialthing").html(special_things[current_index].thing);
    $("#specialthingadded").html(special_things[current_index].added);
  }
};

var back = function() {
  if (current_index == 0) { 
    current_index = special_things.length - 1;
  } else {
    current_index -= 1;
  }
  if (special_things.length > 0) {
    $("#specialthing").html(special_things[current_index].thing);
    $("#specialthingadded").html(special_things[current_index].added);
  }
};

$(document).ready(function() {
  special_things = JSON.parse($("#specialthingsdata").html());
  current_index = 0;
  if (special_things.length > 0) {
    $("#specialthing").html(special_things[current_index].thing);
    $("#specialthingadded").html(special_things[current_index].added);
  }
  $("div#forward a").click(function() { forward(); });
  $("div#back a").click(function() { back(); });
  $("div#add a").click(function() { addSpecialThing(); });
});
