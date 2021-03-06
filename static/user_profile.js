"use strict";

// <--------------update social media info---------------->

function closeSocialDiv(e) {
  e.preventDefault();
  $('#social-div').hide();
}
  $('body').on('click', '#cancel-social', closeSocialDiv);

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
  $('#social-div').one('submit', '#social-new', getSocialData);

function editSocial(e){ 
    e.preventDefault();
    $('#social-div').show();
  }
  $('#edit-social').on('click', editSocial);


$(document).ready(function() {
    $("#social-div").hide();
  });  


// <--------------update or add education info----------------> 

function closeEduDiv(e) {
  e.preventDefault();
  $('#edit-education-div').hide();
  $('#edu-og').show();
}
  $('body').on('click', '#cancel-education', closeEduDiv);

function updateSchool(results){
  $('#school_name_id').html(results[0] + ', ');
  $('#year_id').html(results[1]);
  $('#school_city_id').html(results[2] + ', ');
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

function editSchool(ev){ 
    ev.preventDefault();
    $('#edit-education-div').show();
  }
  $('#edit-education').one('click', editSchool); 

  $(document).ready(function() {
    $("#edit-education-div").hide();
  });    



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

function closeDescriptionDiv(e) {
  console.log('test3');
  e.preventDefault();
  $('#description-div').hide();
  $('#description_id').show();
}
  $('body').on('click', '#cancel-description', closeDescriptionDiv); 

function updateDescription(results){
  console.log('test2');
  $('#description_id').html(results);
}

function getDescriptionData(evt) {
  console.log('test1');
  evt.preventDefault(); 
  $('#description-div').hide(); 
    
  let formInputs = {
    'description': $('#description-field').val(),
  };  
 
  $.post('/edit-description.json', formInputs, updateDescription);
}
  $('body').on('submit', '#description-new', getDescriptionData);

function editDescription(e){
  e.preventDefault();
  $('#description-div').show();
}
$('#edit-description').on('click', editDescription); 

$(document).ready(function() {
  $("#description-div").hide();
});

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

    