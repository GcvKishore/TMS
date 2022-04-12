var countDownDate = new Date("Apr 12, 2022 21:00:00").getTime();

let x = setInterval(function () {

    let now = new Date().getTime();

    let timeleft = countDownDate - now;

    let days = Math.floor(timeleft / (1000 * 60 * 60 * 24));
    let hours = Math.floor((timeleft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    let minutes = Math.floor((timeleft % (1000 * 60 * 60)) / (1000 * 60));
    let seconds = Math.floor((timeleft % (1000 * 60)) / 1000);


    document.getElementById("days").innerHTML = checkNum(days);
    document.getElementById("hours").innerHTML = checkNum(hours);
    document.getElementById("minutes").innerHTML = checkNum(minutes);
    document.getElementById("seconds").innerHTML = checkNum(seconds);

    if (timeleft < 0) {
        clearInterval(x);
        document.getElementById("countdown-status").innerHTML = "EXPIRED";
    }
}, 1000);


function checkNum(number) {
    let num = String(number)
    if (num.length === 1) {
        return "0" + num
    } else {
        return num
    }

}
