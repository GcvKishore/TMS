//Load json -- Load json and store it in a global variable ==> exam_details (Chaitanya)
let JSONpaper = $.getJSON({
  url: "../framework/sampleData/sample_test.json",
  async: false,
});

JSONpaper = JSON.parse(JSONpaper.responseText);
// Global Variables
let current_section = 0;
let current_question = 0;
let start_time_stamp;
let end_time_stamp;
let current_question_details;
let current_question_type;
let user_inputs = [];

startExam();

// Start exam (Chaitanya)
function startExam() {
  // Starts the test once the function is invoked and calls the displayQuestion().
  displayQuestion();
}

//Display Questions (Amulya)
function displayQuestion() {
  // Summary: Used to display the current question in the respective section.
  // para: Using the current section and current question variables we called the functions to generate the questions for different formats.
  // return: None
  document.getElementById("question-text").innerHTML = "";
  document.getElementById("answer-input-options").innerHTML = "";

  let section = JSONpaper.sections[current_section];
  let question = section.questions[current_question];
  current_question_type = question.questionType;
  current_question_details = question.questionDetails;
  max_Time = question.maxTime;
  startCountDown(max_Time);
  document.getElementById("current-section").innerHTML = current_section + 1;
  document.getElementById("current-question").innerHTML = current_question + 1;
  document.getElementById("question-type-title").innerHTML =
    current_question_type;
  console.log(current_question_type);
  switch (current_question_type) {
    case "Multiple Choice - Multiple Answers":
      generateMCMA();
      break;
    case "Fill in the blanks":
      generateFITB();
      break;
    case "Short Answer":
      generateSA();
      break;
    case "File Submission":
      generateFU();
      break;
    default:
  }
}

// Start countdown (Priyusha)
function startCountDown(max_time) {
  // Summary:Used to  display the timer and clears the timer for next question 
  // para:Implemented timer
  // return:None
  var timing = max_time;
  var timer = setInterval(function () {
    if (timing <= 0.0) {
      clearInterval(timer);
      document.getElementById("next_button").click();
    } else {
      mins = Math.floor(timing / 60);
      secs = Math.floor(timing % 60);
      document.getElementById("countdown").innerHTML = `${mins}:${secs}`;
    }
    timing -= 1;
  }, 1000);
}

// Generate questions based on questionType
// Multiple Choice - Multiple Answers (Priyusha)
function generateMCMA() {
  // Summary:Generates multiplechoice questions  and answers
  // para:None
  // return:None
  let quesText = current_question_details.question;
  document.getElementById("question-text").innerHTML = quesText;
  let numOptions = current_question_details.options.length;
  let options = current_question_details.options;
  let input_tag="";
  for(var i=0;i<numOptions;i++){
      input_tag+= `<div class="form-check">
      <input class="form-check-input" type="checkbox" value="" id="defaultCheck${i}">
      <label class="form-check-label" for="defaultCheck${i}">${options[i]}</label>
  </div>`;
  }
  document.getElementById("answer-input-options").innerHTML = input_tag;
}

// Fill in the blanks (Vedavyas)
function generateFITB() {
  // Summary:
  // para:
  // return:
}

// Short Answer (Amulya)
function generateSA() {
  // Summary:
  // para:
  // return:
}

// File Submission (Chaitanya)
function generateFU() {
  // Summary:
  // para:
  // return:
}

// on next button click
// record user_inputs (Vedavyas)
function onNextClick() {
  // Summary:
  // para:
  // return:
}

// record user_inputs (Chaitanya)
function recordUserInputs() {
  // Summary:
  // para:
  // return:
}

// get user answers based on question type
// Multiple Choice - Multiple Answers (Priyusha)
function recordMCMA() {
  // Summary:
  // para:
  // return:
}

// Fill in the blanks (Vedavyas)
function recordFITB() {
  // Summary:
  // para:
  // return:
}

// Short Answer (Amulya)
function recordSA() {
  // Summary:
  // para:
  // return:
}

// File Submission (Chaitanya)
function recordFS() {
  // Summary:
  // para:
  // return:
}

// evaluate user Answers (Priyusha)
function evaluateUserAnswer(user_answers, actual_answers) {
  // Summary:
  // para:
  // return:
}

// Show exam overview and highlight current question (optional)
function examOverview() {
  // Summary:
  // para:
  // return:
}

// generate exam summary json file (Optional)
function createExamSummary() {
  // Summary:
  // para:
  // return:
}
