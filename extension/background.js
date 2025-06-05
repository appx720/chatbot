async function checkServerAndSend() {
  try {
    const res = await fetch("http://localhost:8000/send");
    const data = await res.json();

    if (data.send) {
      const oneHourAgo = Date.now() - 1000 * 60 * 60;
      chrome.history.search({ text: '', startTime: oneHourAgo, maxResults: 50 }, (items) => {
        const logs = items.map(item => ({
          url: item.url//,
          // title: item.title,
          // time: new Date(item.lastVisitTime).toISOString()
        }));

        fetch("http://localhost:8000/log", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(logs)
        }).then(() => {
          fetch("http://localhost:8000/done", { method: "POST" });
        });
      });
    }
  } catch (err) {
    console.error("서버 요청 실패:", err);
  }
}

setInterval(checkServerAndSend, 10000);