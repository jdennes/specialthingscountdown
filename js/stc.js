var current_index = 0;
var special_things = [];

var getRandomInt = function(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
};

var refreshSpecialThings = function(day_id) {
  $.get("/day/" + day_id + "/things", function(data) {
    special_things = data;
    $("#specialthingsdata").html(JSON.stringify(special_things));
    current_index = 0;
    if (special_things.length > 0) {
      $("#specialthing").html(special_things[current_index].thing);
      $("#specialthingadded").html(special_things[current_index].added);
    } else {
      $("#nospecialthings").show();
    }
  }, "json");
};

var showMessage = function(message) {
  $("#message").html(message);
  $("#message").fadeIn("fast");
  setTimeout(function(){ $("#message").fadeOut("slow"); }, 2500);
};

var addSpecialDay = function() {
  if ($("#specialdaydescription").val().trim() == "") {
    showMessage("You have to enter a description!");
    return;
  }
  if ($("#specialdayactualdate").val().trim() == "") {
    showMessage("You have to enter a valid date!");
    return;
  }
  $.post("/day/add", $("#addspecialdayform").serialize(),
    function(data) {
      if (data.status) {
        $("#specialdaydescription").val("");
        $("#specialdayactualdate").val("");
        $("#specialdaydate").val("");
        window.location.replace("/");
      } else {
        showMessage(data.message);
      }
    });
};

var addSpecialThing = function() {
  if ($("#newthing").val().trim() == "") {
    showMessage("Your new special thing can't be empty!");
    return;
  }
  var day_id = $("#specialdayid").val();
  var new_thing = $("#newthing").val();
  $.post("/day/" + day_id + "/add", $("#addform").serialize(),
    function(data) {
      if (data.status) {
        $("#newthing").val("");
        refreshSpecialThings(day_id);
        if ($("#listview").is(":visible")) {
          toggleView();
        }
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

var populateListView = function() {
  html = [];
  $.each(special_things, function(i, item) {
    html.push("<div>");
    html.push("<div class=\"special\">" + special_things[i].thing + "</div>");
    html.push("<div class=\"specialadded pink\">" + special_things[i].added + "</div>");
    html.push("</div>");
  });
  $("#listview").html(html.join(''));
};

var toggleView = function() {
  if (special_things.length == 0) {
    $("#normalview").show();
    $("#viewtoggle a").html("Show full list");
    $("#nospecialthings").show();
    return;
  }
  if ($("#normalview").is(":visible")) {
    // Display list view
    $("#normalview").hide();
    populateListView();
    $("#listview").show();
    $("#viewtoggle a").html("Hide full list");
  } else {
    // Display normal view
    $("#listview").hide();
    $("#normalview").show();
    $("#viewtoggle a").html("Show full list");
  }
};
