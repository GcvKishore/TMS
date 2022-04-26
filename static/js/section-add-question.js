let count = 0

function deleteObject(id_name) {
    document.getElementById(id_name).remove();
    let answers_count = document.getElementsByClassName('question_answers').length
    if (answers_count === 0) {
        document.getElementById("saveCreateBtn").disabled = true
        document.getElementById("addBtn").disabled = true
        document.getElementById("saveExitBtn").disabled = true
    }
}


function generateFormat() {
    // show the selected index
    let btn = document.querySelector('#generateBtn');
    let sb = document.querySelector('#questionType')
    let selection = sb.selectedIndex;

    let html_button = ""
    if (selection === 1) {
        html_button = '<div class="row" id="options_area"></div><button class="btn btn-primary btn-sm" type="button" id="generateBtn" onclick="addOption()"> Add Option</button><hr>'
    } else if (selection === 2) {
        // html_button = '<div id="answers_area"></div><button onclick="addAnswer()" type="button"> Add Answers</button>'
        html_button = '<div class="row" id="answers_area"></div><button onclick="addAnswer()" class="btn btn-primary btn-sm" type="button" id="generateBtn"> Add Answer</button><hr>'
    } else if (selection === 3 || selection === 4) {
        document.getElementById("addBtn").removeAttribute("disabled");
        document.getElementById("saveCreateBtn").removeAttribute("disabled");
    }
    count = 0
    document.getElementById('questionTextArea').removeAttribute("hidden");

    document.getElementById("questionArea").innerHTML = '<hr>' + html_button;
}

function addOption() {
    document.getElementById("saveCreateBtn").disabled = false
    document.getElementById("addBtn").disabled = false
    document.getElementById("saveExitBtn").disabled = false
    count++
    let new_div = document.createElement("div");
    new_div.innerHTML = `
    <div class="form-check mb-3">
        <input class="form-check-input mt-2 question_answers" id="option-${count}" type="checkbox" name="answer-${count}" value="option-${count}">
        <label class="w-75" for="option-${count}">
            <input class="form-control" type="text" name="option-${count}" maxlength="248" required id="id_text" placeholder="Add Option">
        </label>
            <button class="btn" name="option-${count}" onclick="deleteObject('option-${count}-div-id')"><i class="fa fa-trash"></i></button>
    </div>
    `
    new_div.className = "col-md-6";
    new_div.setAttribute('id', `option-${count}-div-id`);


    document.getElementById('options_area').appendChild(new_div);
}


function addAnswer() {
    document.getElementById("saveCreateBtn").disabled = false
    document.getElementById("addBtn").disabled = false
    document.getElementById("saveExitBtn").disabled = false
    count++
    let new_div = document.createElement("div");
    new_div.innerHTML = `
        <div class="input-group mb-3">
            <span class="input-group-text" id="inputGroup-sizing-default${count}">Answer</span>
            <input type="text" class="form-control question_answers" aria-label="Sizing example input"
                   aria-describedby="inputGroup-sizing-default${count}" name="answer-${count}" value="">
            <button class="btn" name="option-${count}" onclick="deleteObject('answer-${count}-div-id')"><i class="fa fa-trash"></i></button>
        </div>
    `
    new_div.className = "col-md-6";
    new_div.setAttribute('id', `answer-${count}-div-id`);

    // emd of new_div
    document.getElementById('answers_area').appendChild(new_div);
}
