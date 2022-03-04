let current_section = 0;
let current_question = 0;
let question_start_timestamp;
let question_end_timestamp;
let current_question_details;
let current_question_type;
let user_exam_inputs = [];
let timer;
let exam_paper = $.getJSON({
    url: "../framework/sampleData/sample_test.json",
    async: false,
});
exam_paper = JSON.parse(exam_paper.responseText);


startExam();


function startExam() {
    examOverview();
    displayQuestion();
}


function displayQuestion() {
    question_start_timestamp = new Date().toLocaleTimeString();

    let section = exam_paper.sections[current_section];
    let question = section.questions[current_question];
    let max_Time = question.maxTime;

    current_question_type = question.questionType;
    current_question_details = question.questionDetails;

    startCountDown(max_Time);
    document.getElementById("current-section").innerHTML = current_section + 1;
    document.getElementById("current-question").innerHTML = current_question + 1;
    document.getElementById("question-type-title").innerHTML = current_question_type;

    let currrent_question_class = `sec-${current_section + 1}-que-${current_question + 1}`;
    document.getElementById(currrent_question_class).style.color = "#FABC75";

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


function startCountDown(max_time) {
    var timing = max_time;
    timer = setInterval(function() {

        if (timing <= 0) {
            clearInterval(timer);
            document.getElementById("next-btn").click();
        } else {
            mins = Math.floor(timing / 60);
            secs = Math.floor(timing % 60);
            document.getElementById("countdown").innerHTML = `${mins}:${secs}`;
        }
        timing--;
    }, 1000);
}


function generateMCMA() {
    let question_text = current_question_details.questionText;
    document.getElementById("question-text").innerHTML = question_text;

    let num_options = current_question_details.options.length;
    let options = current_question_details.options;
    let input_tag = "";

    for (var i = 0; i < num_options; i++) {
        input_tag += `<div class="form-check"><label><input class="form-check-input" type="checkbox" value="${String.fromCharCode(97+i)}" id="defaultCheck${i}">${options[i]}</label></div>`;
    }

    document.getElementById("answer-input-options").innerHTML = input_tag;
}


function generateFITB() {
    let question_text = current_question_details.questionText;
    let blanks = current_question_details.answer;

    for (const i in blanks) {
        let HTML_tag = `<span><input class="FIB" id=fITB-option-${i} spellcheck="false" maxlength="28" style="width: 10vw;"></span>`;
        question_text = question_text.replace(blanks[i], HTML_tag);
    }

    document.getElementById("question-text").innerHTML = question_text;
}


function generateSA() {
    let question_text = current_question_details.questionText;
    document.getElementById("question-text").innerHTML = question_text;

    let maxchars = current_question_details.MaxWords * 6;
    let input_tag = "";

    input_tag = `<div class="mb-3"><textarea class="form-control" id="SA-Textarea1" rows="6" maxlength="${maxchars}" placeholder="Type your answer here"></textarea></div>`;

    document.getElementById("answer-input-options").innerHTML = input_tag;
}


function generateFU() {
    let question_text = current_question_details.questionText;
    document.getElementById("question-text").innerHTML = question_text;

    input_tag = `<div class="row upload_box align-items-center"> <div class="col text-center"><input type="file" id="myfile" name="myfile"></div></div> `;
    document.getElementById("answer-input-options").innerHTML = input_tag;
}


function onNextClick() {
    question_end_timestamp = new Date().toLocaleTimeString();

    recordUserInputs();
    resetDisplayText();

    num_questions = exam_paper.sections[current_section].questions.length;
    num_sections = exam_paper.sections.length;
    current_question = current_question + 1;

    if (current_question >= num_questions) {
        current_question = 0;
        current_section++;
    }

    if (current_section >= num_sections) {
        saveExamSummary();
        location.href = "../framework/exam_summary.html";
    } else {
        displayQuestion();
    }
}


function resetDisplayText() {
    let currrent_question_class = `sec-${current_section + 1}-que-${current_question + 1}`;
    document.getElementById(currrent_question_class).style.color = "#FBF8F2";

    document.getElementById("countdown").innerHTML = "";
    document.getElementById("question-text").innerHTML = "";
    document.getElementById("answer-input-options").innerHTML = "";
    document.getElementById("current-section").innerHTML = "";
    document.getElementById("current-question").innerHTML = "";
    document.getElementById("question-type-title").innerHTML = "";

    clearInterval(timer);
}


function recordUserInputs() {
    let submitted_answer = [];
    let status = "Pending";
    switch (current_question_type) {
        case "Multiple Choice - Multiple Answers":
            submitted_answer = recordMCMA();
            break;
        case "Fill in the blanks":
            submitted_answer = recordFITB();
            break;
        case "Short Answer":
            submitted_answer = recordSA();
            break;
        case "File Submission":
            submitted_answer = recordFS();
            break;
        default:
    }

    let evaluation_type = current_question_details.evaluationType;
    let correct_answer = current_question_details.answer;

    if (evaluation_type == "auto") {
        status = evaluateUserAnswer(submitted_answer, correct_answer);
    }

    let current_question_summary = {
        section: current_section,
        question: current_question,
        answerSubmitted: submitted_answer,
        resultStatus: status,
        questionStartTimestamp: question_start_timestamp,
        questionEndTimestamp: question_end_timestamp
    };

    user_exam_inputs.push(current_question_summary);
}


function recordMCMA() {
    let checkbox = document.querySelectorAll("input[type=checkbox]:checked");
    let checked_options = [];

    try {
        for (const i in checkbox) {
            check_box_value = checkbox[i].value;
            if (typeof check_box_value != "undefined") {
                checked_options.push(check_box_value);
            }
        }
    } finally {
        return checked_options;
    }
}


function recordFITB() {
    let user_exam_inputs = document.querySelectorAll(".FIB");
    let answers = [];

    try {
        for (const i in user_exam_inputs) {
            user_input = user_exam_inputs[i].value;
            if (typeof user_input != "undefined") {
                answers.push(user_input);
            }
        }
    } finally {
        return answers;
    }
}


function recordSA() {
    let answer = "";

    try {
        var SA_input = document.getElementById("exampleFormControlTextarea1").value;
        answer = SA_input;
    } finally {
        return answer;
    }
}


function recordFS() {
    let answer = "";
    try {
        let data = document.getElementById("myfile").value;
        answer = data;
    } finally {
        return answer;
    }
}


function evaluateUserAnswer(submitted_answer, correct_answer) {
    for (let i = 0; i < correct_answer.length; i++) {
        let result = String(correct_answer[i]).localeCompare(String(submitted_answer[i]));
        if (result != 0) {
            return ("Wrong Answer");
        }
    }
    return ("Correct Answer");
}


function examOverview() {
    let num_sections = exam_paper.sections.length;
    let sections_overview = "";

    for (let i = 1; i <= num_sections; i++) {

        let num_questions = exam_paper.sections[i - 1].questions.length;
        let questions_html_tags = "";

        for (let j = 1; j <= num_questions; j++) {
            questions_html_tags += `<li class="py-1" id="sec-${i}-que-${j}">Question ${j}</li>`;
        }

        let questions_overview = `<ul class="px-1">${questions_html_tags}</ul>`;
        sections_overview += `<li class="py-2"><span id="sec-${i}">Section ${i}</span>${questions_overview}</li>`;
    }

    let overview_html_tag = `<ol>${sections_overview}</ol>`;
    document.getElementById("exam-overview").innerHTML = overview_html_tag;
}


function saveExamSummary() {
    const jsonData = JSON.stringify(user_exam_inputs);
    localStorage.setItem("user_exam_inputs", jsonData);
}
