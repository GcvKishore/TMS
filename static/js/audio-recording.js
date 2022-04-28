let constraintObj = {
    audio: true,
    video: false,
};

navigator.mediaDevices.getUserMedia(constraintObj)
    .then(mediaStreamObj => {
        let start = document.getElementById('btn-start-recording');
        let stop = document.getElementById('btn-stop-recording');
        let fileInput = document.getElementById('formFileSm');
        let audio_recorder = new MediaRecorder(mediaStreamObj);
        let audio_chunks = [];

        start.addEventListener('click', () => {
            audio_recorder.start();
            document.getElementById("text").innerHTML='Started Recording..';
            console.log(audio_recorder.state);
        })
        stop.addEventListener('click', () => {
            audio_recorder.stop();
            document.getElementById("text").innerHTML='';
            document.getElementById("stop").innerHTML='Recording Stopped..';
            console.log(audio_recorder.state)
        })

        audio_recorder.ondataavailable = ev => {
            audio_chunks.push(ev.data);
        }

        audio_recorder.onstop = () => {
            console.log('saving process')
            let blob = new Blob(audio_chunks, {type: 'audio/mpeg'});
            audio_chunks = []

            let audio_url = window.URL.createObjectURL(blob);

            let audio_files = document.getElementById('recordings')
            let sound = document.createElement('audio');
            sound.id = 'audio-player';
            sound.controls = 'controls';
            sound.src = audio_url;
            sound.type = 'audio/mpeg';
            audio_files.innerHTML = ''
            audio_files.appendChild(sound);

            let random_file_name = Math.random().toString(36).substr(2, 9)
            let file = new File([blob], `${random_file_name}.mpeg`);
            let container = new DataTransfer();
            container.items.add(file);
            fileInput.files = container.files;
        }
    }).catch(err => {
    console.log(err.name, err.message)
})
