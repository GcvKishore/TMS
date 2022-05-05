let total_question_time_left = document.getElementById('total_question_time_left')
let total_question_time = document.getElementById('total_question_time')

let question_time_left
let question_total_time

if (total_question_time_left) {
    console.log('has')
    question_time_left = convert_to_seconds(total_question_time_left)
    question_total_time = convert_to_seconds(total_question_time)
}

function convert_to_seconds(element) {
    const hms = element.innerText;
    const [hours, minutes, seconds] = hms.split(':');
    const totalSeconds = (+hours) * 60 * 60 + (+minutes) * 60 + (+seconds);
    return totalSeconds.toString()
}

Question_duration = document.getElementById('question_countdown')

if (Question_duration) {
    if (question_time_left !== 'NaN') {
        console.log(question_time_left)
        startCountDown(parseInt(question_time_left))
    }
}

function startCountDown(max_time) {
    let timing = max_time;
    let timer = setInterval(function () {
        let hrs;
        let mins;
        let secs;
        if (timing <= 0) {
            clearInterval(timer);
            document.getElementById("timeout-btn").click();
        } else {
            hrs = Math.floor(timing / 3600).toString();
            mins = Math.floor((timing % 3600) / 60).toString();
            secs = Math.floor(((timing % 3600) % 60) % 60).toString();

            if (hrs.length === 1) {
                hrs = `0${hrs}`
            }
            if (mins.length === 1) {
                mins = `0${mins}`
            }
            if (secs.length === 1) {
                secs = `0${secs}`
            }

            let countdown_element = document.getElementById("question_countdown")

            countdown_element.classList.add('bg-success', 'text-white')
            if ((timing / question_total_time
) < .50) {
                countdown_element.classList.remove('bg-success', 'text-white')
                countdown_element.classList.add('bg-warning', 'text-dark')
            }
            if ((timing / question_total_time) < .25) {
                countdown_element.classList.remove('bg-warning', 'text-dark')
                countdown_element.classList.add('bg-danger', 'text-white')
            }

            countdown_element.innerHTML = `Time left: ${hrs}:${mins}:${secs}`;
        }
        timing--;
    }, 1000);
}


