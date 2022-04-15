total_exam_duration = document.getElementById('totalExamDuration')

if (total_exam_duration) {
    const hms = total_exam_duration.innerText;
    const [hours, minutes, seconds] = hms.split(':');
    const totalSeconds = (+hours) * 60 * 60 + (+minutes) * 60 + (+seconds);
    if (totalSeconds !== 0) {
        localStorage.setItem("time_left", totalSeconds.toString());
        localStorage.setItem("total_time", totalSeconds.toString());
    }
}


exam_duration = document.getElementById('exam_countdown')

if (exam_duration) {
    time_left = localStorage.getItem("time_left");
    total_time = localStorage.getItem("total_time");
    if (time_left !== 'NaN') {
        startCountDown(parseInt(time_left))
    }
    console.log(time_left)
}

function startCountDown(max_time) {
    console.log(max_time)
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

            countdown_element.innerHTML = `Time left: ${hrs}:${mins}:${secs}`;
            localStorage.setItem("time_left", timing.toString());
        }
        timing--;
    }, 1000);
}


