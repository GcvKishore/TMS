let question_type = document.querySelector('#question_type').innerHTML;

if (question_type === 'Fill In The Blanks') {
    let question_text = document.querySelector('#question_text').innerHTML;
    let count = 1
    while (true) {
        let blank = '__________'
        let blank_html_tag = `<span><input type="text" id="fitb-${count}" name="answer-${count}" style="width: 10vw;"/></span>`
        if (question_text.includes(blank)) {
            question_text = question_text.replace(blank, blank_html_tag);
            count++
        } else {
            break
        }
    }
    document.getElementById("question_text").innerHTML = question_text;
}
