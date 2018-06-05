"use strict";

// <--------------update social media info---------------->

function updateSocial(results){

  $('#twitter_id').html('Your twitter handle has been updated to: ' + results[0]);
  $('#linkedin_id').html('Your linkedIn id has been updated to: '  + results[1]);
  $('#website_url_id').html('Your website URL has been updated to: ' + results[2]);
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
    $('#social-div').append('<form submit="/edit-social.json" id="social-new"><input type="text" class="form-control" name="linkedin" id="linkedin-field" placeholder="linkedin id" style="width:15em"/><br><input type="text" class="form-control" name="twitter" id="twit-field" placeholder="twitter handle" style="width:15em"/><br><input type="text" name="website_url" class="form-control" id="web-field" placeholder="website url" style="width:15em"/><br><input type="submit" class="btn btn-primary" value="Submit"></form>');
  }
  $('#edit-social').one('click', editSocial);


// <--------------update or add education info----------------> 

function updateSchool(results){
  $('#school_name_id').html(results[0]);
  $('#year_id').html(results[1]);
  $('#school_city_id').html(results[2]);
  $('#school_state_id').html(results[3]);
  $('#major_id').html(results[4]);
  $('#degree_level').html(results[5]);
}

function getSchoolData(evt) {
    evt.preventDefault(); 
    $('#edit-education-div').hide(); 
    
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
    $('#edit-education-div').append('<form submit="/edit-education.json" id="education-new" style="width:15em"><input type="text" name="school_name" id="school-name-field" class="form-control" placeholder="school name" style="width:15em"/><br><input type="text" name="year" id="year-field" class="form-control" placeholder="year graduated" style="width:15em"/><br><input type="text" name="school_city" id="school-city-field" class="form-control" placeholder="school city" style="width:15em"/><br><input type="text" name="school_state" id="school-state-field" class="form-control" placeholder="school state" style="width:15em"/><br><input type="text" name="major" id="major-field" class="form-control" placeholder="major" style="width:15em"/><br><input type="text" name="degree_level" id="degree-level-field" class="form-control" placeholder="degree level" style="width:15em"/><br><input type="submit" id="cancel-education" class="btn btn-secondary d-line" value="Cancel"><input type="submit" class="btn btn-primary d-line" value="Save Changes"></form>');
  }
  $('#edit-education').one('click', editSchool); 
  

function closeEduDiv(e) {
  console.log('test');
  e.preventDefault();
  // alert();
  $('#edit-education-div').hide();
  $('#edu-og').show();
}
  $('body').on('click', '#cancel-education', closeEduDiv);


// <--------------update languages----------------> 

function updateLangs(results){
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
  $('#description_id').html(results);
}

function getDescriptionData(evt) {
  evt.preventDefault(); 
  $('#description-div').hide(); 
    
  let formInputs = {
    'description': $('#description-field').val(),
  };  
 
  $.post('/edit-description.json', formInputs, updateDescription);
}
  $('#description-div').on('submit', '#description-new', getDescriptionData);

function editDescription(e){
  e.preventDefault();
  $('#description-div').append('<form action="/edit-description.json" id="description-new"><input type-"text" name="description" id="description-field" class="form-control" style="width:100%" placeholder="Enter text here....." form="description-new"><input type="submit" class="btn btn-primary" value="submit"></form>');
}
$('#edit-description').one('click', editDescription); 


// <--------------update mentor/mentee----------------> 

function updateMentor(results){
}

$('input[name=mentor]').change(function(){
  let value = $(this).val();
  let formInputs = {
    'is_mentor' : value
  };
  $.post('/edit-is_mentor.json', formInputs, updateMentor);
});


// <--------------update active/not active----------------> 

function updateActive(results){
  console.log('test')
}

$('input[name=active]').change(function(){
  let value = $(this).val();
  let formInputs = {
    'is_active' : value
  };
  alert(value);
  $.post('/edit-is_active.json', formInputs, updateActive);
});

    