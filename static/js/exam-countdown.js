let total_exam_time_left = document.getElementById('total_exam_time_left')
let total_exam_time = document.getElementById('total_exam_time')

if (total_exam_time_left.innerText.includes('-')) {
    alert("TIMEOUT: You are out of time.")
    document.getElementById("quit-btn").click();
}


let time_left
let total_time

if (total_exam_time_left) {
    time_left = convert_to_seconds(total_exam_time_left)
    total_time = convert_to_seconds(total_exam_time)
}

function convert_to_seconds(element) {
    const hms = element.innerText;
    const [hours, minutes, seconds] = hms.split(':');
    const totalSeconds = (+hours) * 60 * 60 + (+minutes) * 60 + (+seconds);
    return totalSeconds.toString()
}

console.log(time_left)
console.log(total_time)

exam_duration = document.getElementById('exam_countdown')

if (exam_duration) {
    if (time_left !== 'NaN') {
        startCountDown(parseInt(time_left))
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
            alert("TIMEOUT: You are out of time. Click ok to See your exam result")
            document.getElementById("quit-btn").click();
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

            let countdown_element = document.getElementById("exam_countdown")

            countdown_element.classList.add('bg-success', 'text-white')
            if ((timing / total_time) < .50) {
                countdown_element.classList.remove('bg-success', 'text-white')
                countdown_element.classList.add('bg-warning', 'text-dark')
            }
            if ((timing / total_time) < .25) {
                countdown_element.classList.remove('bg-warning', 'text-dark')
                countdown_element.classList.add('bg-danger', 'text-white')
            }

            countdown_element.innerHTML = `Time Left for Exam: ${hrs}:${mins}:${secs}`;
            localStorage.setItem("time_left", timing.toString());
        }
        timing--;
    }, 1000);
}


