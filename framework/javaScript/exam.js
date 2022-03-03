//Load json -- Load json and store it in a global variable ==> exam_details (Chaitanya)
let JSONpaper = $.getJSON({
    url : "../framework/sample_test.json",
    async: false,
  });

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
function startExam(){
    // Starts the test once the function is invoked and calls the displayQuestion().
    displayQuestion();
}

//Display Questions (Amulya)
function displayQuestion(){
    // Summary: 
    // para: 
    // return: 

}

// Start countdown (Priyusha)
function startCountDown(max_time){
    // Summary:
    // para:
    // return:

}

// Generate questions based on questionType
// Multiple Choice - Multiple Answers (Priyusha)
function generateMCMA(){
    // Summary:
    // para:
    // return:

}

// Fill in the blanks (Vedavyas)
function generateFITB(){
    // Summary:
    // para:
    // return:

}

// Short Answer (Amulya)
function generateSA(){
    // Summary:
    // para:
    // return:

}

// File Submission (Chaitanya)
function generateFU(){
    // Summary:
    // para:
    // return:

}

// on next button click
// record user_inputs (Vedavyas)
function onNextClick(){
    // Summary:
    // para:
    // return:

}


// record user_inputs (Chaitanya)
function recordUserInputs(){
    // Summary:
    // para:
    // return:

}


// get user answers based on question type
// Multiple Choice - Multiple Answers (Priyusha)
function recordMCMA(){
    // Summary:
    // para:
    // return:

}

// Fill in the blanks (Vedavyas)
function recordFITB(){
    // Summary:
    // para:
    // return:

}

// Short Answer (Amulya)
function recordSA(){
    // Summary:
    // para:
    // return:

}

// File Submission (Chaitanya)
function recordFS(){
    // Summary:
    // para:
    // return:

}

// evaluate user Answers (Priyusha)
function evaluateUserAnswer(user_answers, actual_answers){
    // Summary:
    // para:
    // return:

}

// Show exam overview and highlight current question (optional)
function examOverview(){
    // Summary:
    // para:
    // return:

}


// generate exam summary json file (Optional)
function createExamSummary(){
    // Summary:
    // para:
    // return:

}
