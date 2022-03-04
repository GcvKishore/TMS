//Load json -- Load json and store it in a global variable ==> exam_details (Chaitanya)
let JSONpaper = $.getJSON({
    url : "../sampleData/sample_test.json",
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

JSONpaper = JSON.parse(JSONpaper.responseText);
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
function generateFU(){
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
function recordUserInputs(){
    // Summary: Records all the user inputs by calling all the different types of questions.
    // para: None
    // return: None

    let ans_submitted=[];
    let status="Pending";
  switch (current_question_type) {
    case "Multiple Choice - Multiple Answers":
      ans_submitted=recordMCMA();
      break;
    case "Fill in the blanks":
      ans_submitted=recordFITB();
      break;
    case "Short Answer":
      ans_submitted=recordSA();
      break;
    case "File Submission":
      ans_submitted= recordFS();
      break;
    default:
  }
    eval_Type=current_question_details.evaluationType;
    crct_Ans=current_question_details.answers;
    if(evaluationType=="auto")
        {
            evaluateUserAnswer(ans_submitted, crct_Ans);
        }
    let summary={
        startTimeStamp: start_time_stamp,
        endTimeStamp: end_time_stamp,
        section:current_section,
        question:current_question,
        ansSubmitted: ans_submitted,
        resultStatus: status
    };
    user_answers.push(summary);
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
