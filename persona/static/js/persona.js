
// scope the first section - IIFE FTW!!
(function () {

  var root = this;

  if ( typeof persona === 'undefined' ) {
    var persona = root.persona = {};
    persona.currentUser = null;
  } 

  // TODO: figure out where this should live
  // hide the logout UI until we know we're logged in
  $('#logout_link').hide();

  // Called when the Persona API logs a user in (hooked up in .watch())
  persona.onlogin = function p_onlogin(assertion) {
    // A user has logged in! Here you need to:
    // 1. Send the assertion to your backend for verification and to create a session.
    // 2. Update your UI.
    $.ajax({
      type: 'POST',
      url: '/auth/login', // any url to handle login
      data: {assertion: assertion},
      success: function(res, status, xhr) {
        console.log('LOGIN SUCCESS');
        // TODO: when we start getting the full user JSON, set this correctly
        persona.currentUser = res;
        $('#login_link').hide();
        $('#logout_link').show();
      },
      error: function(xhr, status, err) {
        navigator.id.logout();
        console.log('LOGIN FAILED: ' + err);
        $('#login_link').show();
        $('#logout_link').hide();
        persona.currentUser = null;
      }
    });
  };

  // Called when the Persona API logs a user out (hooked up in .watch())
  persona.onlogout = function p_onlogout(assertion) {
    // A user has logged out! Here you need to:
    // Tear down the user's session by redirecting the user or making a call to your backend.
    // Also, make sure loggedInUser will get set to null on the next page load.
    // (That's a literal JavaScript null. Not false, 0, or undefined. null.)
    $.ajax({
      type: 'POST',
      url: '/auth/logout',                    // any url to handle logout
      success: function(res, status, xhr) {   // if user gets logged out of backend
        console.log('LOGOUT SUCCESS');
        $('#login_link').show();
        $('#logout_link').hide();
        persona.currentUser = null;
      },
      error: function(xhr, status, err) {     // user not logged out succesfully!! yikes!
        console.log('LOGOUT FAILED: ' + err); // arguably this should still offer login UI
        $('#login_link').hide();
        $('#logout_link').show();
      }
    });
  };

  // Setup the initial persona login watching - will trigger login if user is logged in
  // via cookie
  navigator.id.watch({
    loggedInUser: persona.currentUser,
    onlogin: persona.onlogin,
    onlogout: persona.onlogout
  });
}()); // end of scope for the first section


// Hook up the click listeners for the login/logout
// Scope and call this code right away
(function () {
  // Setup click listeners for the login/logout links
  var signinLink = document.getElementById('login_link');
  if (signinLink) {
    signinLink.onclick = function() {
      navigator.id.request();
    };
  }
 
  var signoutLink = document.getElementById('logout_link');
  if (signoutLink) {
    signoutLink.onclick = function() {
      navigator.id.logout();
    };
  }
}());
