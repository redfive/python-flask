
// scope the first section - IIFE FTW!!
(function () {

  var root = this;

  if ( typeof porkins === 'undefined' ) {
    var porkins = root.porkins = {};
    porkins.currentUser = null;
  } 

  // TODO: figure out where this should live
  // hide the logout UI until we know we're logged in
  $('#logout_link').hide();
  $('#unlink_dropbox').hide();

  // Called when the Persona API logs a user in (hooked up in .watch())
  porkins.onlogin = function p_onlogin(assertion) {
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
        porkins.currentUser = res;
        //porkins.dropboxLogin();
        // instead attempt to fetch the dropbox content and
        // if that fails show the link dropbox link
        console.log('currentUser is: ' + porkins.currentUser);
        $('#greeting').text("Hello " + porkins.currentUser);
        $('#login_link').hide();
        $('#logout_link').show();
      },
      error: function(xhr, status, err) {
        navigator.id.logout();
        console.log('LOGIN FAILED: ' + err);
        $('#greeting').text("Hello Stranger");
        $('#login_link').show();
        $('#logout_link').hide();
        porkins.currentUser = null;
      }
    });
  };

  // Called when the Persona API logs a user out (hooked up in .watch())
  porkins.onlogout = function p_onlogout(assertion) {
    // A user has logged out! Here you need to:
    // Tear down the user's session by redirecting the user or making a call to your backend.
    // Also, make sure loggedInUser will get set to null on the next page load.
    // (That's a literal JavaScript null. Not false, 0, or undefined. null.)
    $.ajax({
      type: 'POST',
      url: '/auth/logout',                    // any url to handle logout
      success: function(res, status, xhr) {   // if user gets logged out of backend
        console.log('LOGOUT SUCCESS');
        $('#greeting').text("Hello Stranger");
        $('#login_link').show();
        $('#logout_link').hide();
        porkins.currentUser = null;
      },
      error: function(xhr, status, err) {     // user not logged out succesfully!! yikes!
        console.log('LOGOUT FAILED: ' + err); // arguably this should still offer login UI
        $('#greeting').text("Hello Stranger");
        $('#login_link').hide();
        $('#logout_link').show();
      }
    });
  };
/*
  porkins.dropboxLogin = function p_dropboxLogin() {
    $.ajax({
      type: 'POST',
      url: '/auth/dropbox', 
      success: function(res, status, xhr) {
        console.log('DROPBOX SUCCESS');
        console.log(res)
        console.log('currentUser is: ' + porkins.currentUser);
      },
      error: function(xhr, status, err) {
        console.log('DROPBOX FAILED: ' + err);
      }
    });
  };
*/

  /**
   *  path should begin with a /
   **/
  porkins.getDropboxFolder = function p_getDropboxFolder(path) {
    // TODO: find a better check/pattern here
    // path = (typeof path === 'undefined') ? "" : path;
    path = path ? path : "";
    $.ajax({
      type: 'GET',
      url: '/content/dropbox' + path , 
      success: function(res, status, xhr) {
        console.log('DROPBOX FETCH SUCCESS');
        console.log(res)
      },
      error: function(xhr, status, err) {
        console.log('DROPBOX FETCH FAILED: ' + err);
      }
    });
  };

  porkins.doLinkDropbox = function p_doLinkDropbox() {
    $.get('/auth/dropbox').done( function (res, status, xhr) {
      console.log('** DROPBOX AUTH SUCCESS: ' + res)
    }).fail( function (xhr, status, err) {
      console.log('** DROPBOX AUTH ERROR: ' + err)
    });
  };

  // Setup the initial persona login watching - will trigger login if user is logged in
  // via cookie
  navigator.id.watch({
    loggedInUser: porkins.currentUser,
    onlogin: porkins.onlogin,
    onlogout: porkins.onlogout
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
  var dropbox_login = $('#link_dropbox');
  if (dropbox_login) {
    dropbox_login.click( function() {
      porkins.doLinkDropbox();
    });
  }
/*
  var login = $('#login');
  if (login) {
    login.onclick = function() {
      navigator.id.request();
    }
  }
*/
  //var greetingEl = document.getElementById('greeting');
  //greetingEl.innerHTML = "hello world";
}());















