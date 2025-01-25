function showNotification(message, type = "info") {
    const notification = document.createElement("div");
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 1000);
}

const recordBtn = document.getElementById("record-btn");
const startButton = document.getElementById("startButton");
const stopButton = document.getElementById("stopButton");
const saveButton = document.getElementById("save-recording");
const titleInput = document.getElementById("recording-title");
const see_events = document.getElementById("events-btn");
const timerDisplay = document.getElementById("timer");
const see_recordings = document.getElementById("recordings-btn");
const windowSelection = document.getElementById("window-selection");

let mediaRecorder;
let recordedChunks = [];
let stream=null; // Przechowujemy odniesienie do strumienia
let recordingStartTime;
let timerInterval;


async function selectWindow() {
    if(stream==null){
        try {
            stream = await navigator.mediaDevices.getDisplayMedia({
                video: true,
                audio: true
            })
            handleStream(stream);   
            startButton.disabled = false;
        } catch (error) {
            console.error("Błąd podczas wybierania okna:", error);
            showNotification("Błąd podczas wybierania okna", "error");
        }}
    else {
        stream.getTracks().forEach(track => track.stop());
        stream == null;
        try {
            stream = await navigator.mediaDevices.getDisplayMedia({
                video: true,
                audio: true
            })
            handleStream(stream);  
            startButton.disabled = false; 
        } catch (error) {
            console.error("Błąd podczas wybierania okna:", error);
            showNotification("Błąd podczas wybierania okna", "error");
        }
    }
}

// Obsługa strumienia
function handleStream(stream) {
    mediaRecorder = new MediaRecorder(stream);
    recordedChunks = [];

    mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
            recordedChunks.push(event.data);
        }
    };

    mediaRecorder.onstop = () => {
        const blob = new Blob(recordedChunks, { type: "video/webm" });
        saveButton.disabled = false;
        saveButton.onclick = () => saveRecording(blob);
    };

    startButton.onclick = () => {
        try {
            if (mediaRecorder.state === "inactive") {
                mediaRecorder.start();
                console.log("Nagrywanie rozpoczęte...");
                showNotification("Nagrywanie rozpoczęte...", "success");

                // Uruchomienie timera
                recordingStartTime = Date.now();
                timerInterval = setInterval(updateTimer, 1000); // Co sekundę aktualizuje czas
                timerDisplay.style.display = "block"; 
                startButton.disabled = true;
                stopButton.disabled = false;
                alert("Pozostaw tą stronę otwartą do zakończenia nagrywania (zapisz)");
           } else {
                throw new Error("Nagrywanie już trwa.");
            }
        } catch (error) {
            console.error("Błąd podczas rozpoczęcia nagrywania:", error);
            showNotification("Nagrywanie jest już w toku. Zakończ je, aby rozpocząć nowe.", "error");
        }
    };

    stopButton.onclick = () => {
        try {
            if (mediaRecorder.state === "recording") {
                mediaRecorder.stop();
                console.log("Nagrywanie zatrzymane.");
                showNotification("Nagrywanie zatrzymane.", "success");
                startButton.disabled = false;
                stopButton.disabled = true;
            } else {
                throw new Error("Nagrywanie nie zostało rozpoczęte.");
            }
        } catch (error) {
            console.error("Błąd podczas zatrzymywania nagrywania:", error);
            showNotification("Nagrywanie nie zostało jeszcze rozpoczęte", "error");
        }
        clearInterval(timerInterval); 
    };
}

function updateTimer() {
    const elapsedTime = Math.floor((Date.now() - recordingStartTime) / 1000); // Czas w sekundach
    const minutes = String(Math.floor(elapsedTime / 60)).padStart(2, '0'); // Minuty
    const seconds = String(elapsedTime % 60).padStart(2, '0'); // Sekundy
    timerDisplay.textContent = `${minutes}:${seconds}`;
}

async function saveRecording(blob) {
    const title = titleInput.value;
    const formData = new FormData();
    formData.append("file", blob, `${title}.webm`);
    formData.append("title", title);

    try {
        const response = await fetch("/save", {
            method: "POST",
            body: formData,
        });
        document.getElementById("timer").style.display = "none"; // Ukrywamy zegar
        if (response.ok) {
            showNotification("Nagranie zapisane!", "success");
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
                stream = null; 
                console.log("Strumień zatrzymany.");
                showNotification("Strumień zatrzymany", "success");

            }
        } else {
            alert("Błąd podczas zapisywania.");
            showNotification("Błąd podczas zapisywania", "error");
        }
    } catch (error) {
        console.error("Błąd podczas wysyłania pliku:", error);
        showNotification("Błąd podczas wysyłania pliku", "error");
    }
    if (stream) {
                stream.getTracks().forEach(track => track.stop());
                stream = null; 
                console.log("Strumień zatrzymany.");
                showNotification("Strumień zatrzymany.", "success");
            }
    
    clearInterval(timerInterval);
    timerDisplay.textContent = "00:00"; 
    timerDisplay.style.display = "none";
    titleInput.value = ""; 
    saveButton.disabled = true;
}

recordBtn.addEventListener("click", selectWindow);
