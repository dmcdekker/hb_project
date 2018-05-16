"use strict";

function getData(evt) {
    evt.preventDefault(); 
    console.log('test2');
    
    let formInputs = {
      'twitter': $('#twit-field').val()
    };  

    console.log(formInputs)

    $.post('/edit-profile.json', formInputs)
  }

  
  $('#twitter-div').on('submit', '#twitter-new', getData);

  function addElements(e){ 
    console.log('test1')
    e.preventDefault();
    console.log('test');    
    $('#twitter-div').append('<form submit="/edit-profile.json" id="twitter-new"><input type="text" name="twitter" id="twit-field"/><br><input type="submit" value="Submit"></form>');  
    // $('#linkedin').append('<form><input type="text" name="linkedin" id="linked-field"/><br><input type="submit" value="Submit"></form>');   
    // $('#website_url').append('<form><input type="text" name="website_url" id="site-field"/><br><input type="submit" value="Submit"></form>');   
    // $('#email').append('<form><input type="text" name="email" id="email-field"/><br><input type="submit" value="Submit"></form>');
    
  }

  $('#edit-profile').one('click', addElements);