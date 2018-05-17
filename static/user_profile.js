"use strict";

function updateSocial(results){
  $('#twitter_id').html('Twitter:' + results[0])
  $('#linkedin_id').html('Linkedin:' + results[1])
  $('#website_url_id').html('Website:' + results[2])
}

function getData(evt) {
    evt.preventDefault(); 
    $('#social-div').hide(); 
    
    let formInputs = {
      'twitter': $('#twit-field').val(),
      'linkedin': $('#linkedin-field').val(),
      'website_url': $('#web-field').val()
    };  

    $.post('/edit-profile.json', formInputs, updateSocial)
  }
  $('#social-div').on('submit', '#social-new', getData);

  
function addElement(e){ 
    e.preventDefault();
    $('#social-div').append('<form submit="/edit-profile.json" id="social-new"><input type="text" name="linkedin" id="linkedin-field" placeholder="linkedin id"/><br><input type="text" name="twitter" id="twit-field" placeholder="twitter handle"/><br><input type="text" name="website_url" id="web-field" placeholder="website url"/><br><input type="submit" value="Submit"></form>');
  }
  $('#edit-social').one('click', addElement);


 