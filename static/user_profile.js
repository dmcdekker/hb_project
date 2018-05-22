"use strict";

// <--------------update social media info---------------->

function updateSocial(results){
  $('#twitter_id').html('Twitter:' + results[0]);
  $('#linkedin_id').html('Linkedin:' + results[1]);
  $('#website_url_id').html('Website:' + results[2]);
}

function getSocialData(evt) {
    evt.preventDefault(); 
    $('#social-div').hide(); 
    
    let formInputs = {
      'twitter': $('#twit-field').val(),
      'linkedin': $('#linkedin-field').val(),
      'website_url': $('#web-field').val()
    };  

    $.post('/edit-social.json', formInputs, updateSocial);
  }
  $('#social-div').on('submit', '#social-new', getSocialData);

function editSocial(e){ 
    e.preventDefault();
    $('#social-div').append('<form submit="/edit-social.json" id="social-new"><input type="text" name="linkedin" id="linkedin-field" placeholder="linkedin id"/><br><input type="text" name="twitter" id="twit-field" placeholder="twitter handle"/><br><input type="text" name="website_url" id="web-field" placeholder="website url"/><br><input type="submit" value="Submit"></form>');
  }
  $('#edit-social').one('click', editSocial);


// <--------------update or add education info----------------> 

function updateSchool(results){
  $('#school_name_id').html('School:' + results[0]);
  $('#year_id').html('Year graduated:' + results[1]);
  $('#school_city_id').html('City:' + results[2]);
  $('#school_state_id').html('State:' + results[3]);
  $('#major_id').html('Major:' + results[4]);
  $('#degree_level').html('Degree Levle:' + results[5]);
}

function getSchoolData(evt) {
    
    evt.preventDefault(); 
    $('#school-div').hide(); 
    
    let formInputs = {
      'school_name': $('#school-name-field').val(),
      'year': $('#year-field').val(),
      'school_city': $('#school-city-field').val(),
      'school_state': $('#school-state-field').val(),
      'major': $('#major-field').val(),
      'degree_level': $('#degree-level-field').val()
    };  

    $.post('/edit-education.json', formInputs, updateSchool);
  }
  $('#edit-education-div').on('submit', '#education-new', getSchoolData);

function editSchool(e){ 
    e.preventDefault();
    $('#edit-education-div').append('<form submit="/edit-education.json" id="education-new"><input type="text" name="school_name" id="school-name-field" placeholder="school name"/><br><input type="text" name="year" id="year-field" placeholder="year graduated"/><br><input type="text" name="school_city" id="school-city-field" placeholder="school city"/><br><input type="text" name="school_state" id="school-state-field" placeholder="school state"/><br><input type="text" name="major" id="major-field" placeholder="major"/><br><input type="text" name="degree_level" id="degree-level-field" placeholder="degree level"/><br><input type="submit" value="Submit"></form>');
  }
  $('#edit-education').one('click', editSchool); 


// <--------------update languages----------------> 

function updateLangs(results){
  console.log('test');
  $('#language_id').html(results);
}

function getLangData(evt) {
  evt.preventDefault(); 
  $('#languages-div').hide();

  let serialized_values = ($('#languages-new').serialize());
  console.log(serialized_values);
  let _str = serialized_values.split('&').join('').split('language_name=');
  console.log(_str);
 
  let formInputs = {
    'language_name': JSON.stringify(_str)
  };

  $.post('/edit-languages.json', formInputs, updateLangs);

}
$('#languages-div').on('submit', '#languages-new', getLangData);

$( "#languages-new" ).on( "submit", function( event ) {
    event.preventDefault();
    console.log($(this).serialize(), getLangData);
  });  

function showLanguage(e){ 
  e.preventDefault();
  $("#languages-div").show();
}
$('#edit-languages').on('click', showLanguage);

$(document).ready(function() {
  $("#languages-div").hide();
});



// <--------------update description----------------> 

function updateDescription(results){
  console.log('test3');
  $('#description_id').html(results);

}

function getDescriptionData(evt) {
  console.log('test2');
  evt.preventDefault(); 
  $('#description-div').hide(); 
    
  let formInputs = {
    'description': $('#description-field').val(),
  };  

  $.post('/edit-description.json', formInputs, updateDescription);
}
  $('#description-div').on('submit', '#description-new', getDescriptionData);

function editDescription(e){
  console.log('test1');
  e.preventDefault();
  $('#description-div').append('<form action="/edit-description.json" id="description-new"><input type="submit" value="submit"></form><br><textarea rows="4" cols="50" name="description" id="description-field" placeholder="Enter text here....." form="description-new"</textarea>');
}
$('#edit-description').one('click', editDescription); 





    