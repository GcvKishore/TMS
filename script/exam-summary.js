let user_exam_summary = "";
let points = 0;
let total_points = 0
let exam_result_status = "Completed";

try {
    user_exam_summary = localStorage.getItem("user_exam_inputs");
} finally {
}

user_exam_summary = JSON.parse(user_exam_summary);


function onTestSummaryBtnClick() {
    document.getElementById("overview").innerHTML = "";
    generateExamSummary();
}

function generateExamSummary() {
    let result_summary = createResultsSummaryJSON();
    createPageTags();
    displayResultSummary(result_summary);
}

function createResultsSummaryJSON() {
    let result_summary = {};

    for (let i = 0; i < user_exam_summary.length; i++) {
        // console.log(user_exam_summary[i]);
        let section_index = user_exam_summary[i].section;
        let question_index = user_exam_summary[i].question;
        let result = user_exam_summary[i].resultStatus
        let time_elapsed = user_exam_summary[i].timeElapsed

        if (!(section_index in result_summary)) {
            result_summary[section_index] = {};
        }

        if (!(question_index in result_summary[section_index])) {
            result_summary[section_index][question_index] = {
                result: result,
                timeElapsed: time_elapsed
            };
        }
    }
    return result_summary;
}

function createPageTags() {
    document.getElementById("overview").innerHTML = `
                    <div class="row justify-content-center">
                        <div class="col-8 text-center"><h1>Exam Summary</h1><hr><h3 class="" id="result-summary-text"></h3>
                            <table class="table"><thead class="thead-dark header">
                                    <tr><th scope="col">Section</th><th scope="col">Question</th><th scope="col">Result</th><th scope="col">Time Elapsed</th></tr>
                                </thead>
                                <tbody id="exam-summary"></tbody>
                            </table>
                        </div>
                    </div>`;
}

function displayResultSummary(result_summary) {

    let results_html_tags = ""

    for (let i in result_summary) {
        i = parseInt(i)
        let current_section = i + 1;
        for (let j in result_summary[i]) {
            j = parseInt(j)
            const current_question = j + 1;
            const current_question_result = result_summary[i][j].result;
            const current_question_time_elapsed = result_summary[i][j].timeElapsed;
            // console.log(`section-${current_section} question-${current_question} ${current_question_result} ${current_question_time_elapsed}`);

            total_points++;
            let td_class = '<td class="answer-wrong">';
            if (current_question_result.includes("Correct")) {
                points++;
                td_class = '<td class="answer-correct">';
            } else if (current_question_result.includes("Pending")) {
                exam_result_status = "Pending"
                td_class = '<td class="answer-pending">';
            }


            results_html_tags += `
                            <tr>
                            <th scope="row">section ${current_section}</th>
                            <td>question ${current_question}</td>
                            ${td_class}${current_question_result}</td>
                            <td>${current_question_time_elapsed}</td>
                        </tr>`
        }
    }

    document.getElementById("exam-summary").innerHTML = results_html_tags;

    if (exam_result_status === "Pending") {
        document.getElementById("result-summary-text").innerHTML = "Result is Pending";
        document.getElementById("result-summary-text").classList.add("result-pending");
    } else {
        document.getElementById("result-summary-text").innerHTML = `You scored ${points} of ${total_points} points`;
        document.getElementById("result-summary-text").classList.remove("result-pending");
    }
}
