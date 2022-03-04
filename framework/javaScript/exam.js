//Load json -- Load json and store it in a global variable ==> exam_details (Chaitanya)
let JSONpaper = $.getJSON({
  url: "../sampleData/sample_test.json",
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
let timer;

startExam();

// Start exam (Chaitanya)
function startExam() {
  // Starts the test once the function is invoked and calls the displayQuestion().
  displayQuestion();
}

//Display Questions (Amulya)
function displayQuestion() {
  // Summary: Used to display the current question in the respective section.
  // para: None
  // return: None
  document.getElementById("question-text").innerHTML = "";
  document.getElementById("answer-input-options").innerHTML = "";

  let section = JSONpaper.sections[current_section];
  let question = section.questions[current_question];
  current_question_type = question.questionType;
  current_question_details = question.questionDetails;
  max_Time = question.maxTime;
  let currrent_question_class = `sec-${current_section + 1}-que-${
    current_question + 1
  }`;
  document.getElementById(currrent_question_class).style.color = "#FABC75";
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
  timer = setInterval(function () {
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
  let input_tag = "";
  for (var i = 0; i < numOptions; i++) {
    input_tag += `<div class="form-check">
      <input class="form-check-input" type="checkbox" value="" id="defaultCheck${i}">
      <label class="form-check-label" for="defaultCheck${i}">${options[i]}</label>
  </div>`;
  }
  document.getElementById("answer-input-options").innerHTML = input_tag;
}

// Fill in the blanks (Vedavyas)
function generateFITB() {
  // Summary: Generate fill in the blanks HT
  // para: None
  // return: None

  // 1.0 create question text
  let question_text = current_question_details.questionText;

  // 2.0 create blanks in question_text
  let blanks = current_question_details.answers;
  for (const i in blanks) {
    let HTML_tag = `<span><input class="FIB" id=fITB-option-${i} spellcheck="false" maxlength="28" style="width: 10vw;"></span>`;
    question_text = question_text.replace(blanks[i], HTML_tag);
  }
  document.getElementById("question-text").innerHTML = question_text;
}

// Short Answer (Amulya)
function generateSA() {
  // Summary: In this we have generated the current question and answer area.
  // para: None
  // return: None
  let quesText = current_question_details.questionText;
  document.getElementById("question-text").innerHTML = quesText;
  let maxchars = current_question_details.MaxWords * 6;
  input_tag = `<div class="mb-3">
    <textarea class="form-control"
    id="exampleFormControlTextarea1"
    rows="6"
    maxlength="${maxchars}">Type your answer here</textarea>
  </div> `;
  document.getElementById("answer-input-options").innerHTML = input_tag;
}

// File Submission (Chaitanya)
function generateFU() {
  //  Represents the code for uploading a file
  let quesText = questionDetails.questionText;
  document.getElementById("ques").innerHTML = quesText;
  input_tag = `<div class="row upload_box align-items-center"> <div class="col text-center"><input type="file" id="myfile" name="myfile"></div></div> `;
  document.getElementById("answer").innerHTML = input_tag;
}

// on next button click
// record user_inputs (Vedavyas)
function onNextClick() {
  // Summary: up on user clicking next button or up on time out. This functions
  //          saves the user inputs and displays next question if available.
  // para: None
  // return: None

  // 1.0 Reset current_question color and countdown
  let currrent_question_class = `sec-${current_section + 1}-que-${
    current_question + 1
  }`;
  document.getElementById(currrent_question_class).style.color = "#FBF8F2";
  clearInterval(timer);

  // 2.0 record user inputs in JSON format
  recordUserInputs();

  // 3.0 get current section and questions details
  num_questions = JSONpaper.sections[current_section].questions.length;
  num_sections = JSONpaper.sections.length;
  current_question = current_question + 1;

  // 4.0 Check if they are more questions in the section
  if (current_question >= num_questions) {
    current_question = 0;
    current_section++;
  }

  // 5.0 Check if they are more sections in the exam paper
  if (current_section >= num_sections) {
    // 5.1 Save user inputes in a JSON File
    createExamSummary();
    location.href = "../framework/test_summary.html";
  } else {
    // 5.2 if more questions available then display next question
    displayQuestion();
  }
}

// record user_inputs (Chaitanya)
function recordUserInputs(){
    // Summary:
    // para:
    // return:

}

// get user answers based on question type
// Multiple Choice - Multiple Answers (Priyusha)
function recordMCMA() {
  // Summary:Records all the answers of multiple choice entered by  the user
  // para:None
  // return:None
  let checkbox=document.querySelectorAll("input[type=checkbox]:checked");
  let checked_options=[];
  try{
    for(const i in checkbox){
      check_box_value=checkbox[i].value;
      if(typeof(check_box_value)!="undefined"){
        checked_options.push(check_box_value);
      }
    }
  } finally {
    return checked_options;
  }
}

// Fill in the blanks (Vedavyas)
function recordFITB() {
  // Summary: records all the ansers entered by the user
  // para: None
  // return: None

  // 1.0 Get all the fill in the blanks input elements
  let user_inputs = document.querySelectorAll(".FIB");
  let answers = [];

  // 2.0 Save the user inputs into an Array/List
  try {
    for (const i in user_inputs) {
      user_input = user_inputs[i].value;
      if (typeof user_input != "undefined") {
        answers.push(user_input);
      }
    }
  } finally {
    // 3.0 finally retuen the user inputs which contains string elements
    return answers;
  }
}

// Short Answer (Amulya)
function recordSA() {
  // Summary: records all the short answers entered by the user.
  // para: None
  // return: None
  let answer = "";
  try {
    var SA_input = document.getElementById("exampleFormControlTextarea1").value;
    answer = SA_input;
  } finally {
    return answer;
  }
}

// File Submission (Chaitanya)
function recordFS() {
  // Summary:
  // para:
  // return:
}

// evaluate user Answers (Priyusha)
function evaluateUserAnswer(user_answers, actual_answers) {
  // Summary:Evaluates the user answers
  // para:User entered answers and actual answers
  // return:Answer is correct or wrong
  for(const i in actual_answers) {
    if(actual_answers[i]!==user_answers[i]){
      return ("Wrong Answer");
    }
  }
  return("Correct Answer");
}

// Show exam overview and highlight current question (Vedavyas)
function examOverview() {
  // Summary: displays exam overview
  // para: None
  // return: None

  // 1.0 Get no of sections and no of rows
  let num_sections = JSONpaper.sections.length;

  // 2.0 generate exam overview html tags
  let sections_overview = "";
  for (let i = 1; i <= num_sections; i++) {
    let num_questions = JSONpaper.sections[i - 1].questions.length;
    let questions_html_tags = "";
    for (let j = 1; j <= num_questions; j++) {
      questions_html_tags += `<li class="py-1" id="sec-${i}-que-${j}">Question ${j}</li>`;
    }
    let questions_overview = `<ul class="px-1">${questions_html_tags}</ul>`;
    sections_overview += `<li class="py-2"><span id="sec-${i}">Section ${i}</span>${questions_overview}</li>`;
  }
  let overview_html_tag = `<ol>${sections_overview}</ol>`;

  // 3.0 Display exam overview
  document.getElementById("exam-overview").innerHTML = overview_html_tag;
}

// generate exam summary json file (Optional)
function createExamSummary() {
  // Summary:
  // para:
  // return:
}
