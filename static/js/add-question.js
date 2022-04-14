let count = 0


let question_tag = `
    <div class="form-group">
        <label class="py-2" for="input-1">Question</label>
        <textarea class="form-control" style="white-space: pre-wrap;" name="question_text" id="input-1" cols="" rows="3" 
        placeholder="Type your question here"></textarea>
    </div>
`
// end of question_tag

let question_info = `
    <div class="row">
        <div class="form-group col-md-3">
            <label class="py-2" for="input-6">Max Time</label>
            <input type="time" step="1" class="form-control" id="input-6" placeholder="HH:MM:SS" name="max_time"
                   value=""
                   aria-describedby="durationDescription">
            <small id="durationDescription" class="form-text text-muted">HH:MM:SS</small>
        </div>
        <div class="form-row col-md-3">
            <label class="py-2" for="input-7">Max Points</label>
            <input type="number" class="form-control" id="input-7" placeholder="Points" name="max_points" value="" min="0"
                   max="100">
        </div>
        <div class="form-row col-md-3">
            <label class="py-2" for="questionDifficultyLevel">Difficulty Level</label>
            <select name="difficulty_level" id="questionDifficultyLevel" class="form-select">
                <option value="None">---</option>
                <option value="Hard">Hard</option>
                <option value="Moderate">Moderate</option>
                <option value="Easy">Easy</option>
            </select>
        </div>
    </div>
`

// end of question_info


function deleteObject(id_name) {
    document.getElementById(id_name).remove();
}


function generateFormat() {
    // show the selected index
    let btn = document.querySelector('#generateBtn');
    let sb = document.querySelector('#questionType')
    let selection = sb.selectedIndex;

    let html_button = ""
    if (selection === 1) {
        html_button = '<div class="row" id="options_area"></div><button class="btn btn-primary" type="button" id="generateBtn" onclick="addOption()"> Add Option</button><hr>'
    } else if (selection === 2) {
        // html_button = '<div id="answers_area"></div><button onclick="addAnswer()" type="button"> Add Answers</button>'
        html_button = '<div class="row" id="answers_area"></div><button onclick="addAnswer()" class="btn btn-primary" type="button" id="generateBtn"> Add Answer</button><hr>'
    } else if (selection === 3 || selection === 4) {
        document.getElementById("addBtn").removeAttribute("disabled");
        document.getElementById("saveBtn").removeAttribute("disabled");
    }
    count = 0

    document.getElementById("questionArea").innerHTML = question_tag + question_info + '<hr>' + html_button;
}

function addOption() {
    document.getElementById("saveBtn").removeAttribute("disabled");
    document.getElementById("addBtn").removeAttribute("disabled");
    count++
    let new_div = document.createElement("div");
    new_div.innerHTML = `
    <div class="form-check mb-3">
        <input class="form-check-input mt-2" id="option-${count}" type="checkbox" name="answer-${count}" value="option-${count}">
        <label class="w-75" for="option-${count}">
            <input class="form-control" type="text" name="option-${count}" maxlength="248" required id="id_text" placeholder="Add Option">
        </label>
            <button class="btn" name="option-${count}" onclick="deleteObject('option-${count}-div-id')"><i class="fa fa-trash"></i></button>
    </div>
    `
    new_div.className = "col-md-4";
    new_div.setAttribute('id', `option-${count}-div-id`);


    document.getElementById('options_area').appendChild(new_div);
}


function addAnswer() {
    document.getElementById("saveBtn").removeAttribute("disabled");
    document.getElementById("addBtn").removeAttribute("disabled");
    count++
    let new_div = document.createElement("div");
    new_div.innerHTML = `
        <div class="input-group mb-3">
            <span class="input-group-text" id="inputGroup-sizing-default${count}">Answer</span>
            <input type="text" class="form-control" aria-label="Sizing example input"
                   aria-describedby="inputGroup-sizing-default${count}" name="answer-${count}" value="">
            <button class="btn" name="option-${count}" onclick="deleteObject('answer-${count}-div-id')"><i class="fa fa-trash"></i></button>
        </div>
    `
    new_div.className = "col-md-4";
    new_div.setAttribute('id', `answer-${count}-div-id`);

    // emd of new_div
    document.getElementById('answers_area').appendChild(new_div);
}
