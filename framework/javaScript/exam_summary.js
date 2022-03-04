let user_exam_summary = localStorage.getItem("user_exam_inputs");


const exam_results = JSON.parse(user_exam_summary);


function onTestSummaryBtnClick() {
    document.getElementById("overview").innerHTML = "";
    displayTestSummary();
}


function displayTestSummary() {
    createTags();
    html_tag = '<tr class="header"><th>Section</th><th>Question</th><th>Result</th><th>Time Elapsed</th></tr>'
    for (let i = 0; i < exam_results.length; i++) {
        html_tag +=`<tr>
                        <td>Section ${exam_results[i].section + 1}</td>
                        <td>Question ${exam_results[i].question + 1}</td>
                        <td>${exam_results[i].resultStatus}</td>
                        <td>${exam_results[i].timeElapsed}</td>
                    </tr>`;
    }
    document.getElementById("detailed-exam-summary").innerHTML = html_tag;
}


function createTags() {
    document.getElementById("overview").innerHTML = `
                <div class="row justify-content-center">
                    <div class="col-md-8">
                        <div class="row text-center">
                            <h1 class="">Exam Summary</h1>
                            <hr>
                            <h5 class="" id="user-score">Pending</h5>
                            <table id="detailed-exam-summary">
                            </table>
                        </div>
                    </div>
                </div>`
}
