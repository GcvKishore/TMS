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
  // Summary:
  // para:
  // return:
}

// Generate questions based on questionType
// Multiple Choice - Multiple Answers (Priyusha)
function generateMCMA() {
  // Summary:
  // para:
  // return:
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
  // Summary: up on user clicking next button or up on time out. This functions
  //          saves the user inputs and displays next question if available.
  // para: None
  // return: None

  // 1.0 record user inputs in JSON format
  recordUserInputs();

  // 2.0 get current section and questions details
  num_questions = JSONpaper.sections[current_section].questions.length;
  num_sections = JSONpaper.sections.length;
  current_question = current_question + 1;

  // 3.0 Check if they are more questions in the section
  if (current_question >= num_questions) {
      current_question = 0;
      current_section++;
  }

  // 4.0 Check if they are more sections in the exam paper
  if (current_section >= num_sections) {
      // 4.1 Save user inputes in a JSON File
      createExamSummary();
      location.href = "../Framework/test_summary.html";
  } else{
      // 4.2 if more questions available then display next question
      displayQuestion();
  }
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
          if (typeof(user_input) != "undefined") {
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
