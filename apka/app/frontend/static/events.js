document.getElementById("load-teams").addEventListener("click", function() {
    fetch("/teams-events")
      .then(resp => resp.json())
      .then(events => {
        const list = document.getElementById("eventsList");
        list.innerHTML = "";
        events.forEach(evt => {
          const li = document.createElement("li");
          li.textContent = `Tytuł: ${evt.title}, start: ${evt.start}, uczestnicy: ${evt.attendees.join(", ")}`;
          list.appendChild(li);
        });
      })
      .catch(err => console.error(err));
  });
  
  document.getElementById("load-zoom").addEventListener("click", function() {
    fetch("/zoom-meetings")
      .then(resp => resp.json())
      .then(meetings => {
        const list = document.getElementById("eventsList");
        list.innerHTML = "";
        meetings.forEach(m => {
          const li = document.createElement("li");
          li.textContent = `Spotkanie: ${m.topic}, start: ${m.start_time}, link: ${m.join_url}`;
          list.appendChild(li);
        });
      })
      .catch(err => console.error(err));
  });
  